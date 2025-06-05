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

from PIL import Image

from .export_process import ExportProcess
from .structs import *

def export_to_folder(root, *exporters):
	for exporter in exporters:
		for dirpath in exporter.dirs:
			dirpath_full = os.path.join(root, dirpath)
			os.makedirs(dirpath_full, exist_ok=True)

		exporter.export(root)

def write_lego_image(lego_image: LegoImage, path: str):
	palette = []

	for color in lego_image.Palette:
		palette.append(color.Red)
		palette.append(color.Green)
		palette.append(color.Blue)

	im = Image.new('P', (lego_image.Width, lego_image.Height))
	im.putpalette(palette)

	for x in range(lego_image.Width):
		for y in range(lego_image.Height):
			index = lego_image.Pixels[x + y * lego_image.Width]
			im.putpixel( (x, y), index )

	im.save(path)

class ModelExporter(ExportProcess):
	def __init__(self, model):
		self.model = model
		self.model_name = self.model.Name.strip('\x00')
		self.texture_path = f'models/{self.model_name}/textures'

		self.path = os.path.join('models', f'{self.model_name}.bin')

		self.dirs = ['models', self.texture_path]

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

		model_roi = ModelROIList.parse(self.model.Data)

		for texture in model_roi.TextureInfo.Textures:
			write_lego_image(texture.Image, os.path.join(
					root,
					self.texture_path,
					texture.Name
				)
			)

		# exit(1)

class PartExporter(ExportProcess):
	def __init__(self, part):
		self.part = part
		self.path = os.path.join('parts', f'{self.part.RoiName.strip('\x00')}.bin')
		self.dirs = ['parts']

	def export(self, root):
		part_roi = PartROIList.parse(self.part.Data)
		print(part_roi)
		exit(1)

		# with open(os.path.join(root, self.path), 'wb') as fp:
		# 	fp.write(self.part.PartData)

def export_world(export_path, world):
	root_path = os.path.join(export_path, 'WDB', world.Name.strip('\x00'))

	exporters = []
	# for model in world.Models:
	# 	exporters.append( ModelExporter(model) )

	for part in world.Parts:
		exporters.append( PartExporter(part) )

	export_to_folder(root_path, *exporters)
