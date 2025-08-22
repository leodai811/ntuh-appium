# tests/test_quick_registration.py
import pytest
import time
import conftest as cfg
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.home_page import HomePage
from pages.dept_page import DeptPage
from utils.ui import click_by_text


def click_date_in_horizontal_scroller(driver, wait, text: str):
    """
    在水平日期列中快速捲到最右再點指定日期。
    """
    try:
        # 先快速滑到最右
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
            '.setAsHorizontalList().flingToEnd(10)'
        )
    except Exception:
        pass  # 可能已在畫面上

    # 再捲到指定日期
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
            '.setAsHorizontalList().scrollTextIntoView("{}")'.format(text)
        )
    except Exception:
        pass

    # 精準以文字定位
    el = wait.until(EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
    ))
    try:
        el.click()
    except Exception:
        parent = el.find_element(AppiumBy.XPATH, "ancestor-or-self::*[@clickable='true'][1]")
        parent.click()


@pytest.mark.quick
def test_quick_registration(driver, wait):

    # 進入掛號 & 進入指定科別/次專科
    HomePage(driver, wait).open_register()
    DeptPage(driver, wait).pick_department("內科部").pick_subdept("胃腸肝膽科")

    # 選日期（水平日期條）
    click_date_in_horizontal_scroller(driver, wait, cfg.QUICK_DATE)

    # 選醫師（可捲動清單）
    ok = click_by_text(driver, wait, cfg.QUICK_DOCTOR, fuzzy=False, do_scroll=True) \
         or click_by_text(driver, wait, cfg.QUICK_DOCTOR, fuzzy=True, do_scroll=True)
    
    time.sleep(1)  # 等待 UI 更新

    assert ok, "找不到醫師：," + cfg.QUICK_DOCTOR
