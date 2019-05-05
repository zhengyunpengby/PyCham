import win32com.client
import os

def change(dir):
    list = os.listdir(dir)
    word = win32com.client.Dispatch('Word.Application')
    for src in list:
        if src.endswith('.html'):
            dist=src.split('.')[0]+'.doc'
            doc = word.Documents.Add(dir+src)
            doc.SaveAs(dir+dist, FileFormat=0)
            doc.Close()
    word.Quit()