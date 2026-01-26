import json
from os import getenv
from pathlib import Path
from datetime import datetime
from typing import Literal, TypedDict

from dateutil.relativedelta import relativedelta
from playwright.sync_api import Playwright, sync_playwright

URL = getenv("URL")
LOGIN = getenv("LOGIN")
PASSWORD = getenv("PASSWORD")

if not URL or not LOGIN or not PASSWORD:
    print("Error! Some env vars are not defined!")
    exit(1)

Profile = TypedDict(
    "Profile",
    {
        "file_name": str,
        "menu_type": Literal["НЭСК", "Географические объекты"],
        "meters": list[str],
    },
)

try:
    with open("profiles.json", mode="r", encoding="UTF-8") as f:
        profiles: list[Profile] = json.load(f)
except FileNotFoundError:
    print("Error! File 'profiles.json' not found!")
    exit(1)

script_dir = Path(__file__).resolve().parent

current_date = datetime.now()
current_month = str(current_date.month).zfill(2)
current_year = str(current_date.year)

previous_month_date = current_date - relativedelta(months=1)
previous_month = str(previous_month_date.month).zfill(2)
previous_year = str(previous_month_date.year)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    page.goto(URL)
    page.locator("#userName").click()
    page.locator("#userName").fill(LOGIN)
    page.locator("#password").click()
    page.locator("#password").fill(PASSWORD)
    page.get_by_role("button", name="EnterA").click()

    page.locator(".menu-group-interaction").first.click()
    page.get_by_text("Новый профиль энергии").click()

    for profile in profiles:
        page.locator("dx-drop-down-box").get_by_role("combobox").click()
        page.locator("dx-button").nth(2).click()

        menu_type = (
            "НЭСК" if profile["menu_type"] == "НЭСК" else "Географические объекты"
        )
        page.get_by_role("menu").get_by_text(menu_type).click()

        for meter in profile["meters"]:
            page.get_by_title("Поиск").click()
            page.get_by_text("Поиск по наименованию").click()
            page.get_by_role("textbox").click()
            page.get_by_role("textbox").press_sequentially(meter)
            page.locator("button").nth(4).click()
            page.get_by_role("gridcell", name=meter).get_by_label(
                "Выбрать строку"
            ).click()
            page.get_by_title("Удалить").locator("button").click()

        page.get_by_role("button", name="OK").click()
        page.get_by_role("checkbox", name="A+").click()

        page.get_by_role("combobox").nth(1).click()
        page.get_by_role("combobox").nth(1).press("ArrowLeft")
        page.get_by_role("combobox").nth(1).press("ArrowLeft")
        page.get_by_role("combobox").nth(1).press_sequentially("01")
        page.get_by_role("combobox").nth(1).press_sequentially(previous_month)
        page.get_by_role("combobox").nth(1).press_sequentially(previous_year)

        for _ in range(3):
            page.get_by_role("combobox").nth(1).press_sequentially("00")

        page.get_by_role("combobox").nth(2).click()
        page.get_by_role("combobox").nth(2).press("ArrowLeft")
        page.get_by_role("combobox").nth(2).press("ArrowLeft")
        page.get_by_role("combobox").nth(2).press_sequentially("01")
        page.get_by_role("combobox").nth(2).press_sequentially(current_month)
        page.get_by_role("combobox").nth(2).press_sequentially(current_year)

        for _ in range(3):
            page.get_by_role("combobox").nth(2).press_sequentially("00")

        with page.expect_download() as download_info:
            page.get_by_role("button", name="Excel").click()

        download = download_info.value
        download.save_as(script_dir / "download" / profile["file_name"])
        page.reload()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
