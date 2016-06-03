# -*- coding: utf-8 -*-
import csv
import sys
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Firefox()

browser.get('http://erp.chinasalestore.com/login')

browser.find_element(By.ID, 'username').send_keys(sys.argv[1])
browser.find_element(By.ID, 'password').send_keys(sys.argv[2])
browser.find_element(By.ID, 'password').submit()

browser.get('http://sale.chinasalestore.com/ui/ProductList.aspx')

browser.find_element(By.ID, 'tab1').click()

browser.switch_to.frame(browser.find_element(By.XPATH, "//div[@id='tabid1']/iframe"))

Select(browser.find_element(By.ID, 's_status')).select_by_visible_text('上线')
Select(browser.find_element(By.ID, 'sc_template')).select_by_visible_text('Wish')

browser.find_element(By.XPATH, "//input[@name='Copyright' and @value='0']").click()
browser.find_element(By.XPATH, "//input[@name='Battery' and @value='0']").click()

all_sku = set()

select_sku = OrderedDict()

with open('input/css_all.csv') as file:
    for sku, price, in csv.reader(file):

        if sku not in all_sku:

            all_sku.add(sku)

            browser.find_element(By.ID, 'sy_sku').clear()

            browser.find_element(By.ID, 'sy_sku').send_keys(sku)

            wait = WebDriverWait(browser, 60)

            wait.until(expected_conditions.invisibility_of_element_located((By.XPATH, "//div[contains(text(), '正在处理，请稍待')]")))

            browser.find_element(By.ID, 'but_Search_Goods').click()

            wait.until(expected_conditions.invisibility_of_element_located((By.XPATH, "//div[contains(text(), '正在处理，请稍待')]")))

            sales = browser.find_element(By.CLASS_NAME, 'datagrid-btable').find_elements_by_xpath("//span[contains(@style, 'color')]")

            if len(sales) == 0:
                print 'sku: {}, 搜索条件或销量条件不符合, 自动忽略'.format(sku)
                continue

            is_upload = input('sku: {}, 是否上传?: '.format(sku))

            if int(is_upload) == 1:
                print 'sku: {}, 选择了上传'.format(sku)
                select_sku[sku] = price

                if len(select_sku) == 60:
                    print '最后一个上传的sku: {}'.format(sku)
                    break

            else:
                print 'sku: {}, 选择了忽略'.format(sku)

print 'your select sku: {}'.format(select_sku)

with open('input/css_select.csv', 'w') as file:
    writer = csv.writer(file)

    for sku, price in select_sku.items():
        writer.writerow([sku, price])

browser.quit()
