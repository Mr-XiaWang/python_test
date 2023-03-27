from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

def broadcast(driver:webdriver):
    while not len(driver.find_elements(By.TAG_NAME, 'iframe'))==0:
        driver.switch_to.frame(0)
        time.sleep(1)
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="video"]/button')))
    driver.find_element(By.XPATH, '//*[@id="video"]/button').click()
    time.sleep(0.5)
    t = driver.find_element(By.XPATH, '//*[@id="video"]/div[6]/div[4]/span[2]').text.split(":")
    if len(t)==3:
        hours=float(t[0])
        minutes=float(t[1])
        seconds=float(t[2])
        time.sleep(hours*60*60+minutes*60+seconds)
    elif len(t)==2:
        minutes = float(t[0])
        seconds = float(t[1])
        time.sleep(minutes * 60 + seconds)
    elif len(t)==1:
        time.sleep( int(t[0]))
    driver.switch_to.default_content()
    time.sleep(2)






class MyThread(threading.Thread):
    def __init__(self, id, pwd,course_name):
        threading.Thread.__init__(self)
        self.id = id
        self.pwd = pwd
        self.course_name=course_name

    def run(self):
        driver = webdriver.Edge(executable_path='msedgedriver.exe')
        driver.get('http://passport2.chaoxing.com/login?fid=16202&role=16&refer=http://i.mooc.chaoxing.com')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="leftdiv"]/form')))
        driver.find_element(By.XPATH, '//*[@id="phone"]').send_keys(self.id)
        time.sleep(0.25)
        driver.find_element(By.XPATH, '//*[@id="pwd"]').send_keys(self.pwd)
        time.sleep(0.25)
        driver.find_element(By.XPATH, '//*[@id="loginBtn"]').click()

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="zne_kc_icon"]/em')))

        driver.get('http://mooc1-1.chaoxing.com/visit/interaction?s=dd37517a93322304ccc597e1dedabe48')

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]')))
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]').click()

        WebDriverWait(driver, 30).until(             # //*[@id="course_232953342_72962440"]/div[2]/h3/a/span
            EC.presence_of_element_located((By.XPATH, '//a[span[text()='+self.course_name+']]')))
        driver.find_element(By.XPATH, '//a[span[text()='+self.course_name+']]').click()

        driver.switch_to.window(driver.window_handles[-1])

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        'https:/'+(driver.find_element(By.XPATH, '//*[@id="frame_content-zj"]').get_attribute('src'))
        driver.get(
            'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse?courseid=232953342&clazzid=72962440&cpi=154174873&ut=s&t=1679833375850')
        driver.switch_to.window(driver.window_handles[-1])

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="fanyaChapter"]/div/div[2]/div[2]')))
        divs = (driver.find_element(By.XPATH, '//*[@id="fanyaChapter"]/div/div[2]/div[2]')).find_elements(By.TAG_NAME,
                                                                                                          'div')  # 定位到整个课程列表

        lis = divs[1].find_element(By.XPATH, './div[@class="catalog_level"]').find_element(By.TAG_NAME,
                                                                                           'ul').find_elements(
            By.TAG_NAME, 'li')

        lis[0].click()

        broadcast(driver)  # 从主页面default_content进入

        driver.switch_to.default_content()
        time.sleep(0.5)

        chapter_list = driver.find_element(By.XPATH, '//*[@id="coursetree"]/ul').find_elements(By.TAG_NAME, 'li')
        chapter_lenth = len(chapter_list)
        for chapter_index in range(0, chapter_lenth):
            if chapter_list[chapter_index].get_attribute('style') == 'display: none;':
                chapter_list[chapter_index].click()
            chapter_list[chapter_index].find_elements(By.TAG_NAME, 'li')
            section_list = chapter_list[chapter_index].find_elements(By.TAG_NAME, 'div')[1].find_element(By.TAG_NAME,
                                                                                                         'ul').find_elements(
                By.TAG_NAME, 'li')
            if chapter_index == 0:
                start_section_index = 1
            else:
                start_section_index = 0
            for section_index in range(start_section_index, len(section_list)):
                section_list[section_index].click()
                time.sleep(0.25)
                broadcast(driver)
                print(driver.title)
        driver.quit()