# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 13:42:30 2020

@author: Dripta
"""

import argparse
from extractor import *
import io
import re
import pprint


def main():
    parser = argparse.ArgumentParser(description='Process some output of text from voter id')
    parser.add_argument('--img', type=str,nargs='+',required=True,help='Take two images from user')
    
    
    
    args = parser.parse_args()
    
    print('Detecting Texts.....')
    _,results_front=TextExtractor(args.img[0])
    _,results_back=TextExtractor(args.img[1])
    print('......Detection Done.....')
    print('Analysing texts processing outputs...')
    name_0,name_1=namesExtractor(results_front)
    name_0=re.sub(" : "," ",name_0)
    name_1=re.sub(" : "," ",name_1)
    name_0=re.sub(": ","",name_0)
    name_1=re.sub(": ","",name_1)
    name_0=re.sub(":+/-","",name_0)
    name_1=re.sub(":+/-","",name_1)
    name_0= name_0.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}).strip()
    name_1= name_1.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}).strip()
    name_0_list=name_0.split()
    name_1_list=name_1.split()
    if 'Name' not in name_0_list: 
        name_0_list.insert(1,'Name')
        name_0=" ".join(name_0_list)
        print(name_0)
    if 'Name' not in name_1.split():
        name_1_list.insert(1,'Name')
        name_1=" ".join(name_1_list)
        print(name_1)
    sex=sexExtractor(results_front)
    DOB=DOBextractor(results_front)
    Id=ext_ID(args.img[0])
    address=addresExtractor(results_back)
    response={f'{" ".join(name_1.split(" ")[:2])}':f'{" ".join(name_1.split(" ")[2:])}',
              f'{" ".join(name_0.split(" ")[:2])}':f'{" ".join(name_0.split(" ")[2:])}',
              f'{sex.split()[0]}':f'{sex.split()[1]}',
              f'{DOB.split()[0]}':f'{DOB.split()[1]}',
              f'{Id.split("-")[0]}':f'{Id.split("-")[1]}',
              'Address':f'{address}'}
    pprint.pprint(response, width=1)
    print('....All Done....')
    
if __name__ == '__main__':
    main()
