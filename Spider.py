from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

Phone = '13886748038'
Password = 'Leihanning123'
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5, 1)

driver.get('http://sxdx.fanya.chaoxing.com/portal')
driver.maximize_window()
driver.find_element(By.CLASS_NAME, 'loginSub').click()
phone = driver.find_element(By.ID, 'phone')
password = driver.find_element(By.ID, 'pwd')
phoneLoginBtn = driver.find_element(By.ID, 'phoneLoginBtn')
wait.until(EC.element_to_be_clickable(phoneLoginBtn))

# 登录
phone.send_keys(Phone)
password.send_keys(Password)
phoneLoginBtn.click()

# 切换到子页面
wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'frame_content')))
print('登录成功')
sleep(2)

# 进入课程
for course in driver.find_elements(By.CSS_SELECTOR, '[class="course-name overHidden2"]'):
    course.click()
    # course.text
    course = course.text
    # 等待新窗口
    wait.until(EC.number_of_windows_to_be(2))
    # 存储原始窗口的 ID
    original_window = driver.current_window_handle
    # 进入新的窗口
    # 循环执行，直到找到一个新的窗口句柄
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    
    #等待并进入子页面
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'frame_content-zj')))
    home_url = driver.current_url
    element = driver.find_element(By.CSS_SELECTOR, 'span.catalog_sbar').click()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, '#iframe')))
    driver.switch_to.default_content()
    #观看每小节课程
    for index in range(0, len(driver.find_elements(By.CSS_SELECTOR, '.posCatalog_name'))):
        sub_class = driver.find_elements(By.CSS_SELECTOR, '.posCatalog_name')[index]
        if sub_class.get_attribute('title') == '本章测验':
            continue
        wait.until(EC.element_to_be_clickable(sub_class))
        sub_class.click()
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, '#iframe')))
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, '.ans-attach-online.ans-insertvideo-online')))
        driver.find_element(By.CSS_SELECTOR, '.vjs-big-play-button[title="播放视频"]').click()
        is_ended = driver.execute_script("var video = document.getElementsByTagName('video')[0]; if (video) { return video.ended; } else { return null; }")
        while(is_ended==False):
            is_ended = driver.execute_script("var video = document.getElementsByTagName('video')[0]; if (video) { return video.ended; } else { return null; }")
            current_time = driver.execute_script("return document.getElementsByTagName('video')[0].currentTime;")
            sleep(10)
            if(current_time == driver.execute_script("return document.getElementsByTagName('video')[0].currentTime;")):
                driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')
        driver.switch_to.default_content()
    driver.close()
    driver.switch_to.window(original_window)
    

