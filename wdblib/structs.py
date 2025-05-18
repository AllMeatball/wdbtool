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

from construct import *

MODEL_VERSION = 19

Vec3 = Array(3, Float32l)
undefined = Byte
undefined2 = Int16sl
undefined4 = Int32sl

RGBColor = Struct(
	"Red"   / Int8ul,
	"Green" / Int8ul,
	"Blue"  / Int8ul,
)

LegoImage = Struct(
	"Width"  / Int32ul,
	"Height" / Int32ul,

	"ColorCount" / Int32ul,
	"Palette"    / Array(this.ColorCount, RGBColor),

	"Pixels"     / Bytes(this.Width * this.Height),
)

WorldDbTexture = Struct(
	"Name"  / PascalString(Int32ul, "ascii"),
	"Image" / LegoImage
)

WorldDbTextureInfo = Struct(
	"NumTextures"  / Int32ul,
	"SkipTextures" / Int32ul,

	"Textures" / IfThenElse(
		this.SkipTextures != 1,
		Array(this.NumTextures, WorldDbTexture),
		Array(0, WorldDbTexture)
	),
)

ROI = Struct(
	"RoiName" / PascalString(Int32ul, "ascii"),
	"NumLODs" / Int32ul,
	"LODs" / Int32ul
)

ModelROIList = Struct(
	"Version" / Int32ul,
	"TextureInfoOffset" / Int32ul,

	"TextureInfo" / Pointer(this.TextureInfoOffset, WorldDbTextureInfo),

	"NumROIs" / Int32ul,
	"ROIs" / Array(this.NumROIs, ROI),
)

WorldDbModel = Struct(
	"Name" / PascalString(Int32ul, "ascii"),

	"DataLength" / Int32ul,
	"DataOffset" / Int32ul,
	"Data"       / Pointer(this.DataOffset, Bytes(this.DataLength)),

	"PresenterName"    / PascalString(Int32ul, "ascii"),
	"Location"         / Vec3,
	"Direction"        / Vec3,
	"Up"               / Vec3,
	"Visibility"       / Flag,
)

WorldDbPart = Struct(
	"RoiName"    / PascalString(Int32ul, "ascii"),
	"DataLength" / Int32ul,
	"DataOffset" / Int32ul,
	"Data"       / Pointer(this.DataOffset, Bytes(this.DataLength)),
)

WorldDbWorld = Struct(
	"Name" / PascalString(Int32sl, "ascii"),

	"NumParts"     / Int32sl,
	"Parts"        / Array(this.NumParts, WorldDbPart),

	"NumModels"    / Int32ul,
	"Models"       / Array(this.NumModels, WorldDbModel),

	# "m_unk0x34"    / Array(0x08, undefined),
)

WorldDbFile = Struct(
	"NumWorlds" / Int32sl,
	"Worlds"    / Array(this.NumWorlds, WorldDbWorld),
)
