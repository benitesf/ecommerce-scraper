#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 15:54:43 2021

@author: joker
"""

import re
import common
import logging

class MerlibSpider:
    
    root = "https://www.mercadolibre.com.pe"
    url = {
        "category": root + "/categorias"
        }
    patt = {
        "cat_id": re.compile(r"c_category_id=(.*?)&"),
        "child_cat_id": re.compile(r"CATEGORY_ID=(.*?)&"),
        "item_id": re.compile(r"\"item_id\":\"(.*?)\","),
        "item_name": re.compile(r"\"item_name\":\"(.*?)\""),
        "item_price": re.compile(r"\"itemPrice\":(.*?),"),
        "local_item_price": re.compile(r"\"localItemPrice\":(.*?),"),
        "available_stock": re.compile(r"\"availableStock\":(.*?),"),
        "sold_stock": re.compile(r"\"soldStock\":(.*?),"),
        "brand": re.compile(r"\"brand\":\"(.*?)\""),
        "model": re.compile(r"\"model\":\"(.*?)\""),
        "item_condition": re.compile(r"\"item_condition\":\"(.*?)\""),
        "root_category": re.compile(r"\"rootCategoryId\":\"(.*?)\""),
        "path_to_root": re.compile(r"\"pathToRoot\":\"(.*?)\""),
        "seller_id": re.compile(r"\"seller_id\":(.*?),"),
        "seller_type": re.compile(r"\"seller_type\":\"(.*?)\""),
        "reputation_level": re.compile(r"\"reputation_level\":\"(.*?)\""),
        "seller_status": re.compile(r"\"power_seller_status\":\"(.*?)\""),
        "customer_satisfaction": re.compile(r"\"thermometer\":\{\"rank\":\d,\"info\":\[\{\"title\":\"(.*?)\","),
        "seller_age": re.compile(r"\"thermometer\":\{\"rank\":\d,\"info\":\[\{.+?\},\{\"title\":\"(.*?)\","),
        "sales_completed": re.compile(r"\"thermometer\":\{\"rank\":\d,\"info\":\[\{.+?\},\{.+?\},\{\"title\":\"(.*?)\","),
        }
    
    categories = None
    
    def __init__(self):
        logging.info("Initialized merlibspider...")
    
    def load_categories(self, fpath):
        logging.info("Loading categories")
        self.categories = common.load_pickle(fpath)
            
    def get_categories(self, save_path="", cache=True):
        """
        Find categories and return a dictionary with each category information
        """
        if (cache is True) and (self.categories is not None):
            logging.info("cache categories dictionary...")
            return
        
        url = self.url["category"]
        page = common.get_page(url)
        common.sleep_random_between(2, 5)
        
        cat_container = page.find_all("div", class_="categories__container")
        
        cat = {}
        
        if len(cat_container) == 0:
            logging.info("category container is empty, returning empty dictionary...")
            return cat
        
        for c in cat_container:
            name = c.h2.text
            link = c.h2.a["href"] 
            cat_id = re.findall(self.patt["cat_id"], link)
            if len(cat_id) == 0:
                logging.info("could not find category id, passing...")
                continue
            cat_id = cat_id[0]
            
            sub = self.get_sub_cats(link)
            
            cat[cat_id] = {
                "name": name,
                "link": link,
                "sub": sub
                }
            
        if len(cat) != 0 and save_path != "":
            common.save_pickle(save_path, cat)
        
        self.categories = cat
    
    def get_sub_cats(self, url):
        page = common.get_page(url)
        common.sleep_random_between(2, 5)
        cat = {}
        
        for child in page.find_all("div", class_="desktop__view-child"):
            link = child.a["href"]
            name = child.a.text
            child_id = re.findall(self.patt["child_cat_id"], link)
            if len(child_id) == 0:
                logging.info("could not find category child id, passing...")
                continue
            child_id = child_id[0]

            items = {}
            
            for item in child.find_all("li", class_="category-list__item"):
                item_name = item.a.text
                item_link = item.a["href"]
                item_id = re.findall(self.patt["child_cat_id"], item_link)
                if len(item_id) == 0:
                    logging.info("could not find category item id, passing...")
                    continue
                item_id = item_id[0]
                
                items[item_id] = {
                    "name": item_name,
                    "link": item_link
                    }
        
            cat[child_id] = {
                "name": name,
                "link": link,
                "items": items
                }
        
        return cat
    
    def extract_items_info(self, keys=[], all_keys=False):
        """
        Extract items info from category dictionary
        
        Set all_keys to
         - True to iterate over all category
         - False to iterate over a specific keys
         
        Set list keys with category ids to extract
        """
        if self.categories is None:
            logging.info("Categories dictionary is None")
            return
        
        cat = {}
        
        if all_keys:
            logging.info("Extracting from all keys...")
            cat = self.categories
        else:
            if isinstance(keys, list):
                if len(keys) == 0:
                    logging.info("List of keys are empty...")
                    return
                cat = {}
                for k in keys:
                    if k in self.categories:
                        cat[k] = self.categories[k]
                    
        self.iterate_categories(cat)
        
                
    def iterate_categories(self, categories):
        """
        Iterates over category dictionary to extract information from items
        """
        # Iterate over each root category
        for k in categories:
            root_cat = categories[k]
            subs = root_cat["sub"]
            logging.info('Root Category: {}'.format(root_cat["name"]))
            # Iterate over each sub category
            for kk in subs:
                sub_cat = subs[kk]
                items = sub_cat["items"]
                logging.info('\tSub Category: {}'.format(sub_cat["name"]))
                # Iterate over each item list
                for kkk in items:
                    item_cat = items[kkk]
                    logging.info('\t\tItem Category: {}'.format(item_cat["name"]))
                    for page_item_list in common.get_n_pages(item_cat["link"], 2):
                        self.extract_posts_info(page_item_list)
                    # Iterate over each page
                    # Extract info from post
            logging.info("------------------------------------------------")
                    
    def extract_posts_info(self):
        pass
    
    def get_location(self, page):
        location = page.find("p", class_="ui-seller-info__status-info__subtitle")
        if location is None:
            return ""
        return location.text