#这是一个获取澳大利亚官方VET课程信息的一段代码。
#主要使用selenium和pandas包实现，
#使用了selenium的webdriver新建浏览器对象，
#根据XPath、TAG_NAME、CLASS_NAME等特点定位元素，
#使用expected_conditions等待元素渲染结束后再进行下一步操作，
#使用selenium中的Selector实现对复选框的操作，
#使用pandas.DataFrame()函数构建df对象，并使用df.to_excel()函数将数据存储到本地文件，
#to_excel函数有两个参数，第一个是文件名，第二个是是否带序列号

#项目中的VET_course_info.xlsx中的C4表格是这段代码执行侯后的存储的数据，
#另两个表是这段代码在复选框处选择另外条件存储的数据
#occupation_list.xlsx是运行一段类似代码存储的数据
#后续导入MySQL数据库可以进行多种条件的查询。


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

#   这是读取一页信息的函数，参数是一个浏览器驱动对象，返回值是一个字典组成的列表。       函数功能：点击这页中需要点击的每个链接然后在新页面读取信息
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

#  新建浏览器驱动对象
driver = webdriver.Edge()

driver.get('https://cricos.education.gov.au/Course/CourseSearch.aspx')  #控制浏览器访问该网页
driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseSearchCriteria_chkWorkComponent"]').click()    #使用XPath寻址方式查找元素并模拟点击事件
Select(driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseSearchCriteria_ddlTypeOfCourse"]')).select_by_value('C4')  #根据条件选择复选框

driver.find_element(By.XPATH,'//*[@id="ctl00_cphDefaultPage_btnSearch"]').click()  

#   等待某元素渲染结束侯继续运行代码     
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_cphDefaultPage_courseList_gridSearchResults"]/tbody')))
courses=read_page(driver)       #  运行read_page()函数获取第一页的信息。
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
    courses.extend(read_page(driver))   #   使用extend函数将新读取的信息列表添加到原列表中
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
df = pd.DataFrame(courses)   #   使用pandas.DataFrame组织数据
df.to_excel('VET_courses_04_info.xlsx', index=False)      #将数据存储到本地的VET_courses_04_info.xlsx文件

driver.quit()
#'Advanced Diploma of Accounting', 'Course Sector': 'VET', 'CRICOS Course Code': '099029B', 'VET National Code': 'FNS60217', 'Dual Qualification': 'No',
#'Advanced Diploma of Accounting', 'Course Sector': 'VET', 'CRICOS Course Code': '099029B', 'VET National Code': 'FNS60217', 'Dual Qualification': 'No',
