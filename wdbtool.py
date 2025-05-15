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
from construct import *

parser = argparse.ArgumentParser()
parser.add_argument('wdb_path')
args = parser.parse_args()

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
	'm_unk0x34'        / undefined,
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
	"PartList"     / Array(this.NumParts, ModelDbPart),

	"NumModels"    / Int32ul,
	"Models"       / Array(this.NumModels, ModelDbModel),

	# "m_unk0x34"    / Array(0x08, undefined),
)

ModelDbFile = Struct(
	"NumWorlds" / Int32sl,
	"Worlds"    / Array(this.NumWorlds, ModelDbWorld),
)

result = ModelDbFile.parse_file(args.wdb_path)
print(result.Worlds)
