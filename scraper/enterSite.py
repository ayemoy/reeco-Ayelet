from playwright.async_api import async_playwright, Browser, Page

# 97201
# 97035
async def enter_site_and_get_page(zip_code: str = "97501") -> tuple[Browser, Page]:
    print("Launching browser and navigating to site...")

    # activate the playwright engine
    playwright = await async_playwright().start()

    # open new object of chrome window
    browser = await playwright.chromium.launch(headless=False)

    # open new tab in chrome
    page = await browser.new_page()

    # Go to homepage and wait 60 sec because the page loads a lot
    await page.goto("https://shop.sysco.com", timeout=60000)

    # waiting until "Continue as Guest"and Click it . button not exist at first load so we need to wait.
    await page.wait_for_selector("text=Continue as Guest", timeout=15000)
    # click on the textbox to type the zip code
    await page.click("text=Continue as Guest")

    # Wait for ZIP input and type ZIP
    await page.wait_for_selector("input[type='text']")
    await page.fill("input[type='text']", zip_code)
    await page.keyboard.press("Enter")

    # Wait for homepage to load after zip
    await page.wait_for_selector("text=Shop by Category", timeout=15000)

    print("Successfully entered site and ZIP!")
    return browser, page
