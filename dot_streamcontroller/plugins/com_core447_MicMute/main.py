# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport

# Import actions
from .actions.ToggleMute.ToggleMute import ToggleMute

class MicMutePlugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.lm = self.locale_manager

        ## Register actions
        self.toggle_mute_holder = ActionHolder(
            plugin_base = self,
            action_base = ToggleMute,
            action_id_suffix = "ToggleMute", # Change this to your own plugin id
            action_name = self.lm.get("actions.toggle-mute.name"),
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.SUPPORTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.toggle_mute_holder)

        # Register plugin
        self.register(
            plugin_name = self.lm.get("plugin.name"),
            github_repo = "https://github.com/StreamController/MicMute",
            plugin_version = "1.0.0",
            app_version = "1.2.0-alpha"
        )