#!/usr/bin/env python
# coding: utf8
from gluon import *
import os
try:
    from PIL import Image, ImageOps
except ImportError:
    import Image
    import ImageOps

def thumbnail(ruta):
    img_enlaces=ruta
    image = Image.open(img_enlaces)

    # ImageOps compatible mode
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
    image.thumbnail((1000,800), Image.ANTIALIAS)
    extension = img_enlaces.split('.')[-1]
    if extension.lower()=="JPG" or extension.lower()=="JPEG":
        result = image.save(img_enlaces, 'JPEG', quality=75)
    else:
        result = image.save(img_enlaces, 'PNG', quality=75)
