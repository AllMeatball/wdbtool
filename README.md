# WDBTool - A tool for messing with Lego Island's .WDB format

## Prerequisites
* Python 3.x
* [Construct](https://construct.readthedocs.io/en/latest/index.html)

## Installation
1. Download [lastest Python 3](https://www.python.org/downloads/)
2. Install construct:

   with pip and a python virtual environment
   ```sh
   # in the repo directory
   python -m venv env
   python -m pip install construct
   ```
   or with a package manager
   ```sh
   # Arch Linux
   sudo pacman -S python-construct

   # Debian/Ubuntu
   sudo apt-get install python3-construct

   # Fedora
   sudo dnf install python3-construct
   ```

## Running
You should be able to run the script like this in a terminal:

`python wdbtool.py [wdb_path]`

## Acknowledgments
* This uses some structs based off of the [Lego Island Decomp Project](https://github.com/isledecomp/isle)
