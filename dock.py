#!/usr/bin/env python3
import gi
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="System Panel")
        self.set_border_width(10)
        self.set_default_size(400, 400)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        label = Gtk.Label(label="Installed Applications:")
        box.pack_start(label, False, False, 0)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        box.pack_start(scrolled_window, True, True, 0)

        app_list_store = Gtk.ListStore(str)
        tree_view = Gtk.TreeView(model=app_list_store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Applications", renderer, text=0)
        tree_view.append_column(column)
        scrolled_window.add(tree_view)

        self.load_applications(app_list_store)

    def load_applications(self, store):
        try:
            result = subprocess.run(['xdg-desktop-menu', 'list'], capture_output=True, text=True, check=True)
            apps = result.stdout.splitlines()
            for app in apps:
                store.append([app])
        except subprocess.CalledProcessError as e:
            print(f"Error listing applications: {e}")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
