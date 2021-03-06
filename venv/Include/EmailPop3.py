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
import QCWYHtml
import HtmlToWord

mypath = 'E://email//'


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
        for index in reversed(range(len(mails))): #reversed(range(len(mails))):
            # 取出某一个邮件的全部信息
            resp, lines, octets = server.retr(index)
            filename=str(len(mails)-index)
            # 邮件取出的信息是bytes，转换成Parser支持的str
            lists = []
            for e in lines:
                lists.append(e.decode())
            msg_content = '\r\n'.join(lists)
            msg = Parser().parsestr(msg_content)
            #print(msg)
            headerMap=self.print_header(msg)
            #print(headerMap['From'])
            print(self.getWeb(headerMap['From']))
            contentMap=self.print_info(msg)
            htmlFilename=mypath+filename+'.html';
            file = open(htmlFilename,'wb');
            content = contentMap['content']
            content=content.replace(r'http://img01.51jobcdn.com/im/2016/resume/','')
            if '51job'==self.getWeb(headerMap['From']):
                content=QCWYHtml.praseHTML(content,contentMap['charset'])
            content = content.encode(contentMap['charset'])
            print(contentMap['charset'])
            #print(content)
            file.write(content)
            file.close()
            print(index)
        # 提交操作信息并退出
        HtmlToWord.change(mypath)
        server.quit()

    # 解析消息头中的字符串
    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            if ('gb2312' in charset):
                charset = 'gb18030'
            value = value.decode(charset)
        return value

    # 将邮件附件或内容保存至文件
    # 即邮件中的附件数据写入附件文件
    def savefile(self, filename, data, path):
        try:
            filepath = path + filename
            #print('Save as: ' + filepath)
            f = open(filepath, 'wb')
        except:
            #print(filepath + ' open failed')
            # f.close()
            pass
        else:
            f.write(data)
            f.close()

    # 获取邮件的字符编码，首先在message中寻找编码，如果没有，就在header的Content-Type中寻找
    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    # 解析邮件的函数，首先打印收件人、发件人、标题
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

    # 然后调用message的walk循环处理邮件中的每一个子对象（包括文本、html、附件一次或多次）
    # 邮件头属性中的filename存在则该子对象是附件，对附件名称进行编码并将附件下载到指定目录
    # 由于网络上传输的邮件都是编码以后的格式，需要在get_payload的时候指定decode=True来转换成可输出的编码
    # 如果邮件是text或者html格式，打印格式并输出转码以后的子对象内容
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
                    #print('Accessory: ' + filename)
                    #self.savefile(filename, data, mypath)
                    pass
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
                contentMap['content_type']=content_type
                contentMap['content']=content
                contentMap['charset']=charset
        return contentMap
    def getWeb(self,email):
        return email.split('.')[-2]


if __name__ == '__main__':
    unittest.main()
