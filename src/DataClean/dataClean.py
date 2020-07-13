import pandas as pd
import numpy as np
import re
import jieba

def split_money(x):
    try:
        if x[-3] == '万':
            sal = [float(i)*10000 for i in re.findall("[0-9]+\.?[0-9]*",x)]
        elif x[-3] == '千':
            sal = [float(i)*1000 for i in re.findall("[0-9]+\.?[0-9]*",x)]
        if x[-1] == '年':
            sal = [i/12 for i in sal]
        return sal
    except Exception as a:
        print(a)
        return x

#工作地处理
def split_location(x):
    if "-" in x:
        loc=x.split('-')[0]
    else:
        loc=x
    return loc

def clean_people(x):
    if x=="50-150人":
        return "50-150"
    elif x=="150-500人":
        return "150-500"
    elif x=="少于50人":
        return "少于50"
    elif x=="1000-5000人":
        return "1000-5000"
    elif x=="500-1000人":
        return "500-1000"
    elif x=="10000人以上":
        return "大于10000"
    elif x=="5000-10000人":
        return "5000-10000"
    else:
        return np.nan

def dataClean(filename):
    df = pd.read_csv(r"../DataGet/"+filename+".csv")
    # print(df.describe(include=['O']))
    # 删除重复值
    employ = df.drop_duplicates(inplace=False)
    # print(df.shape)
    # print(employ.shape)
    # 缺失值处理
    # print(employ.isnull().sum())
    employ.education.fillna('不限学历', inplace=True)
    employ.work_experience.fillna('不做要求', inplace=True)
    # 公司地址，不需要且缺失比较多，直接删除
    employ.drop(['address'], axis=1, inplace=True)
    # 薪水清洗
    # print(employ['wages'].str[-1].value_counts())
    # print('*'*30)
    # print(employ['wages'].str[-3].value_counts())
    # 没有薪资的招聘信息没有意义，删除
    employ.dropna(how='any', subset=['wages', 'company_size', 'company_type'], inplace=True)
    # print(employ.isnull().sum())
    # print(employ.shape)
    index_time = employ['wages'].str[-1].isin(['年', '月'])
    index_money = employ['wages'].str[-3].isin(['万', '千'])
    employ = employ[index_time & index_money]
    salary = employ['wages'].apply(split_money)
    # salary.to_csv('salary.csv',encoding="utf_8_sig")
    employ['salay_min'] = salary.str[0].astype('int')
    employ['salay_max'] = salary.str[1].astype('int')
    employ['salay_mean'] = employ[['salay_min', 'salay_max']].mean(axis=1).astype('int')
    employ['city'] = employ['place'].apply(split_location)
    #公司人员重构
    employ['company_size']=employ['company_size'].apply(clean_people)
    # 岗位描述关键字筛选
    with open('stop_word.txt', 'r', encoding='UTF-8') as f:
        stopword = f.read()

    stopword = stopword.split()
    stopword = stopword + ["任职", "职位", " ","职责", "负责"]
    employ["point_information"] = employ["point_information"].str[2:-2].apply(lambda x: x.lower()).apply(
        lambda x: "".join(x)) \
        .apply(jieba.lcut).apply(lambda x: [i for i in x if i not in stopword])
    employ.loc[employ["point_information"].apply(lambda x: len(x) < 6), "point_information"] = np.nan

    df_job = employ[
        ['position', 'company', 'company_type', 'company_size', 'city', 'salay_min', 'salay_max', 'salay_mean',
         'education', 'work_experience', 'industry', 'point_information']]
    df_job.columns = ['工作', '公司', '公司性质', '公司规模', '城市', '最低薪', '最高薪', '平均薪', '学历', '工作经验', '行业', '职责']
    to_file='cleanData/'+filename+'_clean.csv'
    df_job.to_csv(to_file,encoding="utf_8_sig")

if __name__ == '__main__':
    dataClean("python")

