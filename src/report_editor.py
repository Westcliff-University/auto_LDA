import os
import pandas as pd
import time
from contextlib import chdir
from datetime import datetime, timedelta
from platform import platform
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from shutil import rmtree
from edit_query import edit_query
from get_FA_ids import get_FA_ids
from move_latest_csv import move_latest_csv
from n_splits import n_splits
import subprocess

COMTROL = None # It's named moronically for a reason
if 'Window' in platform():
    COMTROL = Keys.CONTROL
else:
    COMTROL = Keys.COMMAND

def add_to_clipboard(text):
    command = 'echo ' + text + '| clip'
    os.system(command)

class report_editor():
    def __init__(self, report_name, report_url, query_file, dl_url, 
                 domestic, num_splits, time_restriction, need_id_filter,
                 username, password):
        self.report_name = report_name
        self.report_url = report_url
        self.query_file = query_file
        self.dl_url = dl_url
        self.domestic = domestic
        self.num_splits = num_splits
        self.time_restriction = time_restriction
        self.need_id_filter = need_id_filter
        self.username = username
        self.password = password

        self.gap_url = 'https://gap.westcliff.edu/'

        self.dir_name = '../data/' + self.report_name + "-" + datetime.today().strftime('%Y-%m-%d')

        if os.path.exists(self.dir_name):
            rmtree(self.dir_name)
        os.makedirs(self.dir_name)
        options = Options()
        options.set_preference("browser.download.dir", self.dir_name)
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        self.driver = webdriver.Firefox(options=options)
        

    def quit(self):
        self.driver.quit()

    def login_to_gap(self):       
        self.driver.get(self.gap_url)
        time.sleep(1)
        username = self.driver.find_element(By.ID, 'inputName')
        username.clear()
        # TODO: Make these OS_ENV variables or whatever they're called
        username.send_keys(self.username)
        password = self.driver.find_element(By.ID, 'inputPassword')
        password.clear()
        password.send_keys(self.password)
        # login_button = self.driver.find_element(By.NAME, 'loginbtn')
        password.send_keys(Keys.RETURN)
        time.sleep(1)

    def fetch_GAP_report(self):
        ids = get_FA_ids(self.domestic)
        split_list_of_ids = n_splits(ids, self.num_splits)
        sql_id_strings = []
        # print(f'Expected number of files: {len(split_list_of_ids)}')
        lower_bound = (datetime.today() - timedelta(days = 16)).strftime('%Y-%m-%d')
        
        for l in split_list_of_ids:
            try:
                self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[1]/button/i').click()
            except:
                1
            self.driver.get(self.report_url) 
            time.sleep(0.5)
            ActionChains(self.driver)\
                .key_down(Keys.DELETE)\
                .key_down(COMTROL)\
                .send_keys("a")\
                .key_down(Keys.BACK_SPACE)\
                .send_keys(Keys.DELETE)\
                .send_keys(Keys.DELETE)\
                .perform()
            id_string = ""
            for sid in l:
                id_string += "\"" + str(sid) + "\","
            id_string = "AND u.username IN (" + str(id_string[:-1]) + ")"

            replacements = []
            if self.need_id_filter:
                replacements.append(id_string)
            if self.time_restriction:
                replacements.append(f'AND DATE_FORMAT(FROM_UNIXTIME(l.timecreated),\'%Y-%m-%d %H:%i\') > \'{lower_bound}\'') 
            q = edit_query(self.query_file, replacements)

            if 'Window' in platform():

                with open("q.txt", "w") as f:
                    f.write(q)
                    f.close()
                    q_path = os.path.abspath("q.txt")
                    process = subprocess.run(
                        ["powershell.exe", "-Command", f"Get-Content {q_path} | Set-Clipboard"],
                        capture_output=True,
                        check=True,
                        text=True,
                        encoding="utf-8"
                    )

            else:
                subprocess.run("pbcopy", text = True, input = q)

            ActionChains(self.driver)\
                .key_down(COMTROL)\
                .send_keys("v")\
                .perform()
            
            self.driver.find_element(By.ID, 'id_submitbutton').click()
            time.sleep(7)
            # This is the tricky gap where sometimes the report takes forever to save... What's the solution?
            self.driver.get(self.dl_url)
            time.sleep(2) # Without this one, sometimes you might run into "Repository Unreachable" error  

            # There are browser extensions for finding XPaths, so you don't always have to right click Inspect Element etc.
            if not "No records found" in self.driver.page_source:
                try:
                    self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[4]/div[2]/div[3]/div/section/div/div[3]/a').click()
                except:
                    self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/div[3]/div/section/div/form[1]/table/tbody/tr[5]/td[6]/a[1]').click()
                
                time.sleep(8) # Provides an extra delay to make sure the file actually downloads.
                # There is a tradeoff between decreasing this time sleep and decreasing num_splits.

                move_latest_csv(self.dir_name, os.environ.get('DOWNLOADS_DIR'))
            
        with chdir(self.dir_name):
            df = pd.concat([pd.read_csv(f) for f in os.listdir() if os.path.getsize(f)], axis = 0)

        if 'Window' in platform():
            data_dir = os.path.abspath(os.pardir + '\\data')
        else:
            data_dir = "../data"
        if 'Window' in platform():
            os.makedirs(os.path.abspath(os.pardir + f'\\data\\output-{datetime.today().strftime('%Y-%m-%d')}'),exist_ok=True)
            df.to_csv(f'{data_dir}\\{self.report_name}.csv', index = 0)
        else:
            os.makedirs(os.path.abspath(os.pardir + f'/data/output-{datetime.today().strftime('%Y-%m-%d')}'),exist_ok=True)
            df.to_csv(f'../data/output-{datetime.today().strftime('%Y-%m-%d')}/{self.report_name}.csv', index = 0)