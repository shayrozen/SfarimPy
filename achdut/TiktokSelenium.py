# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 12:19:07 2023

@author: U301901
"""

import os
os.chdir('C://Users//u301901//Documents//GitHub//SfarimPy//')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import json
from PyPDF2 import PdfReader
from selenium.webdriver.common.action_chains import ActionChains
import time



driver = webdriver.Chrome()
driver.maximize_window()
link = 'https://www.tiktok.com/@idf.atal' #Main
driver.get(link)


try: #finding the robot captcha
    element = driver.find_element(By.CSS_SELECTOR, "[class*='verify']")
except NoSuchElementException:
    print("Error: Verification is not needed right now")
else:
    print("Error: stop, Verification is needed")


try:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element = driver.find_element(By.CSS_SELECTOR, "[class*='DivThreeColumnContainer']")
    all_children = element.find_elements(By.XPATH, "*")
    all_children = all_children[0].find_elements(By.XPATH, "*")
    linkLst = []
    playsLst = []
    
    for video in all_children:
        action = ActionChains(driver) # Move the mouse to the element to hover
        action.move_to_element(video) # Perform the hover action
        action.perform()
        videoElement = video.find_element(By.CSS_SELECTOR, "[id*='xgwrapper']")
        idText = videoElement.get_attribute("id").split('-')[2]
        linkLst.append("https://www.tiktok.com/@idf.atal/video/{}".format(idText))
        playsCount = driver.find_element(By.CSS_SELECTOR, "[class*='video-count']").text
        playsLst.append(playsCount)
        if len(linkLst)%10==0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(len(linkLst))
    print("Success!")
except NoSuchElementException:
    print("Error: Something Happened")    


postDicts = {}
i=0
try:
    for link in linkLst:
        driver.get(link)
        time.sleep(3)
        #comments = int(driver.find_element(By.CSS_SELECTOR, "[class*='PCommentTitle']").text.split(" ")[0])
        i+=1
        try:
            spanText = driver.find_element(By.CSS_SELECTOR, "[class*='SpanText']").text
            postDicts[i]["spanText"] = spanText
        except:
            print("no span text")
        actionBar = driver.find_element(By.CSS_SELECTOR, "[class*='DivActionBarWrapper']").text.split('\n')
        likes, comments, saved, shares = actionBar
        postDicts[i] = {}
        postDicts[i]["likes"] = likes
        postDicts[i]["comments"] = comments
        postDicts[i]["saved"] = saved
        postDicts[i]["shares"] = shares
        StyledCommonLinks = driver.find_elements(By.CSS_SELECTOR, "[class*='StyledCommonLink']")
        tags = [tag.text for tag in StyledCommonLinks]
        postDicts[i]["tags"] = tags
        
        #to do: capture all recursive comment section
        #to do: save and cast the date of publish
except NoSuchElementException:
    print("Error: Something Happened")    
 



    
    
    try: #finding the loginContainer 
        element = driver.find_element(By.CSS_SELECTOR, "[id*='loginContainer']")
        element = driver.find_element(By.CSS_SELECTOR, "[class*='DivCloseWrapper']").click()
    except NoSuchElementException:
        print("Error: Login is not needed")
    else:
        print("Login Closed Successfully")

    
    
    
    






