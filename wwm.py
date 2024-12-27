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
        

def run(self):
    """
    Setup and run window manager. This includes checking if another window manager is
    running, listening for certain key presses, and handling events.
    """

    # Tell X server which events we wish to receive for the root window.
    cookie = self.conn.core.ChangeWindowAttributesChecked(
        self.root_window,
        xcffib.xproto.CW.EventMask,  # Window attribute to set which events we want
        [
            # We want to receive any substructure changes. This includes window
            # creation/deletion, resizes, etc.
            xcffib.xproto.EventMask.SubstructureNotify |
            # We want X server to redirect children substructure notifications to the
            # root window. Our window manager then processes these notifications.
            # Only a single X client can use SubstructureRedirect at a time.
            # This means if the request to changes attributes fails, another window manager
            # is probably running.
            xcffib.xproto.EventMask.SubstructureRedirect,
        ]
    )

    # Check if request was valid
    try:
        cookie.check()
    except:
        logging.error(logging.traceback.format_exc())
        print('Is another window manager running?')
        exit()

    # Loop through actions listed in config and grab keys. This means we
    # will get a KeyPressEvent if the key combination is pressed.
    for action in self.config['actions']:
        # Get keycode from string
        keycode = self.key_util.get_keycode(
            KeyUtil.string_to_keysym(action['key'])
        )

        # Get modifier from string
        modifier = getattr(xcffib.xproto.KeyButMask, self.config['modifier'], 0)

        self.conn.core.GrabKeyChecked(
            # We want owner_events to be false so all key events are sent to root window
            False,
            self.root_window,
            modifier,
            keycode,
            xcffib.xproto.GrabMode.Async,
            xcffib.xproto.GrabMode.Async
        ).check()

    while True:
        event = self.conn.wait_for_event()

        if isinstance(event, xcffib.xproto.KeyPressEvent):
            self._handle_key_press_event(event)
        if isinstance(event, xcffib.xproto.MapRequestEvent):
            self._handle_map_request_event(event)
        if isinstance(event, xcffib.xproto.ConfigureRequestEvent):
            self._handle_configure_request_event(event)

        # Flush requests to send to X server
        self.conn.flush()



