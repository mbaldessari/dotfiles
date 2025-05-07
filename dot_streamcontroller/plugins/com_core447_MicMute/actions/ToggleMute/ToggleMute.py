# Import StreamController modules
from GtkHelper.GtkHelper import ComboRow
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import pulsectl

class ToggleMute(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.has_configuration = True
        
    def get_mute_state(self, device_nick: str = None) -> bool:
        """
        device_nick: str if None all microphones will be checked
        Returns the mute state of the microphone. If the microphone is not found, returns None.
        """
        with pulsectl.Pulse('mute-microphone') as pulse:
            all_muted = True
            all_unmuted = True

            for source in pulse.source_list():
                # Get the mute state of the microphone
                muted = source.mute
                if muted:
                    all_unmuted = False
                else:
                    all_muted = False

                if device_nick is not None and source.proplist.get("device.nick") == device_nick:
                    return muted

            if all_muted:
                return True
            elif all_unmuted:
                return False
            else:
                return None
        
    def set_mute(self, state: bool, device_nick: str) -> None:
        """
        device_nick: str if None all microphones will be configured
        """
        with pulsectl.Pulse('mute-microphone') as pulse:
            for source in pulse.source_list():
                if device_nick is not None and source.proplist.get("device.nick") != device_nick:
                    continue
                pulse.source_mute(source.index, state)
        
    def show_state(self, device_nick: str) -> None:
        muted = self.get_mute_state(device_nick)
        if muted is None:
            self.show_error()
            return
        
        if muted:
            try:
                self.set_background_color(color=[255, 0, 0, 255])
            except AttributeError: # bug in 1.5.0-beta.5
                pass
            icon_name = "muted.png"
        else:
            try:
                self.set_background_color(color=[0, 0, 0, 0])
            except AttributeError: # bug in 1.5.0-beta.5
                pass
            icon_name = "unmuted.png"

        icon_path = os.path.join(self.plugin_base.PATH, "assets", icon_name)

        self.set_media(media_path=icon_path, size=0.75)

    def on_tick(self):
        settings = self.get_settings()
        nick = settings.get("device")
        is_all = settings.get("all")
        if is_all:
            nick = None
             
        self.show_state(nick)

    def on_ready(self):
        self.on_tick()

    def on_key_down(self):
        settings = self.get_settings()
        device_nick = settings.get("device")
        is_all = settings.get("all")
        print()
        if is_all in [None, False] and device_nick is None:
            self.show_error(2)
            return
        if is_all:
            device_nick = None

        mute = self.get_mute_state(device_nick)
        if mute is None:
            mute = False
        
        self.set_mute(not mute, device_nick)
        self.show_state(device_nick)

    def get_config_rows(self) -> list:
        self.device_model = Gtk.ListStore.new([str, bool]) # First Column: Name, Second Column: IsAll
        self.device_row = ComboRow(title=self.plugin_base.lm.get("actions.toggle-mute.device"), model=self.device_model)

        self.device_cell_renderer = Gtk.CellRendererText()
        self.device_row.combo_box.pack_start(self.device_cell_renderer, True)
        self.device_row.combo_box.add_attribute(self.device_cell_renderer, "text", 0)

        self.load_device_model()

        self.device_row.combo_box.connect("changed", self.on_device_change)

        self.load_config_settings()

        return [self.device_row]

    def load_device_model(self):
        self.device_model.clear()
        self.device_model.append([self.plugin_base.lm.get("actions.toggle-mute.all"), True])
        with pulsectl.Pulse('mute-microphone') as pulse:
            for source in pulse.source_list():
                self.device_model.append([source.proplist.get("device.nick"), False])

    def load_config_settings(self):
        settings = self.get_settings()
        nick = settings.get("device")
        is_all = settings.get("all")
        for i, device in enumerate(self.device_model):
            if device[0] == nick and not is_all:
                self.device_row.combo_box.set_active(i)
                break
            if device[1] and is_all:
                self.device_row.combo_box.set_active(i)
                break

    def on_device_change(self, combo_box, *args):
        name = self.device_model[combo_box.get_active()][0]
        is_all = self.device_model[combo_box.get_active()][1]

        settings = self.get_settings()
        if is_all:
            settings["all"] = True
            settings["device"] = None
        else:
            settings["all"] = False
            settings["device"] = name

        self.set_settings(settings)