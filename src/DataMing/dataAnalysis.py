import traceback
import pandas as pd
import numpy as np
import pymysql
import re
import jieba.analyse
from wordcloud import WordCloud

#企业性质
def companyType_statistic(job):
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8')
    cursor = db.cursor()
    companyType_count = job['公司性质'].value_counts()
    v1 = companyType_count.index.tolist()
    v2 = companyType_count.tolist()
    values = []
    for i in range(0, len(v1)):
        values.append((1, v1[i], v2[i]))
    sql = "insert into company_type (profession_id,company_type,number) values(%s,%s, %s)"
    try:
        cursor.executemany(sql, values)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()

#企业规模
def companySize_statistic(job):
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8')
    cursor = db.cursor()
    companySize_count = job['公司规模'].value_counts()
    v1 = companySize_count.index.tolist()
    v2 = companySize_count.tolist()
    values = []
    for i in range(0, len(v1)):
        values.append((1, v1[i], v2[i]))
    sql = "insert into company_size (profession_id,company_size,company_number) values(%s,%s, %s)"
    try:
        cursor.executemany(sql, values)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()

#学历要求以及salary
def education_statistic(job):
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8')
    cursor = db.cursor()
    education_count = job.groupby('学历', as_index=False)['工作'].count().sort_values('工作', ascending=False)
    # 求出各工作经验对应的平均最高与最低薪资
    salary_education = job.groupby('学历', as_index=False)['最低薪', '最高薪'].mean()
    # 求平均薪资
    salary_education['salary'] = (salary_education['最低薪'].add(salary_education['最高薪'])).div(2)
    salary_education = pd.merge(education_count, salary_education, how='left', on='学历')
    v1 = salary_education['学历'].values.tolist()
    v2 = salary_education['工作'].values.tolist()
    v3 = salary_education['salary'].values.tolist()
    v4 = salary_education['最低薪'].values.tolist()
    v5 = salary_education['最高薪'].values.tolist()
    values = []
    for i in range(0, len(v1)):
        values.append((1, v1[i], v2[i], v3[i], v4[i], v5[i]))
    sql = "insert into education(profession_id,education,number,avg_salary,lowest_salary,highest_salary) values(%s,%s,%s, %s,%s,%s)"
    try:
        # print(salary_education)
        cursor.executemany(sql, values)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()


#工作经验要求以及salary
def workyear_statistic(job):
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8')
    cursor = db.cursor()
    experience_count = job.groupby('工作经验', as_index=False)['工作'].count().sort_values('工作', ascending=False)  # 合并数据表

    salary_year = job.groupby('工作经验', as_index=False)['最低薪', '最高薪'].mean()
    # 求平均薪资
    salary_year['salary'] = (salary_year['最低薪'].add(salary_year['最高薪'])).div(2)
    salary_year = pd.merge(experience_count, salary_year, how='left', on='工作经验')

    v1 = salary_year['工作经验'].values.tolist()
    v2 = salary_year['salary'].values.tolist()
    v3 = salary_year['最低薪'].values.tolist()
    v4 = salary_year['最高薪'].values.tolist()
    v5 = salary_year['工作'].values.tolist()
    values = []
    for i in range(0, len(v1)):
        values.append((1, v1[i], v2[i], v3[i], v4[i], v5[i]))
    sql = "insert into experience(profession_id,experiene,avg_salary,lowest_salary,highest_salary,number) values(%s,%s,%s, %s,%s,%s)"
    try:
        # print(values)
        cursor.executemany(sql, values)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()


#薪资水平
#薪资与岗位需求关系
def salary_req_statistic(job):
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8')
    cursor = db.cursor()
    job['最低薪'], job['最高薪'] = job['最低薪'].astype(float), job['最高薪'].astype(float)
    # 分别求各地区平均最高薪资，平均最低薪资
    salary = job.groupby('城市', as_index=False)['最高薪', '最低薪'].mean()
    Workplace = job.groupby('城市', as_index=False)['工作'].count().sort_values('工作', ascending=False)  # 合并数据表
    Workplace = pd.merge(Workplace, salary, how='left', on='城市')  # 用前20名进行绘图
    Workplace = Workplace.head(20)
    v1 = Workplace['城市'].values.tolist()
    v2 = Workplace['工作'].values.tolist()
    v3 = Workplace['最高薪'].values.tolist()
    v4 = Workplace['最低薪'].values.tolist()
    values = []
    for i in range(0, len(v1)):
        values.append((1, v1[i], v2[i], v4[i], v3[i]))
    sql = "insert into region (profession_id,region,number,lowest_salary,highest_salary) values(%s,%s, %s,%s,%s)"
    try:
        cursor.executemany(sql, values)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()

#薪资与经验关系
def salary_exp_statistic(job):
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8')
    cursor = db.cursor()
    # 求出各工作经验对应的平均最高与最低薪资
    salary_year = job.groupby('工作经验', as_index=False)['最低薪', '最高薪'].mean()
    # 求平均薪资
    salary_year['salary'] = (salary_year['最低薪'].add(salary_year['最高薪'])).div(2)

    v1 = salary_year['工作经验'].values.tolist()
    v2 = salary_year['salary'].values.tolist()
    v3 = salary_year['最低薪'].values.tolist()
    v4 = salary_year['最高薪'].values.tolist()
    values = []
    for i in range(0, len(v1)):
        values.append((1, v1[i], v2[i], v3[i], v4[i]))
    sql = "insert into experience_salary (profession_id,experiene,avg_salary,lowest_salary,highest_salary) values(%s,%s, %s,%s,%s)"
    try:
        cursor.executemany(sql, values)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()


#薪资与学历关系
# def salary_edu_statistic(job):
#     db = pymysql.Connect(
#         host='47.100.11.75',
#         port=3306,
#         user='root',
#         passwd='5880940',
#         db='analysisResults',
#         charset='utf8')
#     cursor = db.cursor()
#     #求出各工作经验对应的平均最高与最低薪资
#     salary_education=job.groupby('学历',as_index=False)['最低薪','最高薪'].mean()
#     #求平均薪资
#     salary_education['salary']=(salary_education['最低薪'].add(salary_education['最高薪'])).div(2)
#
#     sql = ""
#     try:
#         cursor.execute(sql)
#         db.commit()
#     except Exception:
#         print("录入异常！" )
#         traceback.print_exc()
#     finally:
#         db.close()

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

def to_db(filename):
    job=pd.read_csv("../DataClean/cleanData/"+filename+".csv")
    #print(companyType_count.index.tolist(),companyType_count.tolist())
    # description(job['职责'].tolist())

    companyType_statistic(job)
    companySize_statistic(job)
    workyear_statistic(job)
    salary_req_statistic(job)
    education_statistic(job)

if __name__ == '__main__':
    to_db('python_clean')