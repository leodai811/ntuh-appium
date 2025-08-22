# pages/home_page.py
from selenium.common.exceptions import TimeoutException
from utils.ui import click_by_text

DEFAULT_REGISTER_LABELS = ["網路掛號", "預約掛號", "門診掛號"]

class HomePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open_register(self, labels=DEFAULT_REGISTER_LABELS):
        """
        點首頁的『網路掛號/預約掛號/門診掛號』其中之一。
        先精準，不行再模糊；有成功即返回 self。
        """
        for label in labels:
            try:
                if click_by_text(self.driver, self.wait, label, fuzzy=False, do_scroll=False):
                    return self
            except TimeoutException:
                try:
                    if click_by_text(self.driver, self.wait, label, fuzzy=True, do_scroll=True):
                        return self
                except TimeoutException:
                    continue
        raise AssertionError("找不到『網路掛號/預約掛號/門診掛號』文字")
