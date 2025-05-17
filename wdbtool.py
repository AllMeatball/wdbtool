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

import os
import json
import argparse
from construct import *

Vec3 = Array(3, Float32l)
undefined = Byte
undefined2 = Int16sl
undefined4 = Int32sl

ModelDbModel = Struct(
	"ModelName"       / PascalString(Int32ul, "ascii"),

	"ModelDataLength" / Int32ul,
	"ModelDataOffset" / Int32ul,
	"ModelData"       / Pointer(this.ModelDataOffset, Bytes(this.ModelDataLength)),

	"PresenterName"    / PascalString(Int32ul, "ascii"),
	"Location"         / Vec3,
	"Direction"        / Vec3,
	"Up"               / Vec3,
	"Visibility"       / Flag,
)



ModelDbPart = Struct(
	"RoiName"        / PascalString(Int32ul, "ascii"),
	"PartDataLength" / undefined4,
	"PartDataOffset" / undefined4,
	"PartData"       / Pointer(this.PartDataOffset, Bytes(this.PartDataLength)),
)

ModelDbWorld = Struct(
	"WorldName"    / PascalString(Int32sl, "ascii"),

	"NumParts"     / Int32sl,
	"Parts"        / Array(this.NumParts, ModelDbPart),

	"NumModels"    / Int32ul,
	"Models"       / Array(this.NumModels, ModelDbModel),

	# "m_unk0x34"    / Array(0x08, undefined),
)

WorldDbFile = Struct(
	"NumWorlds" / Int32sl,
	"Worlds"    / Array(this.NumWorlds, ModelDbWorld),
)

def export_to_folder(root, filename, data):
	fullpath = os.path.join(root, filename)
	fullpath_dir = os.path.dirname(fullpath)

	os.makedirs(fullpath_dir, exist_ok=True)

	with open(fullpath, 'wb') as fp:
		fp.write(data)

def export_part(part):
	filename = part.RoiName.strip('\x00')+'.bin'
	path = os.path.join('parts', filename)

	return path, part.PartData

def export_model(model):
	filename = model.ModelName.strip('\x00')+'.bin'
	path = os.path.join('models', filename)

	return path, model.ModelData

def export_model_metadata(model):
	filename = model.ModelName.strip('\x00')+'.json'
	path = os.path.join('models', filename)

	metadata = {
		"PresenterName": model.PresenterName.strip('\x00'),
		"Location": model.Location,
		"Direction": model.Direction,
		"Up": model.Up,
		"Visibility": model.Visibility,
	}

	return path, json.dumps(metadata, indent=4).encode('utf-8')

def export_world(export_path, world):
	root_path = os.path.join(export_path, 'WDB', world.WorldName.strip('\x00'))

	for model in world.Models:
		filename, data = export_model(model)
		export_to_folder( root_path, filename, data )

		# export metadata
		filename, data = export_model_metadata(model)
		export_to_folder( root_path, filename, data )


	for part in world.Parts:
		filename, data = export_part(part)
		export_to_folder( root_path, filename, data )

# List all data in the .WDB file
def ACTION_list(args):
	wdb = WorldDbFile.parse_file(args.filename)
	print(wdb)


# Export data to .json and .bin files (creates a WDB path in the target folder)
def ACTION_export(args):
	assert(args.output)
	wdb = WorldDbFile.parse_file(args.filename)

	for world in wdb.Worlds:
		export_world(args.output, world)

# List all world names
def ACTION_world_names(args):
	wdb = WorldDbFile.parse_file(args.filename)

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

