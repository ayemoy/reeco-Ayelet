from playwright.async_api import Page
from bs4 import BeautifulSoup
from itemInfo import collect_item_information


async def scrape_all_products_in_category(page: Page, category_name: str):
    print(f"\n Scraping products in category: {category_name}")
    page_number = 1
    total_links = 0

    while True:
        try:
            await page.wait_for_selector(".product-card-link", timeout=10000)
        except Exception as e:
            print(f" Could not find products: {e}")
            break

        # read page content
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        product_links = soup.select(".product-card-link")
        print(f" Page {page_number}: Found {len(product_links)} products")
        total_links += len(product_links)

        # urls creation
        product_urls = []
        for link in product_links:
            url_suffix = link.get("href", "")
            full_url = f"https://shop.sysco.com{url_suffix}"
            product_urls.append(full_url)

        # go to item page
        for url in product_urls:
            try:
                await page.goto(url)
                await page.wait_for_load_state("domcontentloaded")

                await page.wait_for_selector('[data-id="product_name"]', timeout=15000)

                await collect_item_information(page, category_name)
                # break
                await page.go_back()
                await page.wait_for_selector(".product-card-link", timeout=15000)
            except Exception as e:
                print(f" Failed to load product page: {url} => {e}")
        # break


        # go to next page if we have
        next_button = await page.query_selector("button[data-id='button_page_next']")
        if next_button:
            is_disabled = await next_button.get_attribute("disabled")
            aria_disabled = await next_button.get_attribute("aria-disabled")
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






