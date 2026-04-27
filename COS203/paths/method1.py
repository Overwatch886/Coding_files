# Creating a path from a string
import pathlib
# We can write it like this
path1 = pathlib.Path(r"C:\developer\Coding_files\COS203\paths")
# or like this
path2 = pathlib.Path("C:/developer/Coding_files/COS203/paths")
print(path1)
print(path2)