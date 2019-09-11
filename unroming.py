#! /usr/bin/env python3
# coding: utf-8

import io, pickle
from tkinter import *
from PIL import ImageTk, Image
from roming import Rom
from time import time

IMAGE_HEIGHT = 200

root = Tk()
rom = Rom('super mario.raw')

# affichages des informations
Label(root, text=rom.title).pack(side='top')
Label(root, text=rom.year).pack(side='top')
Label(root, text=rom.players).pack(side='top')
Label(root, text=rom.developer).pack(side='top')
Label(root, text=rom.publisher).pack(side='top')

# jaquette
image = Image.open(io.BytesIO(rom.coverdata))
ratio = image.width / image.height
image = image.resize((int(IMAGE_HEIGHT*ratio), IMAGE_HEIGHT))
photoimg = ImageTk.PhotoImage(image)
cover = Label(root, image=photoimg)
cover.image = photoimg
cover.pack(side='bottom')

root.mainloop()