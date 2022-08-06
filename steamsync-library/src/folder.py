#! /usr/bin/env python

# LICENSE: AGPLv3. See LICENSE at root of repo

import gzip
import json
from pathlib import Path

import toml

import defs
import util


def folder_collect_games(path_to_library, path_to_exe, args_fmt, glob, tag):
    """Add files in the given path to steam library as shortcuts that run the
    given exe.

    folder_collect_games(str, str, str, str) -> list(defs.GameDefinition)
    """
    print(f"\nScanning folder ({path_to_library})...")
    root = Path(path_to_library)
    games = []
    exe = path_to_exe and str(path_to_exe) or None
    working_dir = str(path_to_library)
    for file in root.glob(glob or "*"):
        file_str = str(file)
        game_def = defs.GameDefinition(
            exe or file_str,
            file.stem,
            file.stem,
            working_dir,
            args_fmt.format(file_str),
            None,
            tag,
        )
        games.append(game_def)
    if not games:
        print("Failed to find any files")

    print(f"Collected {len(games)} games from the input folder")
    games.sort()
    return games


def test():
    import os
    import pprint

    games = folder_collect_games(
        # Launch unpacked love2d game folders with love executable.
        "C:/scratch/love",
        "love.exe",
        "{}",
        "*/",
        "love",
    )
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
