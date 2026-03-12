from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import zlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

#
# try:
#     import grp, pwd
# except ModuleNotFoundError:
#     pass


class WiObject:
    def __init__(self, obj_type: str, content: bytes):
        self.type = obj_type
        self.content = content

    def hash(self) -> str:
        """hash file informationn to byte w/o losing info"""
        header = f"{self.type} {len(self.content)}\0".encode()
        return hashlib.sha1(header + self.content).hexdigest()

    def serialize(self) -> bytes:
        """ensure lossless compression"""
        header = f"{self.type} {len(self.content)}\0".encode()
        return zlib.compress(header + self.content)

    @classmethod
    def deserealization(cls, data: bytes) -> WiObject:
        decompressed = zlib.decompress(data)
        null_idx = decompressed.find(b"\0")
        header = decompressed[:null_idx].decode()
        content = decompressed[null_idx + 1 :]

        obj_type, _ = header.split(" ")

        return cls(obj_type, content)


class Blob(WiObject):
    def __init__(self, content: bytes) -> None:
        super().__init__("blob", content)

    # set getter func for blob (if needed)
    def get_content(self) -> bytes:
        return self.content


class Tree(WiObject):
    def __init__(self, entries: List[Tuple[str, str, str]]):
        self.entries = entries or []
        content = self._ser_entries()
        super().__init__("tree", content)

    def _ser_entries(self) -> bytes:
        """serializes entries so it can be passed to init"""
        content = b""
        for mode, name, obj_hash in sorted(self.entries):
            content += f"{mode} {name}\0".encode()
            content += bytes.fromhex(obj_hash)

        return content

    def add_entry(self, mode: str, name: str, obj_hash: str):
        self.entries.append((mode, name, obj_hash))
        self.content = self._ser_entries()

    @classmethod
    def from_content(cls, content: bytes) -> Tree:
        tree = cls()
        i = 0
        while i < len(content):
            null_idx = content.find(b"\0", i)
            if null_idx == -1:
                break
            mode_name = content[i:null_idx].decode()
            mode, name = mode_name.split(" ", 1)
            obj_hash = content[null_idx + 1 : null_idx + 21].hex()
            tree.entries.append((mode, name, obj_hash))
            i = null_idx + 21
        return tree


