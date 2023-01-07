from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import argparse
import os
import stat

# add url to your temple c++ file
TEMPLATE_CPP_FILE = "/home/ankit/CP/template.cpp"

# init argument parse
parser = argparse.ArgumentParser(description="Codechef Contest Helper")

# Adding optional arguments
parser.add_argument('-c', '--contest', help="Contest Id", required=True) # contest id

#directory in which you want to make your project
parser.add_argument('-d','--dir',help="Give the directory",default=".")

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

driver.get(URI + args.contest)

element = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/section/div[2]/div/div/div[2]/div[2]/table')

problems = element.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

p_links = []

for i in problems:
    p = i.find_element(By.CSS_SELECTOR, 'td:nth-child(1)')
    pc = i.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > div:nth-child(1)')
    link = p.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > span > a')
    p_links.insert(0, (p.text, link.get_attribute("href"), pc.text))

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
            print(lines)
            f.writelines(lines)


for i in p_links:
    print(f"opening {i[0]} in seperate window")
    # make files
    make_file(f"{i[2]}.cpp", i[0])
    driver.execute_script(f"window.open('{i[1]}');")
    # TODO
    # work on single file
    # make files with input and output files.
