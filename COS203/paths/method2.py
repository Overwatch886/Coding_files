# Creating a pth using Path.home() and Path.cwd()
import pathlib
# We use this to get our current working directory
current_directory = pathlib.Path.cwd()
# We use this to get the home directory for this current user
home_directory = pathlib.Path.home()
print(current_directory)
print(home_directory)