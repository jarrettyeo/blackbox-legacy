from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

import pathlib # mkdir
import urllib # to parse strings into %-coded urlsafe strings
import time # for explicitly waiting
import re # regex

import os
import glob
import shutil
import sys

def cleanify(string_to_clean):
    # basic string function to create legal folder/file names
    return re.sub("[^\w_.)( -]", " ", string_to_clean.strip())

BLACKBOARD_USERNAME = "REPLACE_ME"
BLACKBOARD_PASSWORD = "REPLACE_ME"

if sys.platform == "win32": # Windows users

    # CHROMEDRIVER_PATH needs to be your working directory
    CHROMEDRIVER_PATH = "REPLACE_ME" # e.g. "C:/Users/Jarrett/Dropbox/NTU/Jarrett/Blackbox/"
    BLACKBOARD_MAIN_PATH = CHROMEDRIVER_PATH + "Blackbox/"
    BLACKBOARD_DOWNLOAD_PATH = BLACKBOARD_MAIN_PATH + "Downloads/"

else: # Mac users

    # CHROMEDRIVER_PATH needs to be your working directory
    CHROMEDRIVER_PATH = "REPLACE_ME" # e.g. "/Users/Jarrett/Dropbox/NTU/Jarrett/Blackbox/"
    BLACKBOARD_MAIN_PATH = CHROMEDRIVER_PATH + "Blackbox/"
    BLACKBOARD_DOWNLOAD_PATH = BLACKBOARD_MAIN_PATH + "Downloads/"

shutil.rmtree(BLACKBOARD_DOWNLOAD_PATH, ignore_errors=True)
pathlib.Path(BLACKBOARD_MAIN_PATH).mkdir(exist_ok=True)
pathlib.Path(BLACKBOARD_DOWNLOAD_PATH).mkdir(exist_ok=True)

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : BLACKBOARD_DOWNLOAD_PATH,
        'download.prompt_for_download': False,
        'plugins.always_open_pdf_externally': True,}
chrome_options.add_experimental_option('prefs', prefs)

# We'll use Chromedriver 2.36
if sys.platform == "win32": # Windows
    driver = webdriver.Chrome(CHROMEDRIVER_PATH  + "chromedriver.exe", chrome_options=chrome_options)
else: # Mac
    driver = webdriver.Chrome(CHROMEDRIVER_PATH  + "chromedriver", chrome_options=chrome_options)

# driver = webdriver.Chrome(BLACKBOARD_MAIN_PATH)
driver.get("https://ntulearn.ntu.edu.sg/webapps/login/")

# when you assert something, you tell the program to test if the condition is true.
# if it isn't (i.e. condition is false), trigger an error.
assert "Blackboard" in driver.title

# we find the email field here.
email_field = driver.find_element_by_id("user_id")
email_field.clear() # we clear the field just in case
email_field.send_keys(BLACKBOARD_USERNAME)

# we find the password field here.
password_field = driver.find_element_by_id("password")
password_field.clear() # we clear the field just in case
password_field.send_keys(BLACKBOARD_PASSWORD)

# in Selenium, it is common to use the try-except block to try navigating to a new page.
# if it isn't successful (usually a timeout error will be thrown, i.e. page taking too long to load),
# the program will exit try and execute the code under except.
try:
    # lazy way of logging in by hitting enter.
    # alternatively, you could find the "Sign In" button and use the click function.
    email_field.send_keys(Keys.RETURN)
except:
    wait = WebDriverWait(driver, 10)
    # EC is the Expected Condition that we are looking out for.
    # in this case, we are looking out for when the URl changes to udemy.com,
    # thereby indicating that you have successfully logged in.
    # of course that it is not the only way to check if you have logged in successfully.
    home_page = wait.until(EC.url_to_be("https://ntulearn.ntu.edu.sg/webapps/portal/execute/tabs/tabAction"))


driver.get("https://ntulearn.ntu.edu.sg/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_13_1")
assert "Courses" in driver.title

element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "courseInformation")))
# wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'a')))

courses = driver.find_element_by_class_name("courseListing").find_elements_by_tag_name("li")
# print(courses)

course_title_list = []
course_url_list = []

course_id_list = []
course_counter = -1

for course in courses:
    
    print(course.find_element_by_tag_name('a').text)
    course_title_list.append(course.find_element_by_tag_name('a').text)

    print(course.find_element_by_tag_name('a').get_attribute("href"))
    course_url_list.append(course.find_element_by_tag_name('a').get_attribute("href"))

