# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

browser = webdriver.Firefox()

browser.get('https://login.aliexpress.com/')

input("登录完成了请输入")

browser.get('http://datamatrix.aliexpress.com/categorySelect.htm')

one_select = Select(browser.find_element(By.NAME, 'oneSelect'))
for one_text in ['家具和室内装饰品', '家居用品', '食品', '五金', '工具', '建筑', '照明灯饰']:
    one_select.select_by_visible_text(one_text)

    two_select = Select(browser.find_element(By.NAME, 'twoSelect'))
    for two_select_option in two_select.options:
        two_text, two_cate = two_select_option.text, two_select_option.get_attribute('value')
        two_select.select_by_visible_text(two_text)
        print '{}^{}^{}^{}^{}'.format(one_text, two_text, '-', '-',
                                      'http://datamatrix.aliexpress.com/categoryInfo.htm?categoryId={}&dateType=30'.format(two_cate))

        three_select = Select(browser.find_element(By.NAME, 'threeSelect'))
        for three_select_option in three_select.options:
            three_text, three_cate = three_select_option.text, three_select_option.get_attribute('value')
            three_select.select_by_visible_text(three_text)
            print '{}^{}^{}^{}^{}'.format(one_text, two_text, three_text, '-',
                                          'http://datamatrix.aliexpress.com/categoryInfo.htm?categoryId={}&dateType=30'.format(
                                              three_cate))

            four_select = Select(browser.find_element(By.NAME, 'fourSelect'))
            for four_select_option in four_select.options:
                four_text, four_cate = four_select_option.text, four_select_option.get_attribute('value')
                four_select.select_by_visible_text(four_text)
                print '{}^{}^{}^{}^{}'.format(one_text, two_text, three_text, four_text,
                                              'http://datamatrix.aliexpress.com/categoryInfo.htm?categoryId={}&dateType=30'.format(
                                                  four_cate))

browser.quit()
