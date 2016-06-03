# -*- coding: utf-8 -*-
import csv
import operator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

browser = webdriver.Firefox()

browser.get('https://login.aliexpress.com/')

input("登录完成了请输入")

data = {}


def read_data(cate):
    if cate == '':
        return ()

    if cate not in data:
        url = 'http://datamatrix.aliexpress.com/categoryInfo.htm?categoryId={}&dateType=30'.format(cate)

        browser.get(url)

        fangkeshu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[2]").text
        liulanliang = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[3]").text
        zhifujine = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[4]").text
        zhifudingdanshu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[5]").text
        gongxuzhishu = browser.find_element(By.XPATH, "//table[@class='idy-int-tb-1']/tbody/tr[3]/td[6]").text

        data[cate] = (fangkeshu, liulanliang, zhifujine, zhifudingdanshu, gongxuzhishu)

    return data[cate]


def calc_data(*ds):
    return ('{}%'.format(reduce(operator.mul, [(float(d[0][:-1]) / 100) for d in ds if len(d) > 0], 1) * 100),
            '{}%'.format(reduce(operator.mul, [(float(d[1][:-1]) / 100) for d in ds if len(d) > 0], 1) * 100),
            '{}%'.format(reduce(operator.mul, [(float(d[2][:-1]) / 100) for d in ds if len(d) > 0], 1) * 100),
            '{}%'.format(reduce(operator.mul, [(float(d[3][:-1]) / 100) for d in ds if len(d) > 0], 1) * 100),
            [d[4] for d in ds if len(d) > 0][-1])


with open('output/ali_test_result.csv', 'w') as ofile:
    writer = csv.writer(ofile)

    with open('input/ali_industry.csv') as file:
        for one_text, two_text, three_text, four_text in csv.reader(file):

            try:

                browser.get('http://datamatrix.aliexpress.com/categorySelect.htm')

                one_select = Select(browser.find_element(By.NAME, 'oneSelect'))
                one_select.select_by_visible_text(one_text)

                two_cate, three_cate, four_cate = '', '', ''

                two_select = Select(browser.find_element(By.NAME, 'twoSelect'))
                if len(two_select.options) > 0:
                    two_select.select_by_visible_text(two_text)
                    two_cate = two_select.first_selected_option.get_attribute('value')

                three_select = Select(browser.find_element(By.NAME, 'threeSelect'))
                if len(three_select.options) > 0:
                    three_select.select_by_visible_text(three_text)
                    three_cate = three_select.first_selected_option.get_attribute('value')

                four_select = Select(browser.find_element(By.NAME, 'fourSelect'))
                if len(four_select.options) > 0:
                    four_select.select_by_visible_text(four_text)
                    four_cate = four_select.first_selected_option.get_attribute('value')

                print '#######################################################################################'
                two_cate_data = read_data(two_cate)
                three_cate_data = read_data(three_cate)
                four_cate_data = read_data(four_cate)
                final_cate_data = calc_data(two_cate_data, three_cate_data, four_cate_data)

                print one_text, two_text, '-', '-', ' '.join(map(str, two_cate_data))
                print one_text, two_text, three_text, '-', ' '.join(map(str, three_cate_data))
                print one_text, two_text, three_text, four_text, ' '.join(map(str, four_cate_data))
                print '---------------------------------------------------------------------------------------'
                print one_text, two_text, three_text, four_text, ' '.join(map(str, final_cate_data))

                writer.writerow((one_text, two_text, three_text, four_text) + final_cate_data)

                print '#######################################################################################'
                print ''

            except:

                print 'wrong: {} {} {} {}'.format(one_text, two_text, three_text, four_text)

browser.quit()
