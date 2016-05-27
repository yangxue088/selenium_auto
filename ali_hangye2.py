# -*- coding: utf-8 -*-
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

browser = webdriver.Firefox()

browser.get('https://login.aliexpress.com/')

input("登录完成了请输入")

browser.get('http://datamatrix.aliexpress.com/categorySelect.htm')

frame = browser.find_element(By.XPATH, "//div[contains(@class, 'cate-selector-content')]/iframe")
browser.execute_script("arguments[0].setAttribute('src', '{}')".format(frame.get_attribute('_src')), frame)

browser.execute_script("arguments[0].setAttribute('style', '{}')".format('visibility: visible; left: 129px; top: 32px;'),
                       browser.find_element(By.CLASS_NAME, 'cate-selector-content'))

browser.switch_to.frame(frame)

with open('input/ali_lanhai.csv') as file:

    for one_cate, two_cate, three_cate, four_cate in csv.reader(file):
        one_select = Select(browser.find_element(By.NAME, 'oneSelect'))
        for one_cate in ['手表']:
            one_select.select_by_visible_text(one_cate)

            two_select = Select(browser.find_element(By.NAME, 'twoSelect'))
            for two_select_option in two_select.options:
                two_text, two_cate = two_select_option.text, two_select_option.get_attribute('value')
                two_select.select_by_visible_text(two_cate)

                three_select = Select(browser.find_element(By.NAME, 'threeSelect'))
                for three_select_option in three_select.options:
                    three_text, three_cate = three_select_option.text, three_select_option.get_attribute('value')
                    three_select.select_by_visible_text(three_cate)

                    four_select = Select(browser.find_element(By.NAME, 'fourSelect'))
                    for four_select_option in four_select.options:
                        four_text, four_cate = four_select_option.text, four_select_option.get_attribute('value')
                        four_select.select_by_visible_text(four_cate)

    Select(browser.find_element(By.NAME, 'twoSelect')).select_by_visible_text('怀表')

browser.switch_to.default_content()

Select(browser.find_element(By.XPATH, "//span[@class='idy-int-t-2']/select")).select_by_visible_text('最近30天')

fangkeshu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[2]").text
liulanliang = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[3]").text
zhifujine = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[4]").text
zhifudingdanshu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[5]").text
gongxuzhishu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[6]").text

print fangkeshu, liulanliang, zhifujine, zhifudingdanshu, gongxuzhishu

# browser.quit()
