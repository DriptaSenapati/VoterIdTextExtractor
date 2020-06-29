# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 19:47:17 2020

@author: Dripta
"""

import pytesseract
from pytesseract import Output
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import os
from datetime import datetime


pytesseract.pytesseract.tesseract_cmd = <tesseract.exe file_location >
TESSDATA_PREFIX = <tessdata_folder_path >


def TextExtractor(img):
    # print(img)
    im = Image.open(img)
    # print(im)
    im.save("front-300.jpg", dpi=(150, 150))
    im = Image.open('front-300.jpg')

    enhancer = ImageEnhance.Contrast(im)
    im_output = enhancer.enhance(factor=2)

    enhancer = ImageEnhance.Brightness(im_output)
    # gives original image
    im_output = enhancer.enhance(factor=1.5)
    im_output.save('britened-image.jpg')

    img = cv2.imread('britened-image.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(gray, kernel, iterations=1)
    img = cv2.erode(gray, kernel, iterations=1)
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
    cv2.imwrite('thres_bright_image.jpg', thresh)
    text = pytesseract.image_to_string(Image.open('thres_bright_image.jpg'))
    results = pytesseract.image_to_data(Image.open(
        'thres_bright_image.jpg'), output_type=Output.DICT)

    return text, results


'''text,result=TextExtractor('test_image.jpg')
text2,result2=TextExtractor('sayan_front.JPEG')
text3,result3=TextExtractor('front_image.jpg')
text4,result2=TextExtractor('test_back_image.jpg')
text5,result3=TextExtractor('sayan_back.JPEG')
text6,result4=TextExtractor('test1.jpg')
text7,result5=TextExtractor('ma_back.jpg')
text8,result6=TextExtractor('test5.jpg')'''


def namesExtractor(result):
    approx_words1 = ['Father', "Father's", "Husband", "Husband's", 'FATHER']
    for approx in approx_words1:
        for i in range(len(result['text'])):
            if approx in result['text'][i]:
                father_line_num = result['line_num'][i]
                father_block_num = result['block_num'][i]
                father_para_num = result['par_num'][i]
    approx_words2 = ["Elector", "Elector's", 'ELECTOR']
    for approx in approx_words2:
        for i in range(len(result['text'])):
            if approx in result['text'][i]:
                elector_line_num = result['line_num'][i]
                elector_block_num = result['block_num'][i]
                elector_para_num = result['par_num'][i]
    extracted = [[], []]
    for j, k in enumerate(result['text']):
        if result['block_num'][j] == father_block_num:
            if result['par_num'][j] == father_para_num:
                if result['line_num'][j] == father_line_num:
                    if int(result['conf'][j]) >= 20:
                        extracted[0].append(k)
            else:
                pass
    for j, k in enumerate(result['text']):
        if result['block_num'][j] == elector_block_num:
            if result['par_num'][j] == elector_para_num:
                if result['line_num'][j] == elector_line_num:
                    if int(result['conf'][j]) >= 20:
                        extracted[1].append(k)
    if len(extracted[1]) == 2:
        elector_block_num += 1
        for j, k in enumerate(result['text']):
            if result['block_num'][j] == elector_block_num:
                if int(result['conf'][j]) >= 20:
                    extracted[1].append(k)

    name_extractor = [" ".join(extracted[0]), " ".join(extracted[1])]
    return name_extractor

# namesExtractor(result6)


def sexExtractor(result):
    flag = 0
    for i in range(len(result['text'])):
        if 'Sex' in result['text'][i]:
            sex_index = i
    for i in range(sex_index, len(result['text']), 1):
        if 'Male' in result['text'][i]:
            gender = 'Gender Male'
            flag = 1
            break
        elif 'M' in result['text'][i]:
            gender = 'Gender Male'
            flag = 1
            break
    if flag == 1:
        return gender
    else:
        return 'Gender Female'


# sexExtractor(result6)

def DOBextractor(result):
    flag = 0
    for i in range(len(result['text'])):
        try:
            date = datetime.strptime(result['text'][i], '%d/%m/%Y')
            flag = 1
            return f'DOB {result["text"][i]}'
        except:
            pass
    if flag != 1:
        return f'DOB None'


def ID(image):
    from PIL import Image, ImageEnhance
    im = Image.open(image)
    enhancer = ImageEnhance.Brightness(im)
    factor = 1.5  # brightens the image
    im_output = enhancer.enhance(factor)
    im_output.save('brightened-front.png')

    '''im3 = Image.open("brightened-front.png")
    enhancer = ImageEnhance.Contrast(im3)
    factor = 1.5 #increase contrast
    im_output = enhancer.enhance(factor)
    im_output.save('more-contrast-image.png')
    
    im2 = Image.open('more-contrast-image.png')
    im2.save("brightened-front-300.jpg",dpi=(75,75))'''

    img = cv2.imread('brightened-front.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
    cv2.imwrite('thres_bright_image_next.jpg', thresh)
    text = pytesseract.image_to_string(r'thres_bright_image_next.jpg')
    words = pytesseract.image_to_data(
        r'thres_bright_image_next.jpg', output_type=Output.DICT)

    '''img = cv2.imread("gray-front.jpg")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_string(img))
    words = pytesseract.image_to_data(r"brightened-front-300.jpg", output_type=Output.DICT)'''
    return words


def ext_ID(image):
    a = ID(image)

    for i in range(len(a['text'])):
        if len(a['text'][i]) == 10:
            if a['conf'][i] > 20:
                numckeck = any(char.isdigit() for char in a['text'][i])
                if (a['text'][i] != 'COMMISSION'):
                    if('/' in a['text'][i]) == False:
                        if(numckeck == True):
                            return 'ID-'+a['text'][i]

# ext_ID('test5.jpg')


# words,text=ID('back_image.jpg')


def addresExtractor(result):
    address = []
    flag = 0
    for i in range(len(result['text'])):
        if 'Address' in result['text'][i]:
            if result['block_num'][i+2] != result['block_num'][i]:
                add_block_num = result['block_num'][i]+1
            elif result['block_num'][i+2] == result['block_num'][i]:
                add_block_num = result['block_num'][i]
    for i in range(add_block_num, add_block_num+2, 1):
        for p, q in enumerate(result['text']):
            if result['block_num'][p] == i:
                if 'Date' not in q:
                    if int(result['conf'][p]) > 50:
                        address.append(q)
                else:
                    flag = 1
                    break
        if flag == 1:
            break
    return " ".join(address)
