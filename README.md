# Scraper for mercado libre
Extract information from mercado libre web pages with the purpose of getting insights about the selling products.

## Stages
* Scrape categories
* Scrape each category
* Save information
* Visualize information

## Category structure
 -> [Belleza]  **Root**
          -> [Barbería]  **Sub**
                    -> [Afeitadoras] **Item**

## Product structure
- item_name
- item_id
- item_price
- local_item_price
- available_stock
- sold_stock
- brand
- model
- condition
- root_category
- path_to_root
- seller_id
- location
- seller_type
- reputation_level
- seller_status
- customer_satisfaction (thermomether)
- seller_age
- sales_completed

## Scraping categories
1. Scrape categories page and save information
2. Find paging object.
3. Iterate over pages to get all postings.
4. Iterate over posts to extract the info.
5. Save information.

## Database schema
We consider 2 tables *Province* and *Mode*.
The table mode is a generalization from different tables:
- sale
- rental
- temporal
- project
	- pre-sale-plan
	- pre-sale-building
	- pre-sale-premiere

