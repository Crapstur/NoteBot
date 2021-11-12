#! /usr/bin/env python3

from selenium import webdriver
import json
import os
import sys
import datetime
import logging

logging.basicConfig(filename='/var/log/NoteBot/NoteBot.log', level=logging.INFO)
logging.warning(str(datetime.datetime.today()) + ' : NoteBot START')

os.chdir('/home/userbot/NoteBot/')

try:
    with open('credentials.json') as creds:
        credentials = json.load(creds)
except:
    sys.exit()

for cred in credentials:
    try:
        login_gpu = credentials[cred]['login']
        mdp_gpu = credentials[cred]['password']

        credmodif = cred.replace(" ", "_")
        path = "./notes/"+credmodif
        
        if not os.path.exists("./notes"):
            os.mkdir("./notes")
            logging.info(str(datetime.datetime.today()) + ' : Create folder [./notes]')
        
        if not os.path.exists(path):
            os.mkdir(path)
            logging.info(str(datetime.datetime.today()) + ' : Create folder for ' + str(cred))
        
        site = "https://intracursus2.unice.fr/"

        dir=os.getcwd()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        #options.add_argument("--window-size=1600,900")
        options.add_experimental_option('prefs', {
        "download.default_directory": path, #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome 
        })
        driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

        driver.maximize_window()

        driver.get(site)

        clique = driver.find_element_by_class_name('infoblue')
        clique.click()

        login = driver.find_element_by_id("username")
        login.send_keys(login_gpu)

        passwd = driver.find_element_by_id("password")
        passwd.send_keys(mdp_gpu)

        connect_btn = driver.find_element_by_class_name("btn-submit")
        connect_btn.click()

        tele=driver.find_element_by_xpath('//*[@id="content"]/form/input')
        tele.click()
        logging.info(str(datetime.datetime.today()) + ' : PDF download for ' + str(cred))
        driver.close()
    except:
        logging.error(str(datetime.datetime.today()) + ' : !! ERROR for ' + str(cred) + ' !!')

logging.warning(str(datetime.datetime.today()) + ' : NoteBot END')