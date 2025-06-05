# MIT License
#
# Copyright (c) 2025 AllMeatball
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse

import wdblib

# List all data in the .WDB file
def ACTION_list(args):
	wdb = wdblib.WorldDbFile.parse_file(args.filename)
	print(wdb)


# Export data to .json and .bin files (creates a WDB path in the target folder)
def ACTION_export(args):
	assert(args.output)
	wdb = wdblib.WorldDbFile.parse_file(args.filename)

	for world in wdb.Worlds:
		wdblib.export_world(args.output, world)

# List all world names
def ACTION_world_names(args):
	wdb = wdblib.WorldDbFile.parse_file(args.filename)

	for world in wdb.Worlds:
		print(world.WorldName)

ACTIONS = {
	'list': ACTION_list,
	'export': ACTION_export,
	'world-names': ACTION_world_names,
}

parser = argparse.ArgumentParser()
parser.add_argument('action', help='Allowed actions: ' + ', '.join(ACTIONS))
parser.add_argument('-o', '--output', help='Output path for export')
parser.add_argument('filename')
args = parser.parse_args()

assert(args.action in ACTIONS)
ACTIONS[args.action](args)

