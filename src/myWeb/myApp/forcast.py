import itertools
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


def TongJiCity(filename):
    data = pd.read_csv(filename)#读文件
    city = []
    publish_time = []
    for row in data.itertuples():
        if getattr(row, '城市') == '广州':  #########这里需要输入城市名称，已测试北京上海都是可以的
            city.append(getattr(row, 'prop'))
            publish_time.append(getattr(row, '发布时间'))
    time = pd.to_datetime(publish_time)  # date转为日期类型
    data = pd.DataFrame(city, index=time, columns=['value'])
    return data

def TongJiSalary(filename):
    employ = pd.read_csv(filename)  # 读文件
    # 尝试统计每天的薪资
    employ['平均薪'] = employ['平均薪'].astype(float)
    average_salary = employ.groupby('发布时间', as_index=False)['平均薪'].mean()
    time = []
    salary = []
    for row in average_salary.itertuples():
        time.append(getattr(row, '发布时间'))
        salary.append(getattr(row, '平均薪'))
    time = pd.to_datetime(time)  # date转为日期类型
    average_salary = pd.DataFrame(salary, index=time, columns=['value'])
    return average_salary

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






