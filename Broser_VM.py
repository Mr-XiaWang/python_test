from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 模仿点击事件（选条件->点按钮），获取完整的HTML代码
driver = webdriver.Edge()

driver.get('https://cricos.education.gov.au/Course/CourseSearch.aspx')
driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseSearchCriteria_chkWorkComponent"]').click()
driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_btnSearch"]').click()
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody/tr[2]')))
driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody/tr[2]').click()
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="course"]/div/div[1]/div')))
divs = driver.find_element(By.XPATH, '//*[@id="course"]/div/div[1]/div').find_elements(By.TAG_NAME, 'div')
print(driver.find_element(By.XPATH,'//*[@id="course"]/div/div[1]/div/div[1]/label').text)
driver.back()
driver.back()

driver.quit()
