# -*- coding: utf-8 -*-
import csv
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Firefox()

browser.get('http://www.dianxiaomi.com')

browser.find_element_by_name('account').send_keys(sys.argv[1])
browser.find_element_by_name('password').send_keys(sys.argv[2])
browser.find_element_by_class_name('btn-denglu').click()

browser.get('http://www.dianxiaomi.com/product/index.htm')

with open("input/dxm_price.csv") as file:
    for sku, dec_price in csv.reader(file):

        old_prices = []
        new_prices = []

        try:
            wait = WebDriverWait(browser, 60)

            browser.find_elements_by_xpath("//div[@class='col-xs-10 pTop10']/a[contains(text(),'产品ID')]")[0].click()

            wait.until(expected_conditions.invisibility_of_element_located((By.XPATH, "//body[contains(@class, 'modal-open')]")))

            browser.find_elements_by_xpath("//div[@class='col-xs-10 pTop10']/a[contains(text(),'KEHAN')]")[0].click()

            wait.until(expected_conditions.invisibility_of_element_located((By.XPATH, "//body[contains(@class, 'modal-open')]")))

            browser.find_element_by_id('searchValue').send_keys(sku)

            browser.find_element_by_id('btnSearch').click()

            wait.until(expected_conditions.invisibility_of_element_located((By.XPATH, "//body[contains(@class, 'modal-open')]")))

            body = browser.find_element(By.XPATH, "//table[@class='myj-table']/tbody")

            if not body.text:
                print '产品ID: {}, 找不到产品, 自动忽略'.format(sku, dec_price)
                continue

            product = body.find_element(By.XPATH, 'tr[1]/td[10]/a[1]')

            product.click()

            origin = browser.current_window_handle

            browser.switch_to.window(browser.window_handles[1])

            wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//a[contains(@data-val, 'priced')]")))

            for element in browser.find_elements(By.NAME, 'priced'):
                old_prices.append(element.get_attribute('value'))

            browser.find_element(By.XPATH, "//a[contains(@data-val, 'priced')]").click()

            browser.find_element(By.XPATH, "//input[@id='price1']").send_keys(dec_price)
            browser.find_element(By.XPATH, "//div[contains(@id, 'batchAdjustPriceModal')]//button[contains(text(),'确定')]").click()

            for element in browser.find_elements(By.NAME, 'priced'):
                new_prices.append(element.get_attribute('value'))

            browser.find_element(By.XPATH, "//button[contains(text(),'更新至')]").click()

            wait.until(expected_conditions.visibility_of_element_located((By.ID, "msgModal")))

            browser.close()

            browser.switch_to.window(origin)

            print '产品ID: {}, 调整价格: {}, 结果: 成功, 原价格: {}, 新价格: {}'.format(sku, dec_price, old_prices, new_prices)
        except:

            print '产品ID: {}, 调整价格: {}, 结果: 失败, 原价格: {}, 新价格: {}'.format(sku, dec_price, old_prices, new_prices)

            raise

browser.quit()
