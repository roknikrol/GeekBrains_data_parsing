from selenium import webdriver  # imports chrome webdriver
from selenium.webdriver.chrome.options import Options # add options customization
from selenium.webdriver.common.keys import Keys # use keyboard keys
from selenium.webdriver.support.ui import WebDriverWait # add feature to wait for page loading
from selenium.webdriver.support import expected_conditions as EC # add expected conditions for WebWaiting
from selenium.webdriver.common.by import By # extra search module
from selenium.webdriver.common.action_chains import ActionChains # multiple actions for page browsing
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
#main selenium settings
opera_options = Options()
opera_options.add_argument('start-maximized')
driver = webdriver.Opera(options=opera_options)

# get inside th mailbox
driver.get("https://mail.ru")
elem = driver.find_element_by_id("mailbox:login")
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.RETURN)
# button = WebDriverWait(elem, 5).until(
#     EC.presence_of_element_located((By.CLASS_NAME,
#                                     'btn btn_blue mailbox__control mailbox__control_twostep mailbox__rwd-control mailbox__control_twostep-short'))
# )
elem = driver.find_element_by_id("mailbox:password")
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

# iterating over scrollable list of emails
emails_data = []
email_dict = {}
page = 1 #
time.sleep(10)
while page < 5: # for test purposes - only 5 pages
    emails = driver.find_elements_by_class_name("ll-sj__normal")
    actions = ActionChains(driver)
    for email in emails:
        email.click()
        # button = WebDriverWait(driver, 6).until(email.find_element_by_xpath("//div/h2[@class='thread__subject']"))
        # time.sleep(15)
        print(email.find_element_by_xpath("//div/h2[@class='thread__subject']/text()")) # ЗДЕСЬ ВЫХОДИТ ОШИБКА StaleElementReferenceException
        # email_dict['header'] = email.find_element_by_xpath("//div/h2[@class='thread__subject']/text()")
        # email_dict['from'] = email.find_element_by_class_name("letter-contact letter-contact_active").value_of_css_property("title").text
        # email_dict['when'] = email.find_element_by_class_name("letter__date").text
        # email_dict['body'] = email.find_element_by_class_name("webkit_mailru_css_attribute_postfix").text
        emails_data.append(email_dict)
        email.back()
    actions.move_to_element(emails[-1])
    actions.perform()
    page += 1
print(emails_data)

# driver.quit()