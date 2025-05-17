import os
import json

from construct import *
from PIL import Image

from .export_process import ExportProcess

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

def export_to_folder(root, *exporters):
	for exporter in exporters:
		for dirpath in exporter.dirs:
			dirpath_full = os.path.join(root, dirpath)
			os.makedirs(dirpath_full, exist_ok=True)

		exporter.export(root)

class ModelExporter(ExportProcess):
	def __init__(self, model):
		self.model = model
		self.model_name = self.model.ModelName.strip('\x00')
		self.texture_path = f'models/{self.model_name}/textures'

		self.path = os.path.join('models', f'{self.model_name}.bin')

		self.dirs = ('models', self.texture_path)

	def _export_metadata(self, root):
		filename = os.path.join('models', f'{self.model_name}', 'extra.json')
		metadata = {
			"PresenterName": self.model.PresenterName.strip('\x00'),
			"Location": self.model.Location,
			"Direction": self.model.Direction,
			"Up": self.model.Up,
			"Visibility": self.model.Visibility,
		}

		with open(os.path.join(root, filename), 'w') as fp:
			json.dump(metadata, fp, indent=4)

	def export(self, root):
		self._export_metadata(root)

		model_roi = ModelRoi.parse(self.model.ModelData)

		for texture in model_roi.TextureInfo.Textures:
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
				root,
				self.texture_path,
				texture.Name
			))

		exit(1)

class PartExporter(ExportProcess):
	def __init__(self, part):
		self.part = part
		self.path = os.path.join('parts', f'{self.part.RoiName.strip('\x00')}.bin')
		self.dirs = ('parts')

	def export(self, root):
		with open(self.path, 'wb') as fp:
			fp.write(self.path.PartData)

def export_world(export_path, world):
	root_path = os.path.join(export_path, 'WDB', world.WorldName.strip('\x00'))

	exporters = []
	for model in world.Models:
		exporters.append( ModelExporter(model) )

	for part in world.Parts:
		exporters.append( PartExporter(part) )

	export_to_folder(root_path, *exporters)
