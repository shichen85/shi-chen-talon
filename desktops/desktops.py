from talon import Context, Module, actions

mod = Module()
desktop_max_setting = mod.setting(
    "desktop_count_max",
    type=int,
    default=4,
    desc="Windows does not have hotkeys to go to specific desktops, so we need a hack based on the total number of desktops. This number must be >= the number of desktops in your setup.",
)

ctx = Context()
ctx.matches = r"""
os: windows
"""


@ctx.action_class("user")
class Actions:
    def desktop(number: int):
        # Go all the way left
        for i in range(desktop_max_setting.get()):
            actions.key("ctrl-win-left")
        if number > 1:
            for i in range(1, number):
                actions.key("ctrl-win-right")
