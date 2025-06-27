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
		part = PartROIList.parse(self.part.Data)
		for roi in part.ROIs:
			lod = roi.LODs[0]
			for vert in lod.Vertices:
				print(f'v {vert[0]:.3f} {vert[1]:.3f} {vert[2]:.3f}')
		# print(part)
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
