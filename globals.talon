# Since global hotkeys will often be user and/or
# environment-specific, if the following hotkeys
# are desired then this file can be copied to
# a location outside the repo (e.g. in `talon/user`)
# and edited as needed.

# #Hotkey to toggle talon being awake or not
# key(ctrl-alt-space):speech.toggle()
# 
# # Hotkey to sleep Talon (matches hotkey to toggle # Discord)
# key(ctrl-alt-f15): speech.disable()
mode: all
-
wake:
  speech.enable()