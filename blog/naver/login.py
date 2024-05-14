from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager


import time
import pyautogui
import pyperclip
from dotenv import load_dotenv
import os


load_dotenv()

id_plain = os.environ.get('id_plain')
pw_plain = os.environ.get('pw_plain')

def login():
    # 브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)


    # 불필요한 에러메세지 없애기
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)


    # 웹페이지 해당 주소 이름
    driver.implicitly_wait(5)  # 웹페이지가 로딩될 때까지 5초 기다림
    driver.maximize_window()  # 화면 최대화
    driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")


    # 아이디 입력창
    id = driver.find_element(By.CSS_SELECTOR, "#id")
    id.click()
    pyperclip.copy(id_plain)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(5)


    # 비밀번호 입력창
    pw = driver.find_element(By.CSS_SELECTOR, "#pw")
    pw.click()
    pyperclip.copy(pw_plain)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(5)


    # 로그인 버튼
    login_btn = driver.find_element(By.CSS_SELECTOR, "#log\.login")
    login_btn.click()
