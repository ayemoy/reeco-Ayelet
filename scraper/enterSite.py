from playwright.async_api import async_playwright, Browser, Page

# 97201
# 97035
async def enter_site_and_get_page(zip_code: str = "97501") -> tuple[Browser, Page]:
    print("Launching browser and navigating to site...")

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()

    # Go to homepage
    await page.goto("https://shop.sysco.com", timeout=60000)

    # Click "Continue as Guest"
    await page.wait_for_selector("text=Continue as Guest", timeout=15000)
    await page.click("text=Continue as Guest")

    # Wait for ZIP input and type ZIP
    await page.wait_for_selector("input[type='text']")
    await page.fill("input[type='text']", zip_code)
    await page.keyboard.press("Enter")

    # Wait for homepage to load after zip
    await page.wait_for_selector("text=Shop by Category", timeout=15000)

    print("Successfully entered site and ZIP!")
    return browser, page
