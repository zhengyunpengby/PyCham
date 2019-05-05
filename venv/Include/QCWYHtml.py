# coding=gbk
import unittest
import sys
from bs4 import BeautifulSoup
from bs4 import element

def praseHTML(content,codeing):
    charset='<meta http-equiv="Content-Type" content="text/html; charset={0}" />'
    charset=charset.format(codeing)
    soup=BeautifulSoup(content,'html.parser')
    contentList=soup.body
    print(len(contentList.contents))
    #print('0:'+str(contentList.contents[0]))
    #print('1:'+str(contentList.contents[1]))
    #print('2:'+str(contentList.contents[2]))
    #print('3:'+str(contentList.contents[3]))
    #print('4:'+str(contentList.contents[4]))
    #print('5:'+str(contentList.contents[5]))
    #print('6:'+str(contentList.contents[6]))
    #print('7:'+str(contentList.contents[7]))
    html='<!DOCTYPE '+str(contentList.contents[2])+'>'+charset+str(contentList.contents[4])
    return html