# utils/ui.py
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def click_by_text(driver, wait, label: str, fuzzy: bool = False, do_scroll: bool = True) -> bool:
    """
    以文字尋找並點擊；若文字節點不可點，會改點最近的可點擊父節點。
    回傳 True/False 代表是否成功點擊。
    """
    # 捲動到可見（若清單支援）
    if do_scroll:
        try:
            if not fuzzy:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
                    f'.scrollTextIntoView("{label}")'
                )
            else:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
                    f'.scrollIntoView(new UiSelector().textContains("{label}"))'
                )
        except Exception:
            pass  # 可能已在畫面上

    locator = (AppiumBy.ANDROID_UIAUTOMATOR,
               f'new UiSelector().textContains("{label}")' if fuzzy
               else f'new UiSelector().text("{label}")')

    el = wait.until(EC.presence_of_element_located(locator))

    try:
        el.click()
        return True
    except Exception:
        # 點最近的可點擊父節點
        try:
            parent = el.find_element(AppiumBy.XPATH, "ancestor-or-self::*[@clickable='true'][1]")
            parent.click()
            return True
        except Exception:
            return False
