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

	"PresenterNameLen" / PascalString(Int32ul, "ascii"),
	"Location"         / Vec3,
	"Direction"        / Vec3,
	"Up"               / Vec3,
	'm_unk0x34'        / undefined,
)



ModelDbPart = Struct(
	"RoiName"        / PascalString(Int32ul, "ascii"),
	"PartDataLength" / undefined4,
	"PartDataOffset" / undefined4,
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
