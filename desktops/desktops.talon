os: windows
-

# Pull up Window's UI for displaying all
# open apps on the current virtual desktop,
# and thumbnails of all the other ones.
desks: key(win-tab)

# Open the start menu
launch: key(win)

# Focus by app and title keyword
focus <user.running_applications> [<user.text>]: user.focus_app_by_title(running_applications,text)