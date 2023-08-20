# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 11:33:37 2023

@author: U301901


1.	CID – מספר סידורי 
2.	CONTRADICTION_QUESTION – במסמך מופיע כהמחלוקת
3.	CONTRADICTION_SOURCE – המקור בגמרא
4.	CONCLUSION_DETAILS – במסמך מופיע כתוכן עניינים	
5.	OP1_DETAILS – פרטיי המחלוקת לדעה הראשונה (ללא שם בעל הדעה) 
6.	OP2_DETAILS –  פרטיי המחלוקת לדעה השנייה (ללא שם בעל הדעה) 
7.	OP1_NAME – בעל הדעה הראשונה
8.	OP2_NAME – בעל הדעה השנייה
9.	OP1_CONCLUSION – חפצא או גברא
10.	OP2_CONCLUSION – חפצא או גברא

"""
pins = ['CONTRADICTION_SOURCE', 'CONTRADICTION_QUESTION', 'OP1_DETAILS', 'OP2_DETAILS']
tractateNames=['מסכת ברכות','מסכת שבת','מסכת עירובין','מסכת פסחים','מסכת יומא','מסכת ר"ה','מסכת סוכה','מסכת ביצה','מסכת מועד קטן','מסכת יבמות','מסכת כתובות','מסכת נדרים','מסכת נזיר','מסכת סוטה','מסכת גיטין','מסכת קידושין','מסכת בבא קמא','מסכת בבא מציעא','מסכת בבא בתרא','מסכת סנהדרין','מסכת מכות','מסכת שבועות','מסכת שבועות','מסכת עבודה זרה','מסכת זבחים','מסכת מנחות','מסכת חולין','מסכת בכורות','מסכת ערכין','מסכת תמורה','מסכת כריתות','מסכת מעילה','מסכת נדה']
import pandas as pd
import PyPDF2

file_path = "C:/Users/u301901/Desktop/achdut/Achdut BaTorah - 3 - Sofi.pDF"
pagesDict = {}
DF = {}
txtLst = []
CID = 1
pin = pins[0]
tractateIndex = 0
with open(file_path, mode="rb") as file:
    reader = PyPDF2.PdfReader(file)   
    num_pages = len(reader.pages)
    currTractate = tractateNames[tractateIndex]
    for page_number in range(num_pages):
        page = reader.pages[page_number]
        txt = page.extract_text()
        pagesDict[page_number+1] = txt # writing saving to Pages - Dict
        txtLst.extend(txt.split('\n'))
txtLst = txtLst[113:] #starting from the relevant rows
#txtLst = txtLst[113:] #starting from the undivided pages


file_path = "C:/Users/u301901/Desktop/achdut/prefixes.xlsx"
prefixes = pd.read_excel(file_path, header=0).values.tolist()
prefixes = [item for sublist in prefixes for item in sublist]

i=0
for row in txtLst:
    #row indetification:
    if row.strip() == '' :
        continue
    elif 'תוות' in row:  #שורת תחילת עמוד 
        print('Page : '+row.replace('תוות',''))
    elif row.strip() == tractateNames[tractateIndex+1]: #שורת שם מסכת
        print("This Tractrate is :" + row.strip())
        tractateIndex += 1
        currTractate = tractateNames[tractateIndex]
    else:
        if pin == 'CONTRADICTION_SOURCE':
            DF[CID] = {}
            DF[CID]['CONTRADICTION_TRACTATE'] = currTractate
            DF[CID]['CONTRADICTION_SOURCE'] = row  #TODO: handle המשך
            DF[CID]['OP1_DETAILS'] = ''
            DF[CID]['OP2_DETAILS'] = ''
            DF[CID]['OP3_DETAILS'] = ''
            DF[CID]['OP4_DETAILS'] = ''
            DF[CID]['OP5_DETAILS'] = ''
            pin = 'CONTRADICTION_QUESTION'
        
        elif pin == 'CONTRADICTION_QUESTION':
            DF[CID]['CONTRADICTION_QUESTION'] = row
            pin = 'OP1_DETAILS'
        
        elif pin == 'OP1_DETAILS':
            DF[CID]['OP1_DETAILS'] += row
            #if (len(row) < 70) & (row[-1] == '.'):
            if txtLst[i+1].split(' ')[0] in prefixes:
                pin = 'OP2_DETAILS'
                
        elif pin == 'OP2_DETAILS':
            DF[CID]['OP2_DETAILS'] += row
            if txtLst[i+1].split(' ')[0] in prefixes:
                pin = 'OP3_DETAILS'
            else:
                CID += 1
                pin = 'CONTRADICTION_SOURCE'
                
        elif pin == 'OP3_DETAILS':
            DF[CID]['OP3_DETAILS'] += row
            if txtLst[i+1].split(' ')[0] in prefixes:
                pin = 'OP4_DETAILS'
            else:
                CID += 1
                pin = 'CONTRADICTION_SOURCE'
        
        elif pin == 'OP4_DETAILS':
            DF[CID]['OP4_DETAILS'] += row
            if txtLst[i+1].split(' ')[0] in prefixes:
                pin = 'OP5_DETAILS'
            else:
                CID += 1
                pin = 'CONTRADICTION_SOURCE'
                
        elif pin == 'OP5_DETAILS':
            DF[CID]['OP5_DETAILS'] += row
            CID += 1
            pin = 'CONTRADICTION_SOURCE'
        
    i+=1
    
        

df = pd.DataFrame(DF).T
df.to_excel('C:/Users/u301901/Desktop/achdut/DF.xlsx', index=True)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        rowNum=0
        while rowNum < len(txtLst):
            # Check for tractate shift:
            #print(txtLst[rowNum].strip())
            if txtLst[rowNum].strip() == '' or 'תוות' in txtLst[rowNum]:  #שורת תחילת עמוד 
                print(txtLst[rowNum])
            elif txtLst[rowNum].strip() == tractateNames[tractateIndex+1]: #שורת שם מסכת
                print("This Tractrate is :" + txtLst[rowNum].strip())
                tractateIndex += 1
                currTractate = tractateNames[tractateIndex]
                rowNum +=1
            else:
                DF[CID] = {}
                DF[CID]['CONTRADICTION_Tractate'] = currTractate
                DF[CID]['CONTRADICTION_SOURCE'] = txtLst[rowNum]  #TODO: handle המשך
                rowNum += 1
                DF[CID]['CONTRADICTION_QUESTION'] = txtLst[rowNum]
                #DF[CID]['CONCLUSION_DETAILS'] = '' #???
                rowNum += 1
                if rowNum < len(txtLst):
                    
                    DF[CID]['OP1_DETAILS'] = ''
                    while (len(txtLst[rowNum]) > 70) & (txtLst[rowNum][-1] != '.'):
                        DF[CID]['OP1_DETAILS'] += txtLst[rowNum]
                        rowNum += 1
                    DF[CID]['OP1_DETAILS'] += txtLst[rowNum]
                    rowNum += 1
                    
                    DF[CID]['OP2_DETAILS'] = ''
                    while (len(txtLst[rowNum]) > 70) & (txtLst[rowNum][-1] != '.'):
                        DF[CID]['OP2_DETAILS'] += txtLst[rowNum]
                        rowNum += 1
                    DF[CID]['OP2_DETAILS'] += txtLst[rowNum]
                    
                    
                CID += 1
            rowNum += 1
                

        
                
        
        #.replace('\ufeff', '')

        
        
import re
def fixNumberizedRow(row):
    if len(re.sub("[^0-9]", "", k)) == 0:
        return row
    else:
        re.search(r"\d", row)
        
        
page_number = 16
with open(file_path, mode="rb") as file:
    reader = PyPDF2.PdfReader(file)   
    num_pages = len(reader.pages)
    tractateIndex = 0
    currTractate = tractateNames[tractateIndex]
    page = reader.pages[page_number]
    txt = page.extract_text()
    pagesDict[page_number+1] = txt # writing saving to Pages - Dict
    txtLst = txt.split('\n')
    rowNum=0
    
    
    
    
    
    

prefix = {}
for row in txtLst:
    if 'תוות' not in row.split(' ')[0]:
        if row.split(' ')[0] in prefix.keys():
            prefix[row.split(' ')[0]] +=1
        else:
            prefix[row.split(' ')[0]] = 1
            
import pandas as pd
df = pd.DataFrame(data=prefix, index=['histogram'])
df.T.to_excel("prefixes.xlsx", index=True)

