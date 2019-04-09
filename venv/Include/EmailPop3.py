# coding=gbk
import unittest
import poplib
import sys
from importlib import reload
from email.parser import Parser
from email.parser import BytesParser
from email.header import decode_header
from email.utils import parseaddr
import email.iterators
import datetime
import time

mypath = 'E://email/'


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)
        email = 'resume@rainier.cn '
        password = 'Rainier112345'
        pop3_server = 'pop3.rainier.cn'

        server = poplib.POP3(pop3_server)
        #server.set_debuglevel(1)
        server.user(email)
        server.pass_(password)
        print('Message: %s. Size: %s' % server.stat())

        resp, mails, objects = server.list()
        for index in [20000-10]: #reversed(range(len(mails))):
            # ȡ��ĳһ���ʼ���ȫ����Ϣ
            resp, lines, octets = server.retr(index)
            # �ʼ�ȡ������Ϣ��bytes��ת����Parser֧�ֵ�str
            lists = []
            for e in lines:
                lists.append(e.decode())
            msg_content = '\r\n'.join(lists)
            msg = Parser().parsestr(msg_content)
            #print(msg)
            headerMap=self.print_header(msg)
            print(headerMap['From'])
            contentMap=self.print_info(msg)
            print(contentMap)
            print(index)
        # �ύ������Ϣ���˳�
        server.quit()

    # ������Ϣͷ�е��ַ���
    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            if ('gb2312' in charset):
                charset = 'gb18030'
            value = value.decode(charset)
        return value

    # ���ʼ����������ݱ������ļ�
    # ���ʼ��еĸ�������д�븽���ļ�
    def savefile(self, filename, data, path):
        try:
            filepath = path + filename
            print('Save as: ' + filepath)
            f = open(filepath, 'wb')
        except:
            print(filepath + ' open failed')
            # f.close()
        else:
            f.write(data)
            f.close()

    # ��ȡ�ʼ����ַ����룬������message��Ѱ�ұ��룬���û�У�����header��Content-Type��Ѱ��
    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    # �����ʼ��ĺ��������ȴ�ӡ�ռ��ˡ������ˡ�����
    def print_header(self,msg):
        headerMap={}
        for header in ['From', 'To', 'Subject', 'Date']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = self.decode_str(value)
                elif header in ['From', 'To']:
                    hdr, addr = parseaddr(value)
                    name = self.decode_str(addr)
                    value = name + ' < ' + addr + ' > '
                elif header == 'Date':
                    if(len(value)==25):
                        utcdatetime  = datetime.datetime.strptime(value, '%d %b %Y %H:%M:%S +0800')
                        value=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(utcdatetime.timestamp()))
                    elif (len(value)==36):
                        utcdatetime = datetime.datetime.strptime(value, '%a, %d %b %Y %H:%M:%S +0800 (CST)')
                        value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(utcdatetime.timestamp()))
                    elif (len(value)== 31):
                        utcdatetime = datetime.datetime.strptime(value, '%a, %d %b %Y %H:%M:%S +0800')
                        value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(utcdatetime.timestamp()))
            headerMap[header]=value
        return headerMap

    # Ȼ�����message��walkѭ�������ʼ��е�ÿһ���Ӷ��󣨰����ı���html������һ�λ��Σ�
    # �ʼ�ͷ�����е�filename��������Ӷ����Ǹ������Ը������ƽ��б��벢���������ص�ָ��Ŀ¼
    # ���������ϴ�����ʼ����Ǳ����Ժ�ĸ�ʽ����Ҫ��get_payload��ʱ��ָ��decode=True��ת���ɿ�����ı���
    # ����ʼ���text����html��ʽ����ӡ��ʽ�����ת���Ժ���Ӷ�������
    def print_info(self, msg):
        contentMap={}
        for part in msg.walk():
            filename = part.get_filename()
            content_type = part.get_content_type()
            charset = self.guess_charset(part)
            if filename:
                filename = self.decode_str(filename)
                data = part.get_payload(decode=True)
                if filename != None or filename != '':
                    print('Accessory: ' + filename)
                    self.savefile(filename, data, mypath)
            else:
                email_content_type = ''
                content = ''
                if content_type == 'text/plain':
                    email_content_type = 'text'
                elif content_type == 'text/html':
                    email_content_type = 'html'
                if charset:
                    if ('gb2312' in charset):
                        charset = 'gb18030'
                    content = part.get_payload(decode=True).decode(charset)
                contentMap[content_type]=content
        return contentMap


if __name__ == '__main__':
    unittest.main()
