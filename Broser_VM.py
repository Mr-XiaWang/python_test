from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import locale
import pandas as pd
from selenium.webdriver.support.ui import Select
from openpyxl.workbook import Workbook

locale.setlocale(locale.LC_ALL,'')
# def append_course(courses:List[dict]):


def read_page(driver:webdriver):
    courses = []
    row_num= len(driver.find_element(By.XPATH,
                              '//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody').find_elements(
        By.TAG_NAME, 'tr'))
    # 开始进入某一页的学校列表
    for i in range(1, row_num-2):
        trs = driver.find_element(By.XPATH,
                                  '//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody').find_elements(
            By.TAG_NAME, 'tr')
        trs[i].click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="course"]/div/div[1]/div')))
        divs = driver.find_element(By.XPATH, '//*[@id="course"]/div/div[1]/div').find_elements(By.TAG_NAME, 'div')
        # print(len(divs))#获取页面每项信息？？？？
        course = {}
        for div in divs:
            if len(div.find_elements(By.TAG_NAME, 'div')) == 0:
                continue
            key = "_".join((div.find_element(By.TAG_NAME, 'label').text.split(":")[0]).split(" "))
            value = div.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'span').text
            if key == 'Tuition_Fee' or key == 'Non_Tuition_Fee' or key == 'Estimated_Total_Course_Cost' :
                value=locale.atoi(value)
            course[key] = value
            time.sleep(0.0625)
        courses.append(course)
        driver.back()
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="tabInstitutionSearch"]')))
        if len(driver.find_elements(By.XPATH, '//*[@id="Australia"]')) ==1:
            driver.find_element(By.XPATH,'//*[@id="tabInstitutionSearch"]/li[2]/a').click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
    return courses




page=1

# 模仿点击事件（选条件->点按钮），获取完整的HTML代码
driver = webdriver.Edge()

driver.get('https://cricos.education.gov.au/Course/CourseSearch.aspx')
driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseSearchCriteria_chkWorkComponent"]').click()
Select(driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseSearchCriteria_ddlTypeOfCourse"]')).select_by_value('C4')

driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_btnSearch"]').click()
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
courses=read_page(driver)
# df = pd.DataFrame(courses)
# df.to_excel('VET_courses_info.xlsx', index=False)
page+=1
while page<=33:
    pages = driver.find_elements(By.XPATH, '//a[text()=' + str(page) + ']')
    if len(pages) ==1:
        pages[0].click()
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
    else:
        ells = driver.find_elements(By.XPATH, '//a[text()="..."]')
        if len(ells) == 2:
            ells[1].click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
        else:
            ells[0].click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
    courses.extend(read_page(driver))
    print("读完第",page,'页')
    page+=1
    # if page%10==0:
    #     ells = driver.find_elements(By.XPATH, '//a[text()="..."]')
    #     if len(ells) ==2:
    #         ells[1].click()
    #         WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
    #     else:
    #         ells[0].click()
    #         WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
    # else:
    #     driver.find_element(By.XPATH,'//a[text()='+str(page)+']').click()
    #     page += 1
    #     WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
    # courses.extend(read_page(driver))
df = pd.DataFrame(courses)
df.to_excel('VET_courses_04_info.xlsx', index=False)

driver.quit()
#'Advanced Diploma of Accounting', 'Course Sector': 'VET', 'CRICOS Course Code': '099029B', 'VET National Code': 'FNS60217', 'Dual Qualification': 'No',
#'Advanced Diploma of Accounting', 'Course Sector': 'VET', 'CRICOS Course Code': '099029B', 'VET National Code': 'FNS60217', 'Dual Qualification': 'No',