import asyncio
from enterSite import enter_site_and_get_page
from categories import visit_each_category
from exportToExcel import save_all_to_excel  


async def main():
    print("STARTING MAIN")

    browser, page = await enter_site_and_get_page("97035")
    print("Site loaded successfully and ready for scraping!")

    # summary = []
    await visit_each_category(page)

    
    save_all_to_excel() 
    print("Saving data to Excel...")

    try:
        input("⏸ Press ENTER to close the browser...")
    except EOFError:
        print("Interrupted manually or closed externally")

    await browser.close()
    print("Done. Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())
