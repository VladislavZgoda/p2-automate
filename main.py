import os
from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright

script_dir = Path(__file__).resolve().parent

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    page.goto(os.getenv("URL"))
    page.locator("#userName").click()
    page.locator("#userName").fill(os.getenv("LOGIN"))
    page.locator("#password").click()
    page.locator("#password").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="EnterA").click()
    
    page.locator(".menu-group-interaction").first.click()
    page.get_by_text("Новый профиль энергии").click()
    page.locator("dx-drop-down-box").get_by_role("combobox").click()
    page.locator("dx-button").nth(2).click()
    page.get_by_role("menu").get_by_text("Географические объекты").click()
    page.get_by_title("Поиск").click()
    page.get_by_text("Поиск по наименованию").click()
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").press_sequentially("51424969")
    page.locator("button").nth(4).click()
    page.get_by_role("gridcell", name="Меркурий 230 ART-03 PQRSIDN, №51424969").get_by_label(
        "Выбрать строку"
    ).click()
    
    page.get_by_role("button", name="OK").click()
    page.get_by_role("checkbox", name="A+").click()

    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("combobox").nth(1).press("ArrowLeft")
    page.get_by_role("combobox").nth(1).press("ArrowLeft")
    page.get_by_role("combobox").nth(1).press_sequentially("01")
    page.get_by_role("combobox").nth(1).press_sequentially("12")
    page.get_by_role("combobox").nth(1).press_sequentially("2025")
    
    for _ in range(3):
        page.get_by_role("combobox").nth(1).press_sequentially("00")
    
    page.get_by_role("combobox").nth(2).click()
    page.get_by_role("combobox").nth(2).press("ArrowLeft")
    page.get_by_role("combobox").nth(2).press("ArrowLeft")
    page.get_by_role("combobox").nth(2).press_sequentially("01")
    page.get_by_role("combobox").nth(2).press_sequentially("01")
    page.get_by_role("combobox").nth(2).press_sequentially("2026")
    
    for _ in range(3):
        page.get_by_role("combobox").nth(2).press_sequentially("00")

    with page.expect_download() as download_info:
        page.get_by_role("button", name="Excel").click()
    download = download_info.value
    download.save_as(script_dir / "download" /download.suggested_filename)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
