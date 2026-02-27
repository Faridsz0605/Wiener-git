import argparse
import json
import sys
import os
from pathlib import Path

#
# try:
#     import grp, pwd
# except ModuleNotFoundError:
#     pass


class Repo:
    def __init__(self, path=".") -> None:
        self.path = Path(
            path
        ).resolve()  # checks initialize a repo on working directory the method resolve() pass an absoulute path.

        ## "wigit" is same as .git folder. the following files will be the same as git/
        self.git_dir = self.path / ".wigit"

        self.obj_dir = self.git_dir / "objects"

        # refs for branch names and pointers to dirs
        self.refs_dir = self.git_dir / "refs"

        self.heads_dir = self.refs_dir / "heads"

        self.head_file = self.git_dir / "W_HEAD"

        self.index_file = self.git_dir / "index"

    def init(self) -> bool:
        if self.git_dir.exists():
            return False

        # creation of base dirs

        self.git_dir.mkdir()
        self.obj_dir.mkdir()
        self.refs_dir.mkdir()
        self.heads_dir.mkdir()

        # creation of initial HEAD (W_HEAD)
        self.head_file.write_text("refs: refs/heads/wiener-main\n")

        self.index_file.write_text(json.dumps({}, indent=2))

        print(f"initialize empty wiener-git repo in {self.git_dir}")
        return True


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

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "winit":
            repo = Repo()
            repo.init()
        if not repo.init():
            print("already on a wiener repo :)")
            return
    except Exception as error:
        print(f"error:{error}")
        sys.exit(1)


main()
