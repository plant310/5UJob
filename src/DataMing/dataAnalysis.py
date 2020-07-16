import traceback
import pandas as pd
import numpy as np
import pymysql
import re
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import itertools
import statsmodels.api as sm
import pymysql
from sqlalchemy import create_engine

def salary_outlier(job_salary):
    # 判断异常值：过箱线图法（分位差法）
    # x_bar = job_salary['平均薪'].mean()
    # x_std = job_salary['平均薪'].std()
    # Q1 = job_salary['平均薪'].quantile(q=0.25)
    # Q3 = job_salary['平均薪'].quantile(q=0.75)
    # IQR = Q3 - Q1  # 分位差
    # print(any(job_salary['平均薪'] > Q3+1.5*IQR))
    # print(any(job_salary['平均薪'] > Q1-1.5*IQR))
    # plt.boxplot(job_salary['salary_new'])
    # plt.show()
    # 异常值处理:盖帽法
    P95 = job_salary['平均薪'].quantile(q=0.95)
    P5 = job_salary['平均薪'].quantile(q=0.05)
    job_salary['salary_new'] = job_salary['平均薪']
    job_salary.loc[job_salary['平均薪'] > P95, 'salary_new'] = P95
    job_salary.loc[job_salary['平均薪'] < P5, 'salary_new'] = P5
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
    try:
        sql = "DELETE FROM company_type WHERE profession_id = 1"
        cursor.execute(sql)
        sql = "insert into company_type (profession_id,company_type,number) values(%s,%s, %s)"
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
    try:
        sql = "DELETE FROM company_size WHERE profession_id = 1"
        cursor.execute(sql)
        sql = "insert into company_size (profession_id,company_size,company_number) values(%s,%s, %s)"
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
    try:
        sql = "DELETE FROM education WHERE profession_id = 1"
        cursor.execute(sql)
        sql = "insert into education(profession_id,education,number,avg_salary,lowest_salary,highest_salary) values(%s,%s,%s, %s,%s,%s)"
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
    try:
        sql = "DELETE FROM experience WHERE profession_id = 1"
        cursor.execute(sql)
        sql = "insert into experience(profession_id,experiene,avg_salary,lowest_salary,highest_salary,number) values(%s,%s,%s, %s,%s,%s)"
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
    try:
        sql = "DELETE FROM region WHERE profession_id = 1"
        cursor.execute(sql)
        sql = "insert into region (profession_id,region,number,lowest_salary,highest_salary) values(%s,%s, %s,%s,%s)"
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
    try:
        sql = "DELETE FROM experience_salary WHERE profession_id = 1"
        cursor.execute(sql)
        sql = "insert into experience_salary (profession_id,experiene,avg_salary,lowest_salary,highest_salary) values(%s,%s, %s,%s,%s)"
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
    myword.to_file('../myWeb/static/images/cloudwords/'+filename+'.png')
    # plt.imshow(myword)
    # plt.axis("off")
    # plt.show()
def predict_req(job):
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8')
    cursor = db.cursor()
    #城市需求预测
    job_req = job.groupby(by=['发布时间', '城市'], as_index=False)['工作'].count()
    date_group = job.groupby(by=['发布时间'])['工作'].count()
    job_req.reset_index(inplace=True)
    # print(job_req[job_req['发布时间']=='2020-05-04'])
    # req=job_req['发布时间']
    # job_req.insert(4,'prop',0.0)
    prop = []
    for i in range(job_req.shape[0]):
        prop.append(job_req.loc[i]['工作'] / date_group[job_req.loc[i]['发布时间']])
    job_req.insert(4, 'prop', prop)
    # print(job_req)
    # job_req.to_csv('job_req.csv', encoding="utf_8_sig")
    v1 = job_req['城市'].tolist()
    v2 = job_req['发布时间'].tolist()
    v3 = job_req['prop'].tolist()
    values = []
    for i in range(0, len(v1)):
        values.append((1, v1[i], v2[i], v3[i]))
    sql = "insert into region_prediction (profession_id,region,date,number) values(%s,%s,%s,%s)"
    try:
        cursor.executemany(sql, values)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()
