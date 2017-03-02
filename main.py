# -*- coding: utf-8 -*-

'''
Created on 2016-12-16

@author: Sawatari
'''

import os
from scrapy import cmdline
from Tkinter import *

def startSpider():
    # 获取文本框内容
    keyword = var.get()
    # 关键字保存至临时文件
    temp = open('tempkey.temp', 'w')
    temp.write(keyword.encode(sys.getfilesystemencoding()))
    temp.close()

    # 清空goods.csv
    if os.path.exists('results.csv'):
        csvfile = open('results.csv', 'w')
        csvfile.truncate()

    # 开始爬虫程序
    cmdline.execute("scrapy crawl WeiboCrawler".split())

reload(sys)
sys.setdefaultencoding('utf8')

root = Tk()
root.title("WeiboCrawler")
# 高宽均不可变
root.resizable(width=False, height=False)

Label(root, text='  ').grid(row=0)
# Label
Label(root, text='输入微博搜索关键字：').grid(row=1)
# 关键字输入框
var = StringVar()
e = Entry(root, textvariable=var).grid(row=2)
# 确认按钮
Button(root, text="开始查询", command=startSpider).grid(row=3)

Label(root, text='  ').grid(row=5, column=0)

# 说明
Label(root, text='结果输出表格文件位于项目根目录“results.csv”').grid(row=6)
Label(root, text='© 2017 Ka Tou').grid(row=7)

# 进入消息循环
root.mainloop()