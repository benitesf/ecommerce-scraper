#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 18:49:26 2020

@author: joker
"""

import logging

from spider import MerlibSpider

logging.basicConfig(level=logging.INFO)
    
category_fpath = "data/raw/category.pkl"
mls = MerlibSpider()
#cat = mls.get_categories()
mls.load_categories(category_fpath)
cat = mls.categories
mls.extract_items_info(all_keys=True)
"""
i`f __name__ == "__main__":
    
"""      