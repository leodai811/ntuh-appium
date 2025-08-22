# conftest.py
import os
import subprocess
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
DEFAULT_APP_PKG = os.getenv("APP_PKG", "xfntuh.droid")
DEFAULT_APP_ACT = os.getenv("APP_ACT", "crc646309fb9dd9b44dd0.MainActivity")

def _get_udid():
    try:
        out = subprocess.check_output(["adb", "devices"], text=True)
        for line in out.splitlines():
            if "\tdevice" in line and not line.startswith("List"):
                return line.split("\t")[0]
    except Exception:
        pass
    return None

def pytest_addoption(parser):
    parser.addoption("--appium-url", action="store", default=DEFAULT_APPIUM_URL)
    parser.addoption("--udid", action="store", default=os.getenv("ANDROID_UDID", None))
    parser.addoption("--pkg", action="store", default=DEFAULT_APP_PKG)
    parser.addoption("--activity", action="store", default=DEFAULT_APP_ACT)
    parser.addoption("--timeout", action="store", type=int, default=40)

@pytest.fixture(scope="function")  # 明確每個測試（每組 param）都新建/銷毀一次
def driver(request):
    appium_url = request.config.getoption("--appium-url")
    udid = request.config.getoption("--udid") or _get_udid()
    app_pkg = request.config.getoption("--pkg")
    app_act = request.config.getoption("--activity")

    opts = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "Android Emulator",
        **({"appium:udid": udid} if udid else {}),
        "appium:appPackage": app_pkg,
        "appium:appActivity": app_act,
        "appium:appWaitActivity": "*",
        "appium:noReset": True,
        "appium:autoGrantPermissions": True,
        "appium:newCommandTimeout": 300,
        "appium:disableWindowAnimation": True,
    })

    drv = webdriver.Remote(appium_url, options=opts)

    # 確保 App 在前景
    if drv.current_package != app_pkg:
        try:
            drv.activate_app(app_pkg)
        except Exception:
            drv.start_activity(app_pkg, app_act)

    yield drv

    # —— 每個測試結束前「先關 app 再關 session」——
    try:
        drv.terminate_app(app_pkg)
    except Exception:
        pass
    try:
        drv.quit()
    except Exception:
        pass

@pytest.fixture
def wait(request, driver):
    timeout = request.config.getoption("--timeout")
    return WebDriverWait(driver, timeout)
