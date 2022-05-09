import bs4
from bs4 import BeautifulSoup
import sys
import re

soup=BeautifulSoup(sys.stdin,'html.parser')

def is_bu(elem): #is this a bold_underline?
    return len(list(elem.select("u > b")))>0 or len(list(elem.select("b > u")))>0

def is_b(elem): #is this bold?
    return len(list(elem.select("b")))>0

def is_tag(elem):
    return isinstance(elem,bs4.Tag)

for elem in soup.body.children:
    if not is_tag(elem):
        continue
    if is_bu(elem):
        print("DOC",elem)
        continue
    if is_b(elem):
        print("Q",elem)
        continue
    
    
