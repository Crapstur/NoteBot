#! /usr/bin/env python3

import PIL
import os
import logging
import numpy as np
import datetime

from PIL import Image
from pdf2image import convert_from_path

def ft_crop(image_path, left, top, width, height):
        
    image = Image.open(image_path)

    box = (left, top, left+width, top+height)

    area = image.crop(box)

    area.save(image_path, "PNG")

try:
    logging.basicConfig(filename='/var/log/NOTEBot/convertpdf.log', level=logging.INFO)
    logging.warning(str(datetime.datetime.today()) + ' : convertpdf START')

    notes_file = "./notes/"
    tmp_file = "./tmp/"
    
    if not os.path.exists(tmp_file):
        os.mkdir(tmp_file)
        logging.info(str(datetime.datetime.today()) + ' : Create folder [\"./tmp\"]')
    
    eleves = os.listdir(notes_file)
    
    for eleve in eleves:
        
        eleve_notes_file = notes_file + eleve
        eleve_tmp_file = tmp_file + eleve
        
        if not os.path.exists(eleve_tmp_file):
            os.mkdir(eleve_tmp_file)
            logging.info(str(datetime.datetime.today()) + ' : Create folder [\"' + eleve_tmp_file + '\"]')
            
        bulletins = os.listdir(eleve_notes_file)
        
        for bulletin in bulletins:
            bulletin_notes_file = eleve_notes_file + "/" + bulletin
            bulletin_tmp_file = eleve_tmp_file + "/" + bulletin

            if not os.path.exists(bulletin_tmp_file):
                os.mkdir(bulletin_tmp_file)
                logging.info(str(datetime.datetime.today()) + ' : Create folder [\"' + bulletin_tmp_file + '\"]')

            images = convert_from_path(bulletin_notes_file)
            for i in range(len(images)):
                image_path = bulletin_tmp_file + '/page'+ str(i+1) +'.jpg'
                images[i].save(image_path, 'JPEG')
                if i == 0:
                    ft_crop(image_path, 0, 450, 1654, 1750)
                else:
                    ft_crop(image_path, 0, 0, 1654, 2250)
            logging.info(str(datetime.datetime.today()) + ' : Bullettin : [\"' + bulletin + '\"] de [\"' + eleve + '\"] convertit')
except:
    pass

logging.warning(str(datetime.datetime.today()) + ' : convertpdf STOP')