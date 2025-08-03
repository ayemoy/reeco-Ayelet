from playwright.async_api import Page
from bs4 import BeautifulSoup
from products import scrape_all_products_in_category




async def visit_each_category(page: Page) -> None:
    # i saved the "shop by category" url so after i visit in each category i can
    # go back to the main page to choose another category
    categories_url = page.url  
    print("categories_url:",categories_url)

    # function in this file. get [{'name': 'Produce'}, {'name': 'Meat & Seafood'}] of all categories.
    categories = await get_all_categories(page)

    # for each category
    for cat in categories:
        # search the right DIV and click on it to go to uts page
        await click_category_by_name(page, cat["name"])
        print(f" Inside category: {cat['name']}")

        # the function is in products.py.
        # scrape all products in this category
        await scrape_all_products_in_category(page, cat["name"])

        print(f"Going back to categories page...")
        await page.goto(categories_url)
        

        try:
            await page.wait_for_selector("span.category-grid-title", timeout=15000)
        except Exception as e:
            print(f" Failed waiting for categories page: {e}")
            return
        # i get again all categories because after i did "await page.goto(categories_url)"
        # the prev elements could change so we need to get them again. the DOM re-build from scratch.
        # the element that have been in memory not longer good we need to reload them again if there are changes
        categories = await get_all_categories(page)







async def get_all_categories(page: Page) -> list[dict]:
    # gets the whole HTML page - this is the DOM
    html = await page.content()
    # insert the DOM into BeautifulSoup for easy parsing and easy CSS selector
    soup = BeautifulSoup(html, "html.parser")

    # [{'name': 'Produce'}, {'name': 'Meat & Seafood'}]
    categories = []
    # extract all spans who contain the category name
    for el in soup.select("span.category-grid-title"):
        name = el.get_text(strip=True)
        if name:
            categories.append({"name": name})

    print(f"Found {len(categories)} categories")
    return categories








async def click_category_by_name(page: Page, category_name: str):
    print(f"Clicking category: {category_name}")

    # gets all dives on the categories
    all_boxes = await page.query_selector_all(".category-grid-button")
    
    for box in all_boxes:
        # for each div i searching for the title
        title_element = await box.query_selector("span.category-grid-title")
        if title_element:
            # read the inner text - for example "Produce"
            title = await title_element.inner_text()
            # if the name is fit so we want to click it
            if title.strip() == category_name:
                await box.click()
                print(f"Clicked on '{category_name}'")
                return
    print(f"Category '{category_name}' not found.")







# async def visit_each_category(page: Page) -> None:
#     categories_url = page.url  
#     print("categories_url:", categories_url)

#     categories = await get_all_categories(page)

#     # run one category for debug
#     for cat in categories:
#         if cat["name"] != "Chemicals":  
#             continue

#         await click_category_by_name(page, cat["name"])
#         print(f" Inside category: {cat['name']}")

#         await scrape_all_products_in_category(page, cat["name"])

#         print(f" Going back to categories page...")
#         await page.goto(categories_url)

#         try:
#             await page.wait_for_selector("span.category-grid-title", timeout=15000)
#         except Exception as e:
#             print(f"Failed waiting for categories page: {e}")
#             return

#         break  # 

















# async def visit_each_category(page: Page) -> None:
#     categories_url = page.url  

#     categories = await get_all_categories(page)

#     for cat in categories:
#         await click_category_by_name(page, cat["name"])
#         print(f"Inside category: {cat['name']}")

#         await scrape_all_products_in_category(page, cat["name"])

#         await page.goto(categories_url)
#         await page.wait_for_selector("span.category-grid-title", timeout=10000)