for course_url in course_url_list:

    course_counter += 1

    print("course_url:", course_url)
    print("course_counter:", course_counter)

    driver.get(course_url)

    pages = driver.find_element_by_class_name("courseMenu").find_elements_by_tag_name("li")
    
    page_title_list = []
    page_url_list = []

    print(driver.find_element_by_class_name('courseId').text)
    course_id_list.append(driver.find_element_by_class_name('courseId').text)

    course_id = course_id_list[course_counter]
    print("course_id:", course_id)

    COURSE_FOLDER_PATH = BLACKBOARD_MAIN_PATH + cleanify(course_id) + '/'

    pathlib.Path(COURSE_FOLDER_PATH).mkdir(exist_ok=True)
    print("COURSE_FOLDER_PATH:", COURSE_FOLDER_PATH)

    for page in pages:

        if not page.get_attribute("class") == "clearfix divider": 

            print(page.find_element_by_tag_name('span').text)
            page_title_list.append(page.find_element_by_tag_name('a').text)
            
            print(page.find_element_by_tag_name('a').get_attribute("href"))
            page_url_list.append(page.find_element_by_tag_name('a').get_attribute("href"))
        
    page_counter = -1

    for page_url in page_url_list:

        page_counter +=1

        driver.get(page_url)

        content_page = driver.find_elements_by_class_name("contentList")

        # print("content_page:", content_page)
        
        if content_page: # if is a content page 

            contents = driver.find_element_by_class_name("contentList").find_elements_by_tag_name("a")

            file_title_list = []
            file_url_list = []
            subfolder_title_list = []
            subfolder_url_list = []
            
            for content in contents: # if content page is not empty

                if "/webapps/blackboard/content/listContent.jsp" in content.get_attribute("href"):

                    # is subfolder

                    subfolder_url_list.append(content.get_attribute("href"))
                    subfolder_title_list.append(content.text)

                elif "/bbcswebdav/" in content.get_attribute("href"):

                    # is file

                    file_url_list.append(content.get_attribute("href"))
                    file_title_list.append(content.text)

            # contents = driver.find_element_by_class_name("contentList").find_elements_by_tag_name("li")

            # file_title_list = []
            # file_url_list = []
            # subfolder_title_list = []
            # subfolder_url_list = []
            
            # for content in contents: # if content page is not empty

            #     if "/webapps/blackboard/content/listContent.jsp" in content.find_element_by_tag_name("a").get_attribute("href"):

            #         # is subfolder

            #         subfolder_url_list.append(content.find_element_by_tag_name("a").get_attribute("href"))
            #         subfolder_title_list.append(content.find_element_by_tag_name("a").text)

            #     elif "/bbcswebdav/" in content.find_element_by_tag_name("a").get_attribute("href"):

            #         # is file

            #         file_url_list.append(content.find_element_by_tag_name("a").get_attribute("href"))

            #         file_title_list.append(content.find_element_by_tag_name("a").text)

            if subfolder_url_list or file_url_list:

                PAGE_FOLDER_PATH = COURSE_FOLDER_PATH + cleanify(page_title_list[page_counter]) + '/'

                shutil.rmtree(PAGE_FOLDER_PATH, ignore_errors=True)
                # pathlib.Path(PAGE_FOLDER_PATH).rmdir()
                pathlib.Path(PAGE_FOLDER_PATH).mkdir(exist_ok=True)

                # download files

                file_counter = -1

                for file_url in file_url_list:

                    file_counter += 1

                    driver.get(file_url)
                    time.sleep(5)

                # check if all files have finished downloading

                countdown_timer = 0

                while True:

                    all_downloaded = True
                    countdown_timer += 1
                    print("countdown_timer:", countdown_timer)

                    for downloading_file in os.listdir(BLACKBOARD_DOWNLOAD_PATH):
                        if downloading_file.endswith(".crdownload"):
                            all_downloaded = False
                            time.sleep(3)

                            if countdown_timer == 6: # give up waiting for 15 seconds on files which are still downloading and kills them all
                                print("killing all unfinished downloads")
                                pathlib.Path(BLACKBOARD_DOWNLOAD_PATH + downloading_file).unlink()

                    if all_downloaded == True:
                        print("all files downloaded!")
                        break

                for file in glob.glob(os.path.join(BLACKBOARD_DOWNLOAD_PATH, '*.*')):
                    shutil.copy(file, PAGE_FOLDER_PATH)
                print("transfer completed!")

                shutil.rmtree(BLACKBOARD_DOWNLOAD_PATH, ignore_errors=True)
                # pathlib.Path(BLACKBOARD_DOWNLOAD_PATH).rmdir()
                pathlib.Path(BLACKBOARD_DOWNLOAD_PATH).mkdir(exist_ok=True)

# finally, we quit the webdriver
driver.close()
print("all downloads completed!\n")