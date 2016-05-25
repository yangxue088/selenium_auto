# -*- coding: utf-8 -*-
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

browser = webdriver.Firefox()

browser.get('https://login.aliexpress.com/')

input("登录完成了请输入")

# browser.find_element(value='fm-login-id').send_keys('shawnxiao2015@outlook.com')
# browser.find_element(value='fm-login-password').send_keys('TJ$shawn2016')
# browser.find_element(value='fm-login-password').submit()

with open("input/ali_hangye.csv") as file:
    for url in csv.reader(file):

        if len(url) == 0:
            print " "
            continue

        browser.get(url)

        Select(browser.find_element(By.XPATH, "//span[@class='idy-int-t-2']/select")).select_by_visible_text('最近30天')

        fangkeshu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[2]").text
        liulanliang = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[3]").text
        zhifujine = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[4]").text
        zhifudingdanshu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[5]").text
        gongxuzhishu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[6]").text

        print url, fangkeshu, liulanliang, zhifujine, zhifudingdanshu, gongxuzhishu

browser.quit()
