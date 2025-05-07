from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

import os
from PIL import Image, ImageEnhance

class MoveRight(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_state = -1

        self.icon_path = os.path.join(self.plugin_base.PATH, "assets", "navigate_next.png")

    def on_ready(self):
        self.show_state(0)
        self.current_state = -1 # Allow the first tick to update the state

    def on_tick(self):
        start_index = self.plugin_base.start_index

        if start_index > 0: # -1 because we want to ignore the first column containing the navigation keys
            # Show that we can go right
            self.show_state(1)
        else:
            # Show that we can't go right
            self.show_state(0)

    def on_key_down(self):
        self.on_tick()

        if self.current_state == 0:
            return
        # Change start_index
        self.plugin_base.start_index = max(0, self.plugin_base.start_index - 1)

        for action in self.plugin_base.volume_actions:
            if action == self:
                continue
            action.on_tick()

    def show_state(self, state):
        """
        0: Greyed out
        1: Can go right
        """
        # Don't do anything if the state hasn't changed
        if state == self.current_state:
            return
        self.current_state = state
        if state == 0:
            with Image.open(self.icon_path) as image:
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(0.65)
                self.set_media(image=image.copy())
            self.set_media(image=image)
        elif state == 1:
            self.set_media(media_path=self.icon_path)