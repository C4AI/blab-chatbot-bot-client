#!/usr/bin/env python3

"""This script can be used to run the main module."""

from pathlib import Path
from runpy import run_path
from sys import path

MODULE = "blab_chatbot_bot_client"

src_dir = Path(__file__).parent.resolve() / "src"
path.insert(0, str(src_dir))
run_path(str(src_dir / MODULE))
