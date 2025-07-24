from playwright.async_api import Page
from bs4 import BeautifulSoup
from products import scrape_all_products_in_category


async def get_all_categories(page: Page) -> list[dict]:
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")

    categories = []
    for el in soup.select("span.category-grid-title"):
        name = el.get_text(strip=True)
        if name:
            categories.append({"name": name})

    print(f"Found {len(categories)} categories")
    return categories


async def click_category_by_name(page: Page, category_name: str):
    print(f"Clicking category: {category_name}")

    all_boxes = await page.query_selector_all(".category-grid-button")
    for box in all_boxes:
        title_element = await box.query_selector("span.category-grid-title")
        if title_element:
            title = await title_element.inner_text()
            if title.strip() == category_name:
                await box.click()
                print(f"Clicked on '{category_name}'")
                return
    print(f"Category '{category_name}' not found.")







# async def visit_each_category(page: Page) -> None:
#     categories_url = page.url  
#     print("🔍 🔍🔍categories_url:", categories_url)

#     categories = await get_all_categories(page)

#     # ✅ הרץ רק קטגוריה אחת לצורך בדיקה:
#     for cat in categories:
#         if cat["name"] != "Chemicals":  # החלף לקטגוריה שאת רוצה לבדוק
#             continue

#         await click_category_by_name(page, cat["name"])
#         print(f"🔍 Inside category: {cat['name']}")

#         await scrape_all_products_in_category(page, cat["name"])

#         print(f"🔁 Going back to categories page...")
#         await page.goto(categories_url)

#         try:
#             await page.wait_for_selector("span.category-grid-title", timeout=15000)
#         except Exception as e:
#             print(f"⚠️ Failed waiting for categories page: {e}")
#             return

#         break  # ✅ סיים אחרי הקטגוריה הראשונה לבדיקה













async def visit_each_category(page: Page) -> None:
    categories_url = page.url  
    print("🔍 🔍🔍categories_url:",categories_url)
    categories = await get_all_categories(page)

    for index, cat in enumerate(categories):
        await click_category_by_name(page, cat["name"])
        print(f"🔍 Inside category: {cat['name']}")

        await scrape_all_products_in_category(page, cat["name"])

        print(f"🔁 Going back to categories page...")
        await page.goto(categories_url)
        
        # חשוב! חכי לאלמנט שמעיד שהעמוד נטען לגמרי
        try:
            await page.wait_for_selector("span.category-grid-title", timeout=15000)
        except Exception as e:
            print(f"⚠️ Failed waiting for categories page: {e}")
            return

        # בגלל שהעמוד נטען מחדש – צריך לשלוף את האלמנטים מחדש
        categories = await get_all_categories(page)






# async def visit_each_category(page: Page) -> None:
#     # שמירת כתובת עמוד הקטגוריות הראשי
#     categories_url = page.url  

#     categories = await get_all_categories(page)

#     for cat in categories:
#         await click_category_by_name(page, cat["name"])
#         print(f"🔍 Inside category: {cat['name']}")

#         await scrape_all_products_in_category(page, cat["name"])

#         # חזרה לעמוד הראשי של הקטגוריות
#         await page.goto(categories_url)
#         await page.wait_for_selector("span.category-grid-title", timeout=10000)
