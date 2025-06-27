# GNU Lesser Public License v3
# Copyright (C) 2025 AllMeatball
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
		print(world.Name)

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

