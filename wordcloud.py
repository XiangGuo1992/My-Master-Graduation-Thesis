# -*- coding:utf-8 -*-
'''
绘制论文词云图
'''
import time
import codecs
import jieba
import jieba.analyse as analyse
from wordcloud import WordCloud
from wordcloud import STOPWORDS, ImageColorGenerator
from scipy.misc import imread
import os
from os import path
import matplotlib.pyplot as plt

#os.chdir('F:\\GuoXiang\\硕士毕业论文\\论文\\wordcloud') 
os.chdir('F:\\GuoXiang\\论文\\祝月艳') 

# 得到所有关键词
def get_all_keywords(file_name):
    word_lists = [] # 关键词列表
    with codecs.open(file_name,'r',encoding='utf-8') as f:
        Lists = f.readlines() # 文本列表
        for List in Lists:
            cut_list = list(jieba.cut(List))
            for word in cut_list:
                word_lists.append(word)
    word_lists_set = set(word_lists) # 去除重复元素
    sort_count = []
    word_lists_set = list(word_lists_set)
    length = len(word_lists_set)
    print ("共有%d个关键词" % length)
    k = 1
    for w in word_lists_set:
        sort_count.append(w+':'+str(word_lists.count(w))+"次\n")
        print ("%d---" % k + w+":"+str(word_lists.count(w))+ "次")
        k += 1
    with codecs.open('count_word.txt','w',encoding='utf-8') as f:
        f.writelines(sort_count)

def get_top_keywords(file_name):
    top_word_lists = [] # 关键词列表
    with codecs.open(file_name,'r',encoding='utf-8') as f:
        texts = f.read() # 读取整个文件作为一个字符串
        Result = analyse.textrank(texts,topK=20,withWeight=True,withFlag=True)
        n = 1
        for result in Result:
            print ("%d:" % n ,)
            for C in result[0]: # result[0] 包含关键词和词性
                print (C,"  ",)
            print ("权重:"+ str(result[1])) # 关键词权重
            n += 1

# 绘制词云
def draw_wordcloud():
   with codecs.open('毕业设计大论文-祝月艳-第五版.txt',encoding='utf-8') as f:
       comment_text = f.read()
   cut_text = " ".join(jieba.cut(comment_text)) # 将jieba分词得到的关键词用空格连接成为字符串
   d = path.dirname(__file__) # 当前文件文件夹所在目录
   color_mask = imread("F:\\GuoXiang\\论文\\祝月艳\\943.jpg") # 读取背景图片
   cloud = WordCloud(font_path=path.join(d,'simsun.ttc'),background_color='white',mask=color_mask,max_words=2000,max_font_size=40)
   word_cloud = cloud.generate(cut_text) # 产生词云
   word_cloud.to_file("paper_cloud.jpg")

   image_colors = ImageColorGenerator(color_mask)
   # 以下代码显示图片
   plt.imshow(cloud)
   plt.axis("off")
    # 绘制词云
   plt.figure()
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
   plt.imshow(cloud.recolor(color_func=image_colors))
   plt.axis("off")
    # 绘制背景图片为颜色的图片
   plt.figure()
   plt.imshow(color_mask, cmap=plt.cm.gray)
   plt.axis("off")
   plt.show()
    # 保存图片
   cloud.to_file("名称.jpg")
   


#file_name='13_ZY1413206_郭翔.txt'
file_name='毕业设计大论文-祝月艳-第五版.txt'
get_top_keywords(file_name)
draw_wordcloud()