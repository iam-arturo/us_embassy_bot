from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.keys import Keys
from time import sleep

def lambda_handler(event, context):

    email = os.environ['email']
    password = os.environ['password']

    print("v2")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://ais.usvisa-info.com/es-es/niv")

    elem = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[3]/div[2]/div[1]/div/a')
    elem.click();

    elem = driver.find_element_by_name("user[email]")
    elem.send_keys(email)

    driver.find_element_by_name("user[password]").send_keys(password)

    #sleep(1)
    elem = driver.find_element_by_xpath('//*[@id="policy_confirmed"]')
    driver.execute_script("arguments[0].click();", elem)


    driver.find_element_by_name("commit").click()

    sleep(1)
    driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click() # Continue
    #sleep(1)
    driver.find_element_by_xpath('//*[@id="forms"]/ul/li[4]').click() # Reprogram dte 1
    #sleep(1)
    driver.get("https://ais.usvisa-info.com/es-es/niv/schedule/31769104/appointment")
    sleep(1)
    driver.find_element_by_xpath('//*[@id="appointments_consulate_appointment_date"]').click() # Date of the date
    #sleep(1)

    driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[2]/div/a').click() # Next 1

    #sleep(1)
    driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[2]/div/a').click() # Next 2

    dates = {
#        'D16': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[3]/td[4]',
#        'D17': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[3]/td[5]',
#        'D18': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[3]/td[6]',
        'D19': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[3]/td[7]',
        'D20': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[4]/td[1]',
        'D21': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[4]/td[2]',
        'D22': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[4]/td[3]',
        'D23': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[4]/td[4]',
        'D24': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[4]/td[5]',
        'D25': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[4]/td[6]',
        'D26': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[4]/td[7]',
        'D27': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[5]/td[1]',
        'D28': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[5]/td[2]',
        'D29': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[5]/td[3]',
        'D30': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[5]/td[4]',
        'D31': '//*[@id="ui-datepicker-div"]/div[1]/table/tbody/tr[5]/td[5]',
        'J1': '//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[1]/td[6]',
        'J2': '//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[1]/td[7]',
        'J3': '//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[2]/td[1]',
        'J4': '//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[2]/td[2]',
#        'J5': '//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[2]/td[3]',
#        'J6': '//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[2]/td[4]',
#        'J7': '//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[2]/td[5]',
#        'J8': '//*[@id="ui-datepicker-div"]/div[2]/table/tbody/tr[2]/td[6]',
    }

    available_dates = []

    # Calendar
    # Class " undefined" means it is selectable

    for key in dates.keys():
        if driver.find_element_by_xpath(dates[key]).get_attribute("class") == " undefined":
            available_dates.append(key)

    if len(available_dates) != 0:
        print('DATES', available_dates)
        import boto3
        import json

        message = {"available_dates": available_dates}
        client = boto3.client('sns')
        response = client.publish(
            TargetArn="arn:aws:sns:us-east-2:136344217835:bot_us_embassy_topic",
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )    
    else:
        print('NO DATES AVAILABLE')

    driver.close()

    return available_dates
