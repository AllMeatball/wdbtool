import os
import json

from construct import *
from PIL import Image

Vec3 = Array(3, Float32l)
undefined = Byte
undefined2 = Int16sl
undefined4 = Int32sl

MODEL_VERSION = 19

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

ModelTexture = Struct(
	"Name"  / PascalString(Int32ul, "ascii"),
	"Image" / LegoImage
)

ModelTextureInfo = Struct(
	"NumTextures"  / Int32ul,
	"SkipTextures" / Int32ul,

	"Textures" / IfThenElse(
		this.SkipTextures != 1,
		Array(this.NumTextures, ModelTexture),
		Array(0, ModelTexture)
	),
)

ModelRoi = Struct(
	"Version" / Const(MODEL_VERSION, Int32ul),
	"TextureInfoOffset" / Int32ul,

	"TextureInfo" / Pointer(this.TextureInfoOffset, ModelTextureInfo),
)

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
	model_parse = ModelRoi.parse(model.ModelData)

	for texture in model_parse.TextureInfo.Textures:
		image_info = texture.Image
		palette = []

		for color in image_info.Palette:
			palette.append(color.Red)
			palette.append(color.Green)
			palette.append(color.Blue)

		im = Image.new('P', (image_info.Width, image_info.Height))
		im.putpalette(palette)

		for x in range(image_info.Width):
			for y in range(image_info.Height):
				index = image_info.Pixels[x + y * image_info.Width]
				im.putpixel( (x, y), index )

		im.save(os.path.join(
			'/tmp',
			texture.Name
		))

	exit(1)

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
