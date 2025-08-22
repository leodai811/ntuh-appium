# tests/test_register_flow.py
import pytest
from pages.home_page import HomePage
from pages.dept_page import DeptPage

@pytest.mark.smoke
@pytest.mark.parametrize(
    "dept, subdept",
    [
        ("內科部", "胃腸肝膽科"),
        ("內科部", "心臟血管科"),
    ]
)
def test_register_by_dept(driver, wait, dept, subdept):
    """
    首頁 → 網路掛號 → 選科別 → 選次專科（乾測，不送出預約）
    """
    HomePage(driver, wait).open_register()
    DeptPage(driver, wait).pick_department(dept).pick_subdept(subdept)

    assert True
