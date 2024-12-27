# Whisker Window Manager - 2024 licensed by GNU general public license v3.0


from pwm.utils import KeyUtil
import logging
import subprocess
import xcffib
import xcffib.xproto
import yaml


# Constants to use in window manager
NEXT_WINDOW = 'NEXT_WINDOW'
PREVIOUS_WINDOW = 'PREVIOUS_WINDOW'


class WindowManager:
    def __init__(self):
        # Load config file. This should be moved into ~/.config/ and be read from there.
        with open('config.yaml') as f:
            self.config = yaml.safe_load(f)

        # Connect to X server. Since we don't specify params it will connect to display 1
        # that was set in preview.sh.
        self.conn = xcffib.connect()

        # Class that contains utils for switching between keycodes/keysyms
        self.key_util = KeyUtil(self.conn)

        # Get first available screen
        self.screen = self.conn.get_setup().roots[0]

        # All windows have a parent, the root window is the final parent of the tree of windows.
        # It is created when a screen is added to the X server. It is used for background images
        # and colors. It also can receive events that happen to its children such as mouse in/out,
        # window creation/deletion, etc.
        self.root_window = self.screen.root

        # An array of windows
        self.windows = []
        self.current_window = 0

