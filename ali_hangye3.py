# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

browser = webdriver.Firefox()

browser.get('https://login.aliexpress.com/')

input("登录完成了请输入")

browser.get('http://datamatrix.aliexpress.com/categorySelect.htm')

one_select = Select(browser.find_element(By.NAME, 'oneSelect'))
for one_text in ['美容健康', '俄罗斯当地图书销售', '手表', '办公文教用品', '运动及娱乐', '孕婴童', '服装/服饰配件', '玩具', '工具', '珠宝饰品及配件', '电话和通讯', '家居用品']:
    one_select.select_by_visible_text(one_text)

    two_select = Select(browser.find_element(By.NAME, 'twoSelect'))
    for two_select_option in two_select.options:
        two_text, two_cate = two_select_option.text, two_select_option.get_attribute('value')
        two_select.select_by_visible_text(two_text)
        print one_text, two_text, '-', '-', 'http://datamatrix.aliexpress.com/categoryInfo.htm?categoryId={}&dateType=30'.format(two_cate)

        three_select = Select(browser.find_element(By.NAME, 'threeSelect'))
        for three_select_option in three_select.options:
            three_text, three_cate = three_select_option.text, three_select_option.get_attribute('value')
            three_select.select_by_visible_text(three_text)
            print one_text, two_text, three_text, '-', 'http://datamatrix.aliexpress.com/categoryInfo.htm?categoryId={}&dateType=30'.format(
                three_cate)

            four_select = Select(browser.find_element(By.NAME, 'fourSelect'))
            for four_select_option in four_select.options:
                four_text, four_cate = four_select_option.text, four_select_option.get_attribute('value')
                four_select.select_by_visible_text(four_text)
                print one_text, two_text, three_text, four_text, 'http://datamatrix.aliexpress.com/categoryInfo.htm?categoryId={}&dateType=30'.format(
                    four_cate)

browser.quit()