class Repo:
    def __init__(self, path=".") -> None:
        self.path = Path(
            path
        ).resolve()  # checks initialize a repo on working directory the method resolve() pass an absoulute path.

        ## "wigit" is same as .git folder. the following files will be the same as git/
        self.wgit_dir = self.path / ".wigit"

        self.obj_dir = self.wgit_dir / "objects"

        # refs for branch names and pointers to dirs
        self.refs_dir = self.wgit_dir / "refs"

        self.heads_dir = self.refs_dir / "heads"

        self.head_file = self.wgit_dir / "W_HEAD"

        self.index_file = self.wgit_dir / "index"

    def init(self) -> bool:
        if self.wgit_dir.exists():
            return False

        # creation of base dirs

        self.wgit_dir.mkdir()
        self.obj_dir.mkdir()
        self.refs_dir.mkdir()
        self.heads_dir.mkdir()

        # creation of initial HEAD (W_HEAD)
        self.head_file.write_text("refs: refs/heads/wiener-main\n")

        # creates the index file
        self.save_index({})

        print(f"initialize empty wiener-git repo in {self.wgit_dir}")
        return True

    def store_objects(self, obj: WiObject) -> str:
        obj_hash = obj.hash()
        obj_dir = (
            self.obj_dir / obj_hash[:2]
        )  # <- requires composition of hash <dir>+<hash>
        obj_file = obj_dir / obj_hash[2:]
        if not obj_file.exists():  # <- check if file exists
            obj_dir.mkdir(exist_ok=True)
            obj_file.write_bytes(obj.serialize())
        return obj_hash

    def load_index(self) -> Dict[str, str]:
        if not self.index_file.exists():
            return {}
        try:
            return json.loads(self.index_file.read_text())
        except:
            return {}

    def save_index(self, index: Dict[str, str]):
        """saves the index again to json"""

        self.index_file.write_text(json.dumps(index, indent=2))

    def add_file(self, path: str) -> None:
        """adds file to index used on add_paths"""
        full_path = self.path / path
        if not full_path.exists():
            raise FileNotFoundError(f"path not {path} found")
        # set content (read file)
        content = full_path.read_bytes()
        # create blob
        blob = Blob(content)
        # store blob on (.wigit/objects)
        # the (/objects) dir is sort of the database (elegant solution to safe space)
        blob_hash = self.store_objects(blob)
        # update index
        index = self.load_index()
        index[path] = blob_hash
        self.save_index(index)
        pass

    def add_directory(self, path: str):
        """same as file but with dirs"""
        # check if exist path
        full_path = self.path / path
        if not full_path.exists():
            raise FileNotFoundError(f"directory not found in {path} ")
        if not full_path.is_dir():
            raise FileNotFoundError(f"file on {path} is not a directory")

        index = self.load_index()
        added_count = 0

        for file_path in full_path.rglob("*"):
            if file_path.is_file():
                if ".wigit" in file_path.name:
                    continue
                # create blob for every file on dir
                content = file_path.read_bytes()
                blob = Blob(content)
                # store blob hash
                blob_hash = self.store_objects(blob)
                # update index
                rel_path = str(file_path.relative_to(self.path))
                index[rel_path] = blob_hash

        self.save_index(index)

        if added_count > 0:
            print(f"added {added_count} files to repo")
        else:
            print(f"repo in {path}already up to date")
            print("there is nothing else to do.")

    def add_paths(self, path: str) -> None:
        """checks if path exists and define if file or directory"""
        full_path = self.path / path

        if not full_path.exists():
            raise FileNotFoundError(f"path not {path} found")
        if full_path.is_file():
            self.add_file(path)
        # elif full_path.is_dir():
        # self.add_directory(path)
        else:
            raise ValueError(f"unknown path type {path}")

    def create_tree(self):
        """create tree from index"""  # staging area
        index = self.load_index()
        if not index:
            tree = Tree()
            return self.store_objects(tree)
        dirs = {}
        files = {}

        for file_path, blob_hash in index.items():
            parts = file_path.split("/")

            if len(parts) == 1:  # <- file is in the root folder
                files[parts[0]] = blob_hash
            else:
                dir_name = parts[0]
                if dir_name not in dirs:
                    dirs[dir_name] = {}
                current = dirs[dir_name]

    def commit(self, message: str) -> None:
        """commit func logic"""
        tree_hash = self.create_tree()


def main():
    parser = argparse.ArgumentParser(
        description="Wiener-git its a git clone written on python to understand how it works under the hood :)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # def commands (they require to be parsed bc its a CLI)

    winit_parser = subparsers.add_parser("winit", help="initialize repo")
    add_parser = subparsers.add_parser("wiadd", help="add files to the existing repo")
    commit_parser = subparsers.add_parser(
        "wicommit", help="commit files to the existing repo"
    )
    push_parser = subparsers.add_parser("wipush", help="push files to remote")

    commit_parser.add_argument(
        "-m", "--mesage", help="message to the commit.", required=True
    )
    add_parser.add_argument("paths", nargs="+", help="paths and directories to add.")
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    repo = Repo()
    try:
        if args.command == "winit":
            if not repo.init():
                print("already on a wiener repo :)")
                return
        elif args.command == "wiadd":
            if not repo.wgit_dir.exists():
                print("not in a wiener repo")
                return
        elif args.command == "wicommit":
            if not repo.wgit_dir.exists():
                print("not in a wiener repo")
                return
            repo.commit(args.message)

    except Exception as error:
        print(f"error:{error}")
        sys.exit(1)


main()
