# -*- coding: utf-8 -*-
import os
os.chdir('C://Users//u301901//Documents//GitHub//SfarimPy//')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import json
from PyPDF2 import PdfReader

global sfarim; sfarim = {}



def findPasukNum(p):
    pList = p.split(' ')
    pList = list(filter(lambda teva: teva!= '', pList))
    Num = pList[0]
    index = p.find(Num)
    return index, Num
    

def fetchContent(sefer, href=None):
    if href:
        driver.get(href)
    perek = driver.find_element(By.CLASS_NAME, "mainTxt > h1").text.split()[-1]
    content = driver.find_element(By.CLASS_NAME, "contentCantill")
    txt = content.text
    txt = re.sub('{פ}', "", txt)
    txt = re.sub('{ש}', "", txt)
    txt = re.sub('{ס}', "", txt)
    txt = re.sub('{ר}', "", txt)
    txt = re.sub('\n', "", txt)
    txt = txt.split('.')
    
    for p in txt:
        p = p.strip()
        if p != '':
            pasukNumIndex, pasukNum = findPasukNum(p)
            pasuk = ' '.join(p.split(' ')[1:])
            sfarim[sefer][perek][pasukNum] = pasuk
    


driver = webdriver.Chrome()
driver.maximize_window()

torahLink = 'https://kodesh.snunit.k12.il/i/tr/t0100.htm'
neveiimLink = 'https://kodesh.snunit.k12.il/i/tr/t0600.htm'
ktuvimLink = 'https://kodesh.snunit.k12.il/i/tr/t25a00.htm'
helekLinks = [torahLink, neveiimLink, ktuvimLink]

for link in helekLinks:
    driver.get(link)
    seferElement = driver.find_element(By.CLASS_NAME, "biblist")
    all_children = seferElement.find_elements(By.CSS_SELECTOR, "*")
    sfraimHref = [child.get_attribute("href") for child in all_children]
    sfraimHref = list(filter(lambda k: k != None, sfraimHref))
    
    for seferLink in sfraimHref:    
        driver.get(seferLink)
    # driver.get("https://kodesh.snunit.k12.il/i/tr/t0101.htm")
        sefer = driver.find_element(By.CLASS_NAME, "mainTxt > h1").text[:-2]
        try:
            prakimElement = driver.find_element(By.CLASS_NAME, "prakimLine")
            all_children = prakimElement.find_elements(By.XPATH, "*")
            prakimHref = [child.get_attribute("href") for child in all_children]
            sfarim[sefer] = {}
            for perek in prakimElement.text.split()[1:]:
                sfarim[sefer][perek] = {}
            
            fetchContent(sefer)
            for perekLink in prakimHref:
                fetchContent(sefer, perekLink)
                
        except:
            sfarim[sefer] = {}
            sfarim[sefer]['א'] = {}
            fetchContent(sefer)
            
      
            
# =========================== nikud ================================================== #      

def remove_niqqud_from_string(my_string):
    return ''.join(['' if  1456 <= ord(c) <= 1479 else c for c in my_string])

sfarimT = {}



# =========================== PDF ================================================== #
# TODO Diffrentiate Yidish & Hebrew


reader = PdfReader('igeret17.pdf')
print(len(reader.pages))
page = reader.pages[15]
text = page.extract_text()
print(text)

import fitz

def scrape(filePath):
    textFonts = ['David-Bold', 'David-Reg']
    titleFonts = ['TimesNewRomanPS-BoldMT']
    results = [] # list of tuples that store the information as (text, font size, font name) 
    pdf = fitz.open(filePath) # filePath is a string that contains the path to the pdf
    for page in pdf:
        dic = page.get_text("dict")
        blocks = dic["blocks"]
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                for span in spans:
                    data = span['spans']
                    for lines in data:
                        # if keyword in lines['text'].lower(): # only store font information of a specific keyword
                        # if lines['font'] not in textFonts:
                        #     results.append((lines['text'][::-1], lines['size'], lines['font']))
                        if lines['font'] in titleFonts and lines['size']>7:
                            results.append((lines['text'][::-1], lines['size'], lines['font']))
                            # lines['text'] -> string, lines['size'] -> font size, lines['font'] -> font name
    pdf.close()
    return results


results= scrape('igeret17.pdf')

# =============================================================================
# for block in list(pdf.pages())[32].get_text("dict")['blocks']:
#     if "lines" in block.keys():
#         print(block['lines'][0]['spans'][0]['text'])
# 
# =============================================================================


# =========================== parshiot ==================================================
# global parshiot; parshiot = {}
#     content = driver.find_element(By.CLASS_NAME, "contentCantill")
#     lines = content.text.splitlines()
#     lines = list(filter(lambda line: line != '', lines))
#     for line in lines:
#         parshiot[len(parshiot.keys())+1] = line
# =========================== parshiot ==================================================


def writeDBtoJson():
    with open("sfarimDict.json", "w") as fp:
        json.dump(sfarim,fp) 


def loadDBfromJson():
    with open('sfarimDict.json') as f:
        data = json.load(f)
    return data
sfarim = loadDBfromJson()



with open(r"C://Users//u294902//Documents//Python Scripts//MainTxt.txt", "w") as f:
    f.write(txt)

elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
#C:\Users\u294902\Documents\Python Scripts