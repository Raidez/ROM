#! /usr/bin/env python3
# coding: utf-8

import pickle
from time import time
from pathlib import Path

class Platform:
	UNKNOW = 0
	SNES = 1

class Language:
	UNKNOW = 0
	FRA = 1

class Genre:
	UNKNOW = 0
	ACTION = 1
	ADVENTURE = 2
	FIGHTING = 3
	PLATFORM = 4
	PUZZLE = 5
	RACING = 6
	ROLE_PLAYING = 7
	SHOOTER = 8
	SIMULATION = 9
	SPORTS = 11
	STRATEGY = 12
	MISC = 13

class Rom:
	VERSION = 1

	def __init__(self, importfile=None):
		self.version = self.VERSION
		self.title = str()
		self.platform = Platform.UNKNOW
		self.year = int()
		self.language = Language.UNKNOW
		self.genres = list()
		self.players = int()
		self.developer = str()
		self.publisher = str()
		self.romsize = int()
		self.romdata = bytes()
		self.coversize = int()
		self.coverdata = bytes()
		self.extra = str()

		if importfile:
			self._import(importfile)

	def _import(self, importfile):
		with open(importfile, 'rb') as fs:
			self.version = int.from_bytes(fs.read(1), byteorder='big')
			self.title = fs.read(50).strip().decode('utf-8')
			self.platform = int.from_bytes(fs.read(1), byteorder='big')
			self.year = int.from_bytes(fs.read(2), byteorder='big')
			self.language = int.from_bytes(fs.read(1), byteorder='big')
			genres = fs.read(4).replace(Genre.UNKNOW.to_bytes(1, byteorder='big'), b'')
			for genre in genres:
				self.genres.append(genre)
			self.players = int.from_bytes(fs.read(1), byteorder='big')
			self.developer = fs.read(20).strip().decode('utf-8')
			self.publisher = fs.read(20).strip().decode('utf-8')
			self.romsize = int.from_bytes(fs.read(10), byteorder='big')
			self.romdata = fs.read(self.romsize)
			self.coversize = int.from_bytes(fs.read(10), byteorder='big')
			self.coverdata = fs.read(self.coversize)

	def append_rom(self, romfile):
		pathfile = Path(romfile)
		self.romsize = pathfile.stat().st_size
		self.romdata = pathfile.read_bytes()

	def append_cover(self, coverfile):
		pathfile = Path(coverfile)
		self.coversize = pathfile.stat().st_size
		self.coverdata = pathfile.read_bytes()

	def __bytes__(self):
		data = bytearray()

		## genres
		genres = bytearray()
		for i in range(4):
			try:
				genre = self.genres[i]
				genres.extend(genre.to_bytes(1, byteorder='big'))
			except:
				genres.extend(Genre.UNKNOW.to_bytes(1, byteorder='big'))

		## entête
		data.extend(self.version.to_bytes(1, byteorder='big'))
		data.extend(bytes(self.title, 'utf-8').rjust(50))
		data.extend(self.platform.to_bytes(1, byteorder='big'))
		data.extend(self.year.to_bytes(2, byteorder='big'))
		data.extend(self.language.to_bytes(1, byteorder='big'))
		data.extend(genres)
		data.extend(self.players.to_bytes(1, byteorder='big'))
		data.extend(bytes(self.developer, 'utf-8').rjust(20))
		data.extend(bytes(self.publisher, 'utf-8').rjust(20))

		## contenu de la rom & de la jaquette
		data.extend(self.romsize.to_bytes(10, byteorder='big'))
		data.extend(self.romdata)
		data.extend(self.coversize.to_bytes(10, byteorder='big'))
		data.extend(self.coverdata)

		## ajout d'information supplémentaire
		data.extend(bytes(self.extra, 'utf-8'))

		return bytes(data)


if __name__ == "__main__":
	rom = Rom()
	rom.title = "Super Mario World"
	rom.platform = Platform.SNES
	rom.year = 1991
	rom.language = Language.FRA
	rom.genres.append(Genre.PLATFORM)
	rom.players = 2
	rom.developer = "Nintendo"
	rom.publisher = "Nintendo"
	rom.append_rom('Super Mario World.smc')
	rom.append_cover('Super Mario World.png')

	with open('super mario.raw', 'wb') as fs:
		fs.write(bytes(rom))