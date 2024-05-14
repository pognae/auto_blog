from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import pyperclip
import io

temp_url = '로그인하려는 URL'
chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(temp_url)

# kaXO 로그인 버튼 찾기(텍스트로)
try:
    # 3초 동안 대기하여 특정 요소가 나타나면 클릭
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="카카오로 3초 만에 시작하기"]'))
    )
    element.click()

    # 클릭 후 다음 동작 수행
    username = driver.find_element(By.NAME, 'loginId')
    pw = driver.find_element(By.NAME, 'password')
    input_id = "입력할 ID"
    input_pw = "입력할 비밀번호"


    def typing(element, keyword, delay):
        for c in keyword:
            element.send_keys(c)
            time.sleep(delay / 1000)


    typing(username, input_id, 100)
    typing(pw, input_pw, 100)

    # 입력이 완료되면 로그인 버튼 누르기
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="로그인"]'))
    )
    element.click()

except:
    print('텍스트를 찾을 수 없습니다.')