"""Browser-based smoke test.
Run with: python tests/smoke_test.py (requires playwright package and Chromium).
All tests operate on the local file. No network connections needed.
"""
from pathlib import Path
from shutil import which
from playwright.sync_api import sync_playwright

HTML = (Path(__file__).resolve().parent.parent / "index.html").read_text(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=which("chromium"), args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1365, "height": 900})
    page.set_content(HTML)
    assert page.locator("#profit").inner_text() == "¥14.38", page.locator("#profit").inner_text()
    assert page.locator("#breakEven").inner_text() == "¥22.61", page.locator("#breakEven").inner_text()
    assert page.locator("#targetPrice").inner_text() == "¥34.63", page.locator("#targetPrice").inner_text()
    page.locator("#discount").fill("100")
    assert not page.locator("#error").is_hidden()
    assert page.locator("#profit").inner_text() == "—"
    page.locator("#exampleBtn").click()
    assert page.locator("#error").is_hidden()
    page.locator("#clearBtn").click()
    assert page.locator("#profit").inner_text() == "¥0.00"
    assert page.locator("#margin").inner_text() == "—"
    page.locator("#exampleBtn").click()
    page.locator("#price").fill("5")
    assert page.locator("#profit").inner_text() == "−¥14.64"
    assert page.locator("#profitStatus").inner_text() == "预计亏损"
    page.locator("#exampleBtn").click()
    page.locator("#platformRate").fill("99")
    page.locator("#paymentRate").fill("2")
    assert not page.locator("#error").is_hidden()
    page.locator("#exampleBtn").click()
    page.locator("#copyBtn").click()
    assert page.locator("#copyStatus").inner_text() in ("已复制计算结果。", "自动复制失败，请使用支持复制功能的现代浏览器。")
    mobile = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, device_scale_factor=1)
    mobile.set_content(HTML)
    assert mobile.locator("#price").is_visible()
    assert mobile.locator("#profit").inner_text() == "¥14.38"
    assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "mobile horizontal overflow"
    mobile.screenshot(path=str(Path(__file__).resolve().parent.parent / "preview-mobile.png"), full_page=True)
    page.screenshot(path=str(Path(__file__).resolve().parent.parent / "preview-desktop.png"), full_page=True)
    browser.close()
print("PASS: sample calculation, break-even, goal price, invalid input, loss, fee limit, reset, copy UI, mobile layout")
