import cloudscraper
import re
import random
import time
import logging
import _pickle as pkl
from bs4 import BeautifulSoup

def get_page(url):
  src = cloudscraper.create_scraper(browser={"browser": "firefox",
                                             "platform": "windows",
                                             "mobile": False
                                             }).get(url)
  return BeautifulSoup(src.text, features="html.parser")

def get_n_pages(src_url, number):
  """
  Returns n pages from url
  """
  curr_url = src_url
  next_url = ""
  n = 0

  while curr_url and n < number:
    page = get_page(curr_url)
    next_url = get_next_url(page) 
    yield page
		
    curr_url = next_url
    n += 1

def get_next_page(src_url):
  """
  Returns the next page if exists
  """
  curr_url = src_url
  next_url = ""
  
  while curr_url:
    page = get_page(curr_url)
    next_url = get_next_url(page)
    yield page
		
    curr_url = next_url

def get_next_url(page):
  """
  Finds the next url link
  """
  li = page.find("li", class_="andes-pagination__button andes-pagination__button--next")
  if li is None:
    return None

  return li.a["href"]

def search_pattern(pattern, resultSet):
	"""
	Iterates over a resultset to find a pattern
	"""
	value = ""
	for s in resultSet:
		data = s.string
		if type(data) is type(None):
			continue
		m = re.search(pattern, data)
		if m:
			value = m.group(1)
			break
	return value

def sleep_random_between(start, stop):
	"""
	Sleeps random between start and stop seconds to prevent been blocked
	"""
	time.sleep(random.randint(start, stop))

def load_pickle(fpath):
    logging.info("loading pickle file...")
    try:
        with open(fpath, 'rb+') as f:
            cat = pkl.load(f)
        return cat
    except Exception as e:
        logging.info("could not load pickle file...")
        logging.info(e)
        return None
    
def save_pickle(fpath, data):
    logging.info("saving pickle file...")
    try:
        with open(fpath, 'wb+') as f:
            pkl.dump(data, f)
    except Exception as e:
        logging.info("could not save pickle file...")
        logging.info(e)
        return None
