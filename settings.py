#!/usr/bin/env python3
import gi
import subprocess
import os
from gi.repository import Gtk

gi.require_version("Gtk", "3.0")

class SettingsApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Settings")
        self.set_border_width(10)
        self.set_default_size(400, 300)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.create_wallpaper_section()
        self.create_audio_server_section()

    def create_wallpaper_section(self):
        label = Gtk.Label(label="Change Wallpaper:")
        self.grid.attach(label, 0, 0, 1, 1)

        self.wallpaper_entry = Gtk.Entry()
        self.grid.attach(self.wallpaper_entry, 1, 0, 1, 1)

        browse_button = Gtk.Button(label="Browse")
        browse_button.connect("clicked", self.on_browse_clicked)
        self.grid.attach(browse_button, 2, 0, 1, 1)

        apply_wallpaper_button = Gtk.Button(label="Apply")
        apply_wallpaper_button.connect("clicked", self.on_apply_wallpaper_clicked)
        self.grid.attach(apply_wallpaper_button, 3, 0, 1, 1)

    def create_audio_server_section(self):
        label = Gtk.Label(label="Change Audio Server:")
        self.grid.attach(label, 0, 1, 1, 1)

        self.audio_server_combo = Gtk.ComboBoxText()
        self.audio_server_combo.append_text("PulseAudio")
        self.audio_server_combo.append_text("Other Audio Server")
        self.audio_server_combo.set_active(0)
        self.grid.attach(self.audio_server_combo, 1, 1, 2, 1)

        apply_audio_button = Gtk.Button(label="Apply")
        apply_audio_button.connect("clicked", self.on_apply_audio_clicked)
        self.grid.attach(apply_audio_button, 3, 1, 1, 1)

    def on_browse_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Choose a wallpaper", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Images")
        filter_text.add_mime_type("image/png")
        filter_text.add_mime_type("image/jpeg")
        dialog.add_filter(filter_text)

        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            self.wallpaper_entry.set_text(dialog.get_filename())
        dialog.destroy()

    def on_apply_wallpaper_clicked(self, widget):
        wallpaper_path = self.wallpaper_entry.get_text()
        if os.path.exists(wallpaper_path):
            subprocess.run(['feh', '--bg-scale', wallpaper_path])
        else:
            self.show_error_message("File not found", "The specified wallpaper file does not exist.")

    def on_apply_audio_clicked(self, widget):
        selected_audio_server = self.audio_server_combo.get_active_text()
        if selected_audio_server == "PulseAudio":
            subprocess.run(['pactl', 'load-module', 'module-pulse'])
        else:
            self.show_error_message("Unsupported Audio Server", "Only PulseAudio is supported in this example.")

    def show_error_message(self, title, message):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

win = SettingsApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
