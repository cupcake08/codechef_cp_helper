from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from colorama import Fore
import argparse
import os
import stat

# add url to your temple c++ file
TEMPLATE_CPP_FILE = "/home/ankit/CP/template.cpp"

# init argument parse
parser = argparse.ArgumentParser(description="Codechef Contest Helper")

# Adding optional arguments
# contest Id
parser.add_argument('-c', '--contest', help="Contest Id", required=True)

# directory in which you want to make your project
parser.add_argument('-d', '--dir', help="Give the directory", default=".")

# Read arguments from command line
args = parser.parse_args()

# change the directory
os.chdir(args.dir)

firefox_options = Options()

URI = "https://www.codechef.com/"

firefox_options.binary_location = "/usr/bin/firefox"

# for making all actions silent (prefer to be not)
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)

# driver.get(URI)


def login():
    css = 'm-login-button-no-border'
    e = driver.find_element(By.CLASS_NAME, css)
    e.click()
    inpt = driver.find_element(
        By.CSS_SELECTOR, '#ajax-login-form > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
    # username
    inpt.send_keys("")
    pswd = driver.find_element(By.CSS_SELECTOR, '.password-login')
    # password
    pswd.send_keys("")
    hide = driver.find_element(By.CSS_SELECTOR, '.toggle-password-login')
    hide.click()
    sub = driver.find_element(By.XPATH, '//*[@id="ajax-login-form"]')
    sub.submit()


# login()

driver.get(URI + args.contest)

try:
    path = '/html/body/div[1]/div/main/section/div[2]/div/div/div[2]/div[2]/table'
    e = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, path)))
    element = driver.find_element(By.XPATH, path)
    problems = element.find_element(
        By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
except:
    driver.quit()
    os.abort()

p_links = []

for i in problems:
    p = i.find_element(By.CSS_SELECTOR, 'td:nth-child(1)')
    pc = i.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > div:nth-child(1)')
    link = p.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > span > a')
    p_links.append((p.text, link.get_attribute('href'), pc.text))

os.mkdir(args.contest, mode=stat.S_IRWXU)
os.chdir(args.contest)


def make_file(filename, pname):
    t = datetime.now()
    s = f'''/**
     * Author     : Ankit Bhankharia (cup_cake_07)
     * Created At : {t.day}-{t.month}-{t.year} {t.hour}:{t.minute}:{t.second}
     * Problem    : {pname}
**/\n\n'''

    with open(filename, 'w') as f:
        f.write(s)
        with open(TEMPLATE_CPP_FILE, 'r') as template:
            lines = template.readlines()
            f.writelines(lines)


for idx, i in enumerate(p_links):
    print(f"working on problem: {Fore.MAGENTA + i[0]}")
    folder = str(chr(ord('A') + idx))
    os.mkdir(folder, mode=stat.S_IRWXU)
    os.chdir(folder)
    # make files
    make_file(f"{i[2]}.cpp", i[0])
    driver.get(i[1])
    try:
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '._values__container_10hzz_207')))
    except:
        driver.quit()

    inpt = driver.find_element(
        By.CSS_SELECTOR, 'div._values_10hzz_207:nth-child(1) > pre:nth-child(1)')
    output = driver.find_element(
        By.CSS_SELECTOR, 'div._values_10hzz_207:nth-child(2) > pre:nth-child(1)')

    with open('input.txt', 'w') as inputF:
        inputF.write(inpt.text)
    with open('output.txt', 'w') as outputF:
        outputF.write(output.text)

    os.chdir('..')
