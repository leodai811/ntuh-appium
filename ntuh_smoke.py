import subprocess, time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

APP_PKG = "xfntuh.droid"
APP_ACT = "crc646309fb9dd9b44dd0.MainActivity"

REGISTER_LABELS = ["網路掛號", "預約掛號"] 
DEPT_NAME = "內科部"
SUBDEPT_NAME = "胃腸肝膽科"

def get_udid():
    try:
        out = subprocess.check_output(["adb", "devices"], text=True)
        for line in out.splitlines():
            if "\tdevice" in line and not line.startswith("List"):
                return line.split("\t")[0]
    except Exception:
        pass
    return None

def click_by_text(driver, wait, label, fuzzy=False, do_scroll=True):
    """以文字尋找並點擊；若文字節點不可點，會改點最近的可點擊父節點。"""
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
        try:
            parent = el.find_element(AppiumBy.XPATH, "ancestor-or-self::*[@clickable='true'][1]")
            parent.click()
            return True
        except Exception:
            return False

def main():
    udid = get_udid()
    opts = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "Android Emulator",
        **({"appium:udid": udid} if udid else {}),
        "appium:appPackage": APP_PKG,
        "appium:appActivity": APP_ACT,
        "appium:appWaitActivity": "*",
        "appium:noReset": True,
        "appium:autoGrantPermissions": True,
        "appium:newCommandTimeout": 300,
        "appium:disableWindowAnimation": True,
    })

    driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
    wait = WebDriverWait(driver, 40)

    try:
        # 確保 App 在前景
        if driver.current_package != APP_PKG:
            try: driver.activate_app(APP_PKG)
            except Exception: driver.start_activity(APP_PKG, APP_ACT)

        # 1) 首頁：直接以「文字」點『網路掛號』（依序嘗試標籤）
        clicked = False
        for label in REGISTER_LABELS:
            try:
                if click_by_text(driver, wait, label, fuzzy=False, do_scroll=False):
                    print(f"✅ 點擊：{label}")
                    clicked = True
                    break
            except TimeoutException:
                # 試模糊匹配與捲動
                try:
                    if click_by_text(driver, wait, label, fuzzy=True, do_scroll=True):
                        print(f"✅ 點擊(模糊)：{label}")
                        clicked = True
                        break
                except TimeoutException:
                    pass
        if not clicked:
            raise RuntimeError("找不到『網路掛號/預約掛號/門診掛號』文字")

        # 2) 科別：點『內科部』
        if not click_by_text(driver, wait, DEPT_NAME, fuzzy=False, do_scroll=True):
            # 失敗再用模糊
            assert click_by_text(driver, wait, DEPT_NAME, fuzzy=True, do_scroll=True), f"找不到 {DEPT_NAME}"
        print(f"✅ 已選科別：{DEPT_NAME}")

        # 3) 次專科：點『胃腸肝膽科』
        if not click_by_text(driver, wait, SUBDEPT_NAME, fuzzy=False, do_scroll=True):
            assert click_by_text(driver, wait, SUBDEPT_NAME, fuzzy=True, do_scroll=True), f"找不到 {SUBDEPT_NAME}"
        print(f"✅ 已選次專科：{SUBDEPT_NAME}")

        print("🎉 Flow OK（純文字點擊）：首頁→網路掛號→內科部→胃腸肝膽科")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
