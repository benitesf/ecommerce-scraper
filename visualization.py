#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 15:50:00 2021

@author: joker
"""

import os
import datetime
import pandas as pd
import _pickle as pkl
import seaborn as sns

import common

data = []
filename = os.path.join(os.getcwd(), "data", "raw", "MPE1246_17-01-2021.data")
with open(filename, "rb") as fr:
    try:
        while True:
            data.append(pkl.load(fr))
    except EOFError:
        pass
    
cols = ["item_name", "item_id", "item_price", "local_item_price",
        "available_stock", "sold_stock", "brand", "model", "condition",
        "root_category", "path_to_root", "seller_id", "location", "seller_type",
        "reputation_level", "seller_status", "customer_satisfaction", "seller_age",
        "sales_completed", "link"]

df = pd.DataFrame()

for chunk in data:
    for row in chunk:
        item_name = row["item_name"]
        item_id = row["item_id"]
        item_price = row["item_price"]
        local_item_price = row["local_item_price"]
        available_stock = row["available_stock"]
        sold_stock = row["sold_stock"]
        brand = row["brand"]
        model = row["model"]
        condition = row["item_condition"]
        root_category = row["root_category"]
        path_to_root = row["path_to_root"]
        seller_id = row["seller_id"]
        location = row["location"]
        seller_type = row["seller_type"]
        reputation_level = row["reputation_level"]
        seller_status = row["seller_status"]
        customer_satisfaction = row["customer_satisfaction"]
        seller_age = row["seller_age"]
        sales_completed = row["sales_completed"]
        link = row["link"]
        
        s = pd.Series([item_name, item_id, item_price, local_item_price, available_stock,
                       sold_stock, brand, model, condition, root_category, path_to_root,
                       seller_id, location, seller_type, reputation_level, seller_status,
                       customer_satisfaction, seller_age, sales_completed, link])
        row_df = pd.DataFrame([s])
        df = pd.concat([row_df, df], ignore_index=True)
        
df.columns = cols
