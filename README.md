# multipackage-pyispec

This is script is inspired by the [tutorial](https://www.zacoding.com/en/post/pyinstaller-create-multiple-executables/) written by [Zao Coding](https://www.zacoding.com/en/about/).

## Usage

```python
# This is the top part of the script.
...
# ----------------- Global variable -----------------
# Fill project name here. This will also be the name of 
# the folder's name that contains your application.
PROJECT_NAME = "<Your_Project_name>" 

# List your applications' source code here. Each item is
# corresponding to a executable file in outputted folder
src_file_paths = [
    ## For example:
    # "./say_hi.py",
    # "./main.py",
    # "./say_fvck.py"
]
# ----------------- Global variable -----------------
...
```

```python
# Output necessary spec file.
python generate_spec.py
# Packaging application with PyInstaller.
pyinstaller ./<Your_Project_Name>
```
