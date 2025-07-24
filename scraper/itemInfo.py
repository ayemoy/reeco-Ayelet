from playwright.async_api import Page
from bs4 import BeautifulSoup
import re

# save every data for categories
category_data = {}

# clean the text
def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()





async def collect_item_information(page: Page, category_name: str) -> None:
    
    # if there is "read more" button in page we need to click on it
    try:
        read_more = await page.query_selector('button:has-text("Read More")')
        if read_more:
            await read_more.click()
            await page.wait_for_timeout(500)  # wait for description to load
    except Exception as e:
        print(f"ℹRead More button not found or click failed: {e}")
    
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")

    product = {}

    ### all the 6 data that i have to collect in assignment
    try:
        name = soup.select_one('[data-id="product_name"]')
        product["Product Name"] = clean(name.text if name else "")
    except:
        product["Product Name"] = ""

    try:
        brand = soup.select_one('[data-id="product_brand_link"]')
        product["Brand Name"] = clean(brand.text if brand else "")
    except:
        product["Brand Name"] = ""

    try:
        pack = soup.select_one('[data-id="pack_size"]')
        product["Packaging Information"] = clean(pack.text if pack else "")
    except:
        product["Packaging Information"] = ""

    try:
        sku = soup.select_one('[data-id="product_id"]')
        product["SKU"] = clean(sku.text if sku else "")
    except:
        product["SKU"] = ""

    try:
        img = soup.select_one('[data-id="main-product-img-v2"]')
        product["Picture URL"] = img.get("src") if img else ""
    except:
        product["Picture URL"] = ""

    try:
        desc = soup.select_one('.description-detail-wrapper')
        description_text = clean(desc.text if desc else "")

        #clean the "Read Less" 
        description_text = re.sub(r'\s*Read Less\s*$', '', description_text, flags=re.IGNORECASE)

        product["Description"] = description_text
    except:
        product["Description"] = ""

    
    ### get the data from the headline - Specifications
    try:
        spec_section = soup.find("div", class_="product-specifications-wrapper")
        if spec_section:
            spec_rows = spec_section.select("div.product-spec-description")
            for row in spec_rows:
                label_el = row.select_one(".product-spec-header")
                detail_els = row.select("div.product-spec-details")

                if label_el and detail_els:
                    key = clean(label_el.get_text())
                    # collect all rows 
                    values = [clean(detail.get_text()) for detail in detail_els]
                    val = " ".join(values)
                    product[key] = val
    except Exception as e:
        print(f"Failed to parse specifications: {e}")

    
    # collect theinfo from title "Nutrition" block
    try:
        ingredients_header = soup.find("div", class_="nutrition-details-header", string=re.compile(r"Ingredients", re.I))
        if ingredients_header:
            # dad of Nutrition
            nutrition_section = ingredients_header.find_parent("div", class_="nutrition-section")
            if nutrition_section:
                # find ingredients_text
                ingredients_text = nutrition_section.select_one('[data-id="ingredients_text"]')
                if ingredients_text:
                    product["Ingredients"] = clean(ingredients_text.get_text())

                # find header + value in the nutrition-section
                nutrition_wrappers = nutrition_section.select("div.other-nutrition-detail-wrapper")
                for wrapper in nutrition_wrappers:
                    title = wrapper.select_one("[class$='-header']")
                    value = wrapper.select_one("[data-id$='-value']")
                    if title and value:
                        key = clean(title.get_text())
                        val = clean(value.get_text())
                        product[key] = val
    except Exception as e:
        print(f"Failed to parse Nutrition (Ingredients) section: {e}")


    #save it by categories
    if category_name not in category_data:
        category_data[category_name] = []
    
    category_data[category_name].append(product)
