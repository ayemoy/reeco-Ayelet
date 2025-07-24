# Sysco Product Scraper

## Overview

This project implements a web scraper that extracts product data from the [Sysco](https://shop.sysco.com) website. The scraper is designed to collect structured information about grocery and foodservice items from various product categories.

## Technologies Used

- **Python** – chosen as the main programming language.
- **Playwright** – a modern browser automation library, used instead of Selenium.
- **Pandas** – preferred for handling and exporting tabular data in CSV format.
- **BeautifulSoup** – used for parsing and navigating HTML/DOM structures more clearly and easily.

## Zip Code Used

- The scraper was run using the following U.S. zip code: `97035`.

## Site Access Limitations

Due to Sysco’s registration policy:

- I was unable to register as a customer since full business verification is required.
- Even when using a VPN and a phone number based in Oregon, I could only browse the site as a guest.
- As a guest, the number of products shown was limited, and I had no access to their APIs, which would have simplified data extraction.

## Technical Challenges

- After two days of scraping, the site began blocking access regardless of the U.S. zip code used.
- I was eventually able to bypass the block and continue scraping successfully.

## Bonus Features

The following bonus requirements were implemented:

- **Scraped all products from all categories**
- **Initially extracted only the essential fields required by the assignment**
- **Extended scraping logic to collect additional product-specific fields**, such as:
  - Nutritional information
  - Ingredients
  - Dimensions
  - Features
  - GTIN
- Not all possible fields were collected, in order to save time and avoid repeated blocks but the extraction logic is extendable and demonstrates full understanding of the task.

## Future Optimization

- The scraper could be significantly accelerated using Python's `asyncio` with a `Semaphore` to run scraping tasks in parallel across multiple browser tabs.
- For clarity and simplicity, this version was submitted in a more naive, sequential form.



