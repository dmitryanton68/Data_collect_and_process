#1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
# сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

#  Скрипт захродит в почтовый ящик и показывает непрочитанные письма.

driver = webdriver.Chrome()
driver.get('https://mail.ru/')

email = 'no.name.08.2019@mail.ru'
pwd = 'without-pwd'

email_input = driver.find_element_by_id('mailbox:login')
email_input.send_keys(email)

driver.implicitly_wait(2)

password_input = driver.find_element_by_id('mailbox:password')
password_input.send_keys(pwd, Keys.RETURN)

submit_input = driver.find_element_by_id('mailbox:submit').find_element_by_class_name('o-control')
submit_input.send_keys(Keys.ENTER)

sleep(10)

filter_button = driver.find_element_by_css_selector('.filters-control.filters-control_short.filters-control_pure')
filter_button.click()

sleep(5)

filter_unread_letter = driver.find_element_by_xpath(".//div[@class='select__items select__items_expanded']//div[2]//span[2]")
filter_unread_letter.click()

sleep(2)

all_emails = driver.find_elements_by_xpath(".//div[@class='dataset-letters']")
print(f'{all_emails}')
