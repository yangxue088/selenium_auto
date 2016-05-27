# -*- coding: utf-8 -*-
import csv
import sys

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

browser.get('http://sale.chinasalestore.com/wish/SelectItem.aspx')

reader = csv.reader(open("input/css_select.csv"))

idx = 0

for sku, price in reader:

    try:

        if idx % 2 == 0:
            account = 'KEHAN'
        else:
            account = 'RUIERSI'

        Select(browser.find_element(By.ID, 'txtaccount')).select_by_visible_text(account)

        browser.find_element(By.XPATH, "//span[contains(text(),'选择SKU')]").click()

        browser.switch_to.frame(browser.find_element(By.ID, 'iframecheckimage'))

        wait = WebDriverWait(browser, 60)

        wait.until(expected_conditions.element_to_be_clickable((By.ID, 'btnSearch')))

        browser.find_element(By.ID, 'txtKeyWord').send_keys(sku)
        browser.find_element(By.ID, 'btnSearch').click()

        wait.until(expected_conditions.element_to_be_clickable((By.NAME, 'radioSelect')))

        risks = browser.find_elements(By.XPATH, "//td/span")

        if len(risks) > 0:
            print 'account: {}, sku: {}, 自动忽略, 存在风险: {}'.format(account, sku, risks[0].text)
            browser.get('http://sale.chinasalestore.com/wish/SelectItem.aspx')
            continue

        browser.find_element(By.NAME, 'radioSelect').click()

        wait.until(expected_conditions.invisibility_of_element_located(()))

        browser.switch_to.default_content()

        browser.find_element(By.ID, 'popWinClose').click()

        browser.find_element(By.ID, 'Shipstarttime').clear()
        browser.find_element(By.ID, 'Shipstarttime').send_keys('14')
        browser.find_element(By.ID, 'Shipendtime').clear()
        browser.find_element(By.ID, 'Shipendtime').send_keys('21')

        row_count = browser.execute_script('''return $('#dg').datagrid('getData').total''')

        for i in xrange(row_count):
            browser.execute_script('''$('#dg').datagrid('beginEdit', {})'''.format(i))

            browser.execute_script('''var price=$('#dg').datagrid('getEditor',{{index:{}, field:'Price'}});
                                        $(price.target).numberbox('setValue', {});'''.format(i, price))

            browser.execute_script('''$('#dg').datagrid('endEdit', {})'''.format(i))

        is_kanden = input('account: {}, sku: {}, 是否刊登?'.format(account, sku))

        is_kanden = 1

        if int(is_kanden) == 1:
            print 'account: {}, sku: {}, 选择了刊登'.format(account, sku)

            browser.find_element(By.XPATH, "//span[contains(text(),'立即刊登')]").click()

            wait.until(expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@class='messager-body panel-body panel-body-noborder window-body']/div")))

            text = browser.find_element(By.XPATH, "//div[@class='messager-body panel-body panel-body-noborder window-body']/div").text

            browser.find_element(By.XPATH, "//span[contains(text(), '确定')]").click()

            if '刊登成功' in text:
                idx += 1
                print 'account: {}, sku: {}, 上传结果: 成功, 反馈: {}'.format(account, sku, text)
            elif '重复刊登' in text:
                print 'account: {}, sku: {}, 上传结果: 失败, 反馈: 重复刊登'.format(account, sku)
        else:

            print 'account: {}, sku: {}, 选择了忽略'.format(account, sku)

    except:

        print 'sku: {}, 出现错误, 上传结果: 失败'.format(sku)

        raise

browser.quit()
