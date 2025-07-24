r
Overview
This project implements a web scraping tool designed to extract product data from the Sysco website. The scraper collects structured information about grocery and foodservice items across multiple categories.

Technologies Used
Python – chosen as the primary programming language for its simplicity and strong ecosystem for data processing.

Playwright – selected as the main browser automation tool for scraping, as it is a modern, powerful alternative to Selenium.

Pandas – used to handle tabular data and export structured information to CSV files.

BeautifulSoup – utilized for clear and flexible parsing of HTML and DOM structures.

Zip Code Used
The scraper was configured to use the following U.S. zip code: 97035 (Lake Oswego, Oregon).

Challenges
The Sysco website requires full business verification to register as a customer. As an unverified guest, I could only access a limited subset of the products.

Even with VPN access and a local Oregon phone number, I was unable to complete the registration process without direct communication with their support team.

As a result, access to their APIs was not possible, and only public product listings were available.

After two days of scraping, the website blocked access to my scraper, regardless of which U.S. zip code I used. Eventually, I was able to overcome this limitation and resume scraping.

Bonus Features Completed
Full Catalog Scraping – The scraper automatically traverses all product categories and gathers data on every visible item.

Extended Field Extraction – Initially, only the required fields were collected. Later, additional fields (such as nutritional values, ingredients, dimensions, features, GTIN, etc.) were extracted when available. These fields vary from product to product.

Selective Field Coverage – Not all fields were scraped to avoid excessive run-time, especially considering the temporary IP blocks I encountered. However, the scraping logic is extensible and demonstrates the intended approach.

Optimization Note
For performance improvements, the scraper could be parallelized using Python's asyncio along with a Semaphore to control the number of concurrent browser tabs. This would significantly reduce scraping time. For this submission, however, I chose to submit a more "naive" sequential version for clarity.

