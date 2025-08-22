# pages/home_page.py
from selenium.common.exceptions import TimeoutException
from utils.ui import click_by_text

class HomePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open_register(self, label: str = "網路掛號"):
        # 1) 精準、不捲動（最快）
        try:
            if click_by_text(self.driver, self.wait, label, fuzzy=False, do_scroll=False):
                return self
        except TimeoutException:
            pass  # 找不到就往下試
        # 即使沒丟例外，但回傳 False 也繼續往下試

        # 2) 精準、允許捲動（較穩）
        try:
            if click_by_text(self.driver, self.wait, label, fuzzy=False, do_scroll=True):
                return self
        except TimeoutException:
            pass

        raise AssertionError(f"找不到「{label}」")
