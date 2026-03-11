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
    def __init__(self, obj_type: str, content: bytes) -> None:
        super().__init__("blob", content)

    # set getter func for blob (if needed)
    def get_content(self) -> bytes:
        return self.content


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

        self.index_file.write_text(json.dumps({}, indent=2))

        print(f"initialize empty wiener-git repo in {self.wgit_dir}")
        return True

    def store_objects(self, obj: WiObject) -> str:
        obj_hash = obj.hash()
        obj_dir = self.obj_dir / obj_hash[:2]
        obj_file = obj_dir / obj_hash[2:]
        if not obj_file.exists():
            obj_dir.mkdir(exist_ok=True)
            obj_file.write_bytes(obj.serialize())
        return obj_hash

    def add_file(self, path: str) -> None:
        """adds file to index used on add_paths"""
        full_path = self.path / path
        if not full_path.exists():
            raise FileNotFoundError(f"path not {path} found")
        # set content (read file)
        content = full_path.read_bytes()
        # create blob
        blob = Blob(content)
        pass

    def add_paths(self, path: str) -> None:
        """checks if path exists and define if file or directory"""
        full_path = self.path / path

        if not full_path.exists():
            raise FileNotFoundError(f"path not {path} found")
        if full_path.is_file():
            self.add_file(full_path)
        elif full_path.is_dir():
            self.add_directory(full_path)
        else:
            raise ValueError(f"unknown path type {path}")


## important lybraries imported each explained on [README](./yap.md)


def main():
    parser = argparse.ArgumentParser(
        description="Wiener-git its a git clone written on python to understand how it works under the hood :)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # def commands (they require to be parsed bc its a CLI)

    init_parser = subparsers.add_parser("winit", help="initialize repo")
    add_parser = subparsers.add_parser("wiadd", help="add files to the existing repo")
    push_parser = subparsers.add_parser("wipush", help="push files to remote")

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
                print("already on a wiener repo :)")
                return
            print(args.paths)
    except Exception as error:
        print(f"error:{error}")
        sys.exit(1)


main()
