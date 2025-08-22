# pages/dept_page.py
from utils.ui import click_by_text

class DeptPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def pick_department(self, name: str):
        assert click_by_text(self.driver, self.wait, name, fuzzy=False, do_scroll=True) \
               or click_by_text(self.driver, self.wait, name, fuzzy=True, do_scroll=True), \
               f"找不到科別：{name}"
        return self

    def pick_subdept(self, name: str):
        assert click_by_text(self.driver, self.wait, name, fuzzy=False, do_scroll=True) \
               or click_by_text(self.driver, self.wait, name, fuzzy=True, do_scroll=True), \
               f"找不到次專科：{name}"
        return self
