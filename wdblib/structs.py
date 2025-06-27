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

from construct import *

MODEL_VERSION = 19
U16_MAX = 2**2

Vec2 = Array(2, Float32l)
Vec3 = Array(3, Float32l)

IVec3 = Array(3, Int32ul)

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

Mesh = Struct(
	"NumPolys"     / Int16ul,
	"NumVertices"  / Int16ul,
	"PolyIndices" / Array(this.NumPolys, IVec3),

	"NumTextureIndices" / Int16sl,
	"TextureIndices" / If(this.NumTextureIndices > 0, Array(this.NumPolys, IVec3)),

	# Mesh Metadata
	"Alpha"     / Float32l,
	"Shading"   / Int8ul,
	"m_unk0x0d" / Int8ul,
	"m_unk0x20" / undefined,
	"m_unk0x21" / Int8ul,

	# "TextureName"  / PascalString(Int32ul, "ascii"),
	# "MaterialName" / PascalString(Int32ul, "ascii"),
)

LOD = Struct(
	"m_unk0x08" / undefined4,
	"NumMeshes" / Int32ul,

	"NumVerts"   / Int16ul,
	"NumNormals" / ExprAdapter(
		Int16ul,
		(obj_+1) >> 1,
		obj_-1,
	),
	"NumUVMaps"  / Int16sl,

	"Vertices" / Array(this.NumVerts, Vec3),
	"Normals"  / If(this.NumNormals > 0, Array(this.NumNormals, Vec3)),
	"UVMaps"   / If(this.NumUVMaps  > 0, Array(this.NumUVMaps,  Vec2)),

	"Meshes" / Array(this.NumMeshes, Mesh),
)

WorldDbTexture = Struct(
	"Name"  / PascalString(Int32ul, "ascii"),
	"Image" / LegoImage
)

WorldDbTextureInfo = Struct(
	"NumTextures"  / Int32ul,
	# "SkipTextures" / Int32ul,

	"Textures" / Array(this.NumTextures, WorldDbTexture),
)

ROI = Struct(
	"RoiName" / PascalString(Int32ul, "ascii"),
	"NumLODs" / Int32ul,
	"RoiInfoOffset" / Int32ul,
	"LODs"    / Array(1, LOD),
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

ModelROIList = Struct(
	"Version" / Int32ul,
	"TextureInfoOffset" / Int32ul,

	"TextureInfo" / Pointer(this.TextureInfoOffset, WorldDbTextureInfo),

	"NumROIs" / Int32ul,
	"ROIs" / Array(this.NumROIs, ROI),
)




WorldDbPart = Struct(
	"RoiName"    / PascalString(Int32ul, "ascii"),
	"DataLength" / Int32ul,
	"DataOffset" / Int32ul,
	"Data"       / Pointer(this.DataOffset, Bytes(this.DataLength)),
)

PartROIList = Struct(
	"TextureInfoOffset" / Int32ul,

	"TextureInfo" / Pointer(this.TextureInfoOffset, WorldDbTextureInfo),

	"NumROIs" / Int32ul,
	"ROIs" / Array(this.NumROIs, ROI),
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
