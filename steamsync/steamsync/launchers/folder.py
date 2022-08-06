#! /usr/bin/env python

# LICENSE: AGPLv3. See LICENSE at root of repo

import pprint
from pathlib import Path

import steamsync.defs as defs
import steamsync.launchers.launcher as launcher


class FolderLauncher(launcher.Launcher):
    def __init__(self, path_to_library, path_to_exe, args_fmt, glob, tag):
        self.path_to_library = Path(path_to_library)
        self.path_to_exe = Path(path_to_exe) if path_to_exe else None
        self.args_fmt = args_fmt
        self.glob = glob
        self.tag = tag

    def collect_games(self) -> list[defs.GameDefinition]:
        """Add files in the given path to steam library as shortcuts that run the
        given exe.

        collect_games() -> list(defs.GameDefinition)
        """
        working_dir = self.path_to_library.as_posix()
        print(f"\nScanning folder ({working_dir})...")
        games = []
        exe = self.path_to_exe and self.path_to_exe.as_posix() or None
        for file in self.path_to_library.glob(self.glob or "*"):
            file_str = str(file)
            game_def = defs.GameDefinition(
                exe or file_str,
                file.stem,
                file.stem,
                working_dir,
                self.args_fmt.format(file_str),
                None,
                self.tag,
            )
            games.append(game_def)
        if not games:
            print("Failed to find any files")

        print(f"Collected {len(games)} games from the input folder")
        games.sort()
        return games

    def get_store_id(self) -> str:
        return defs.TAG_FOLDER

    def get_display_name(self) -> str:
        if self.path_to_exe:
            return f"{self.path_to_exe.name} Launcher for Folder"
        else:
            return "Launcher for Games in Folder"

    def is_installed(self) -> bool:
        return self.path_to_library.is_dir()


def test():
    # Launch unpacked love2d game folders with love executable.
    fold = FolderLauncher(
        path_to_library="C:/scratch/love",
        path_to_exe="love.exe",
        args_fmt="{}",
        glob="*/",
        tag="love",
    )
    games = fold.collect_games()
    print(fold.get_display_name())
    pprint.pprint(
        [
            (
                g.app_name,
                g.executable_path,
                g.launch_arguments,
            )
            for g in games
        ]
    )


if __name__ == "__main__":
    test()
