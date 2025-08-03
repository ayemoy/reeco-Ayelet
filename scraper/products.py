from playwright.async_api import Page
from bs4 import BeautifulSoup
from itemInfo import collect_item_information


async def scrape_all_products_in_category(page: Page, category_name: str):
    print(f"\n Scraping products in category: {category_name}")
    page_number = 1
    # count the total items that we already visited in the category
    total_links = 0

    # move pages until there is no more "next page"
    #  loops forever until i break it because we are in the last page of the category
    while True:
        try:
            # waiting until products load in the current page
            await page.wait_for_selector(".product-card-link", timeout=10000)
        except Exception as e:
            print(f" Could not find products: {e}")
            break

        # read page content - all DOM
        html = await page.content()
        # parse the dom
        soup = BeautifulSoup(html, "html.parser")

        # searching <a> with "class =product-card-link" - this it how ww enter to the item itself
        product_links = soup.select(".product-card-link")
        print(f" Page {page_number}: Found {len(product_links)} products")
        total_links += len(product_links)

        # urls creation for all items in the current page (24 items per page)
        product_urls = []
        # save the url and not click th item is more stable - if the DOM changed while scraping we have the URL
        for link in product_links:
            url_suffix = link.get("href", "")
            full_url = f"https://shop.sysco.com{url_suffix}"
            product_urls.append(full_url)

        # go to item page..for each item in the current page
        # loop on 24 items in the current page or less
        for url in product_urls:
            try:
                # go to item page
                await page.goto(url)
                # waiting for the dom to load
                await page.wait_for_load_state("domcontentloaded")
                # waiting for the item name
                await page.wait_for_selector('[data-id="product_name"]', timeout=15000)

                # this function is in itemInfo.py file. collect all data for this item
                await collect_item_information(page, category_name)
                # break
                # go back to items page
                await page.go_back()
                await page.wait_for_selector(".product-card-link", timeout=15000)
            except Exception as e:
                print(f" Failed to load product page: {url} => {e}")
        # break


        # go to next page if we have
        # searching for "next" button
        next_button = await page.query_selector("button[data-id='button_page_next']")
        if next_button:
            # we check both  Disabled/aria-disabled 
            is_disabled = await next_button.get_attribute("disabled")
            aria_disabled = await next_button.get_attribute("aria-disabled")

            # if the button Disabled/aria-disabled is true we in the last page 
            if is_disabled is not None or aria_disabled == "true":
                # print("Reached last page (Next button disabled).")
                break

            try:
                await next_button.click()
                await page.wait_for_selector(".product-card-link", timeout=10000)
                await page.wait_for_timeout(1500)
                page_number += 1
            except Exception as e:
                print(f"Failed to click Next button: {e}")
                break
        else:
            print("Next button not found.")
            break

    print(f"Done. Total products visited in '{category_name}': {total_links}")






