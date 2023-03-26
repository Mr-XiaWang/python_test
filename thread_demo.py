from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import locale
import pandas as pd
from selenium.webdriver.support.ui import Select

driver = webdriver.Edge(executable_path='msedgedriver.exe')
driver.get('http://passport2.chaoxing.com/login?fid=16202&role=16&refer=http://i.mooc.chaoxing.com')
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="leftdiv"]/form')))
driver.find_element(By.XPATH,'//*[@id="phone"]').send_keys('18842637266')
time.sleep(0.25)
driver.find_element(By.XPATH,'//*[@id="pwd"]').send_keys('Wh010820')
time.sleep(0.25)
driver.find_element(By.XPATH,'//*[@id="loginBtn"]').click()
#
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="zne_kc_icon"]/em')))
# driver.find_element(By.XPATH,'//*[@id="zne_kc_icon"]/em').click()
# WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//iframe[@src="http://mooc1-1.chaoxing.com/visit/interaction?s=dd37517a93322304ccc597e1dedabe48"]')))
driver.get('http://mooc1-1.chaoxing.com/visit/interaction?s=dd37517a93322304ccc597e1dedabe48')
# /html/body/div[1]/div/div/div[1]/div[2]
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[1]/div[2]')))
driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[2]').click()
# //*[@id="course_232953342_72962440"]/div[2]/h3/a/span
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="course_232953342_72962440"]/div[2]/h3/a/span')))
driver.find_element(By.XPATH,'//*[@id="course_232953342_72962440"]/div[2]/h3/a/span').click()

# //*[@id="fanyaChapter"]/div/div[2]/div[2]
driver.switch_to.window(driver.window_handles[-1])

WebDriverWait(driver,30).until(EC.presence_of_element_located((By.TAG_NAME,'body')))
# //*[@id="fanyaChapter"]/div/div[2]/div[2]
driver.get('https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse?courseid=232953342&clazzid=72962440&cpi=154174873&ut=s&t=1679833375850')
driver.switch_to.window(driver.window_handles[-1])
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="fanyaChapter"]/div/div[2]/div[2]')))
divs = (driver.find_element(By.XPATH, '//*[@id="fanyaChapter"]/div/div[2]/div[2]')).find_elements(By.XPATH,'./div')
len =len(divs)

for i in range(1,len):
    div2 = (divs[i].find_elements(By.TAG_NAME, 'div'))[1]
    ul=div2.find_element(By.TAG_NAME,'ul')
    lis = ul.find_elements(By.TAG_NAME, 'li')
    print(len(lis))

# WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="zne_kc_icon"]/em')))


# for i in range(1,10):
#     WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="zne_kc_icon"]/em')))
#     driver.find_element(By.XPATH,'//*[@id="zne_kc_icon"]/em').click()
#     time.sleep(3)
#     print(driver.find_element(By.XPATH, '//*[@id="frame_content"]').get_attribute('src'))




driver.quit()