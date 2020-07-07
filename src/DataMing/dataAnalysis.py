import traceback
import pandas as pd
import numpy as np
import pymysql
import re
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import string
import seaborn as sns

#企业性质
def companyType_statistic(name,job):
    db = pymysql.Connect(
        host='47.100.11.75',
        port=3306,
        user='root',
        passwd='5880940',
        db='analysisResults',
        charset='utf8')
    cursor = db.cursor()
    companyType_count = job['公司性质'].value_counts(normalize=True)
    sql=""
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print("录入异常！" )
        traceback.print_exc()
    finally:
        db.close()

#企业规模
def companySize_statistic(name, job):
    db = pymysql.Connect(
        host='47.100.11.75',
        port=3306,
        user='root',
        passwd='5880940',
        db='analysisResults',
        charset='utf8')
    cursor = db.cursor()
    companySize_count = job['公司规模'].value_counts(normalize=True)
    sql = ""
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()

#学历要求
def education_statistic(name,job):
    db = pymysql.Connect(
        host='47.100.11.75',
        port=3306,
        user='root',
        passwd='5880940',
        db='analysisResults',
        charset='utf8')
    cursor = db.cursor()
    education_count = job['学历'].value_counts(normalize=True)
    sql=""
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print("录入异常！" )
        traceback.print_exc()
    finally:
        db.close()
#工作经验要求
def workyear_statistic(name,job):
    db = pymysql.Connect(
        host='47.100.11.75',
        port=3306,
        user='root',
        passwd='5880940',
        db='analysisResults',
        charset='utf8')
    cursor = db.cursor()
    workyear_count = job['工作经验'].value_counts(normalize=True)
    sql=""
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print("录入异常！" )
        traceback.print_exc()
    finally:
        db.close()

#薪资水平
#薪资与岗位需求关系
def salary_req_statistic(name,job):
    db = pymysql.Connect(
        host='47.100.11.75',
        port=3306,
        user='root',
        passwd='5880940',
        db='analysisResults',
        charset='utf8')
    cursor = db.cursor()
    job['最低薪'], job['最高薪'] = job['最低薪'].astype(float), job['最高薪'].astype(float)
    # 分别求各地区平均最高薪资，平均最低薪资
    salary = job.groupby('城市', as_index=False)['最高薪', '最低薪'].mean()
    Workplace = job.groupby('城市', as_index=False)['工作'].count().sort_values('工作', ascending=False)  # 合并数据表
    Workplace = pd.merge(Workplace, salary, how='left', on='城市')  # 用前20名进行绘图
    Workplace = Workplace.head(20)
    sql=""
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print("录入异常！" )
        traceback.print_exc()
    finally:
        db.close()

#薪资与经验关系
def salary_exp_statistic(name,job):
    db = pymysql.Connect(
        host='47.100.11.75',
        port=3306,
        user='root',
        passwd='5880940',
        db='analysisResults',
        charset='utf8')
    cursor = db.cursor()
    #求出各工作经验对应的平均最高与最低薪资
    salary_year=job.groupby('工作经验',as_index=False)['最低薪','最高薪'].mean()
    #求平均薪资
    salary_year['salary']=(salary_year['最低薪'].add(salary_year['最高薪'])).div(2)

    sql=""
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print("录入异常！" )
        traceback.print_exc()
    finally:
        db.close()

#薪资与学历关系
def salary_edu_statistic(name,job):
    db = pymysql.Connect(
        host='47.100.11.75',
        port=3306,
        user='root',
        passwd='5880940',
        db='analysisResults',
        charset='utf8')
    cursor = db.cursor()
    #求出各工作经验对应的平均最高与最低薪资
    salary_education=job.groupby('学历',as_index=False)['最低薪','最高薪'].mean()
    #求平均薪资
    salary_education['salary']=(salary_education['最低薪'].add(salary_education['最高薪'])).div(2)

    sql=""
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print("录入异常！" )
        traceback.print_exc()
    finally:
        db.close()

#职责词云
def description(job_list,filename):
    comments=''
    for k in range(len(job_list)):
        comments = comments + (str(job_list[k])).strip()
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    cleaned_comments = ''.join(filterdata)
    result = jieba.analyse.extract_tags(cleaned_comments, topK=100, withWeight=True)
    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]

    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80)
    word_frequence = keywords
    myword = wordcloud.fit_words(word_frequence)
    myword.to_file('wordCloud/'+filename+'.png')
    # plt.imshow(myword)
    # plt.axis("off")
    # plt.show()

if __name__ == '__main__':
    job=pd.read_csv("../DataClean/python_clean.csv")

    #description(job['职责'].tolist())
