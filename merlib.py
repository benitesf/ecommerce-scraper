#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:49:26 2020

@author: joker
"""

import datetime
import logging
import os

from spider import MerlibSpider

logging.basicConfig(level=logging.INFO)
    
category_fpath = "data/raw/category.pkl"
mls = MerlibSpider()
#cat = mls.get_categories()
mls.load_categories(category_fpath)
keys = ["MPE1246"]

outdir = os.path.join(os.getcwd(), "data", "raw")
if not os.path.exists(outdir):
    os.makedirs(outdir)

date = datetime.datetime.now().strftime("%d-%m-%Y")
filename = os.path.join(outdir, f"MPE1246_{date}.data")

with open(filename, 'ab+') as fp:
    mls.extract_items_info(fp, keys=keys, all_keys=False)


"""
if __name__ == "__main__":
    
"""      