def predict_salary(job):
    db = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
        charset='utf8')
    cursor = db.cursor()
    #薪资变化预测
    job_salary = job.groupby(by=['发布时间'], as_index=False)['平均薪'].mean()
    # job_salary_group = job_salary.groupby(by=['发布时间'], as_index=False).agg(lambda x: x.value_counts().index[0]).reset_index()
    salary_outlier(job_salary)
    # print(job_salary['salary_new'])
    # plt.plot(job_salary['发布时间'], job_salary['salary_new'])
    # plt.show()
    v1 = job_salary['发布时间'].tolist()
    v2 = job_salary['salary_new'].tolist()
    values = []
    for i in range(0, len(v1)):
        values.append((1, v1[i], v2[i]))
    sql = "insert into salary_prediction (profession_id,date,avg_salary) values(%s,%s,%s)"
    try:
        cursor.executemany(sql, values)
        db.commit()
    except Exception:
        print("录入异常！")
        traceback.print_exc()
    finally:
        db.close()
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print("录入异常！" )
        traceback.print_exc()
    finally:
        db.close()
#职业分析数据存入数据库
def to_db(filename):
    job=pd.read_csv("../DataClean/cleanData/"+filename+".csv")
    #print(companyType_count.index.tolist(),companyType_count.tolist())
    # description(job['职责'].tolist())
    companyType_statistic(job)
    companySize_statistic(job)
    workyear_statistic(job)
    salary_req_statistic(job)
    education_statistic(job)

#不断迭代，找到优化感兴趣度量的ARIMA(p,d,q)的值
def bestParameter(data):
    # 找合适的p d q
    p = d = q = range(0, 2) #初始化 p d q
    pdq = list(itertools.product(p, d, q))# 产生不同的pdq元组,得到 p d q全排列
    seasonal_pdq = [(x[0], x[1], x[2], 7) for x in pdq] #季节性参数，7代表一个星期的长度
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                #使用statsmodels模块的SARIMAX()函数拟合一个新的季节性ARIMA模型，并评估其整体质量
                mod = sm.tsa.statespace.SARIMAX(data['value'],
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
                results = mod.fit()
            except:
                continue
    return results

def forcast (results):
    #根据训练好的拟合模型result，向后预测
    pred_uc = results.get_forecast(steps=30)  # 设定预测的时长30天
    pred_uc = pred_uc.predicted_mean
    value = pred_uc.reset_index().values
    return value

def plotPicture(data,predict_value):
    plt.title("Predict", fontsize=15, color="red")  # 图像标题
    ax = data['value'].plot(label='observed', figsize=(7, 4))  # 根据原数据绘图
    predict_value.plot(ax=ax, label='Forecast')  # 对预测值绘图
    '''ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)'''  # 绘制预测数据的上下浮动范围
    # 横纵坐标
    ax.set_xlabel('Date', fontsize=15)
    ax.set_ylabel('Predict', fontsize=15)
    plt.legend()
    plt.show()



if __name__ == '__main__':
     # to_db('python_clean')
     job = pd.read_csv("../DataClean/cleanData/python_clean.csv")
     #conn = create_engine('mysql+pymysql://root:root@localhost:3306/test')  # 连接数据库
     #sql = 'select * from salary_prediction'
     #job_salary = pd.read_sql(sql, conn)
     #predict_salary(job)
     #薪资变化预测
     job_salary = job.groupby(by=['发布时间'], as_index=False)['平均薪'].mean()
     job_salary_group = job_salary.groupby(by=['发布时间'], as_index=False).agg(lambda x: x.value_counts().index[0]).reset_index()
     salary_outlier(job_salary)

     time = []
     salary = []
     for row in job_salary.itertuples():
         time.append(getattr(row, '发布时间'))
         salary.append(getattr(row, 'salary_new'))
     time = pd.to_datetime(time)  # date转为日期类型
     job_salary = pd.DataFrame(salary, index=time, columns=['value'])
     # job_salary.rename(columns={'salary_new':'value'}, inplace = True)#送入公共预测函数前，统一列名
     # 调用第二个函数，遍历的方式寻找最优参数.返回训练好的拟合模型
     results = bestParameter(job_salary)
     # 预测一下
     predict_value = forcast(results)
     print(predict_value.index)
     # 画个图看一下
     plotPicture(job_salary, predict_value)
     db = pymysql.Connect(
         host='localhost',
         port=3306,
         user='root',
         passwd='root',
         db='test',
         charset='utf8')
     cursor = db.cursor()
     v1 = job_salary['发布时间'].tolist()
     v2 = job_salary['salary_new'].tolist()
     values = []
     for i in range(0, len(v1)):
         values.append((1, v1[i], v2[i]))
     sql = "insert into salary_prediction (profession_id,date,avg_salary) values(%s,%s,%s)"
     try:
         cursor.executemany(sql, values)
         db.commit()
     except Exception:
         print("录入异常！")
         traceback.print_exc()
     finally:
         db.close()
     try:
         cursor.execute(sql)
         db.commit()
     except Exception:
         print("录入异常！")
         traceback.print_exc()
     finally:
         db.close()

