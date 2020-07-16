from django.shortcuts import render

from myApp.forcast import *
from myApp.models import *
from django.core import serializers
#导入HttpResponse 框架
from django.shortcuts import HttpResponse
import json
import itertools
import statsmodels.api as sm
import pandas as pd

# Create your views here.
def index(request):
    return render(request,'index.html')

def analysis(request,pid):
    return render(request,'analysis.html', {"pid": pid})

def login(request):
    return render(request, 'login.html')

def predict(request):
    return render(request, 'predic.html')

def selfcenter(request):
    return render(request, 'selfcenter.html')

def getProId(request):
    job = ''
    if request.method == "POST":
        job=request.POST.get('profession')
        pro=Profession.objects.get(profession_name=job)
        print(pro)
        return HttpResponse(json.dumps({
            "pid":pro.profession_id,
        }))

def getAnalysis(request):
    data_x = []
    data_y = []
    data_z = []
    data_a = []
    item = ''
    pid = 0
    if request.method == "POST":
        item = request.POST.get("type")
        pid = request.POST.get("pid")
        prof=Profession.objects.get(profession_id=pid);
        #查询图1所对应的表，并把图所需要的横坐标纵坐标传给页面
        if((item=="companySize")):
            list = CompanySize.objects.all()
            for row in list:
                #判断对应的职业
                if (row.profession_id==int(pid)):
                    data_x.append(row.company_size)
                    data_y.append(row.company_number)
            #return HttpResponse(data_x+data_y)
            # return render(request, "analysis.html", {"marks": 0, "data_x": data_x, "data_y": data_y})
            return HttpResponse(json.dumps({"marks": 0, "profession":prof.profession_name,"data_x": data_x, "data_y": data_y}))
        #查询图2所对应的表，并把图所需要的公司种类以及百分比传给界面
        elif((item=="companyType")):
            list=CompanyType.objects.all()
            for row in list:
                #判断对应的职业
                if(row.profession_id==int(pid)):
                    data_x.append(row.company_type)
                    data_y.append(row.number)
            #return HttpResponse(data_x+data_y)
            return HttpResponse(json.dumps({"marks": 1, "profession":prof.profession_name,"data_x": data_x, "data_y": data_y}))
        elif((item=="region_number")):
            list = Region.objects.all()
            for row in list:
                if (row.profession_id == int(pid)):
                    data_x.append(row.region)
                    data_y.append(row.number)
            return HttpResponse(json.dumps({"marks": 2, "profession":prof.profession_name,"data_x": data_x, "data_y": data_y}))
        elif ((item=="region_salary")):
            list = Region.objects.all()
            for row in list:
                if (row.profession_id == int(pid)):
                    data_x.append(row.region)
                    data_y.append(row.lowest_salary)
                    data_z.append(row.highest_salary)
            return HttpResponse(json.dumps({"marks": 3, "profession":prof.profession_name,"data_x": data_x, "data_y": data_y,"data_z":data_z}))
        # return render(request,"文件名.html",{"横坐标列表":data_x,"第一纵坐标列表":data_y,""})
        elif ((item == "education_number")):
            list = Education.objects.all()
            for row in list:
                if (row.profession_id == int(pid)):
                    data_x.append(row.education)
                    data_y.append(row.number)
            return HttpResponse(json.dumps({"marks": 4, "profession":prof.profession_name,"data_x": data_x, "data_y": data_y}))

        elif ((item == "experience_number")):
            list = Experience.objects.all()
            for row in list:
                if (row.profession_id == int(pid)):
                    data_x.append(row.experiene)
                    data_y.append(row.number)
            return HttpResponse(json.dumps({"marks": 5, "profession": prof.profession_name, "data_x": data_x, "data_y": data_y}))

        elif ((item == "education_salary")):
            list = Education.objects.all()
            for row in list:
                if (row.profession_id == int(pid)):
                    data_x.append(row.education)
                    data_y.append(row.avg_salary)
                    data_z.append(row.highest_salary)
                    data_a.append((row.lowest_salary))
            return HttpResponse(json.dumps({"marks": 6, "profession":prof.profession_name,"data_x": data_x, "data_y": data_y,"data_z":data_z,"data_a":data_a}))

        elif (item=="experience_salary"):
            list = Experience.objects.all()
            for row in list:
                if (row.profession_id == int(pid)):
                    data_x.append(row.experiene)
                    data_y.append(row.avg_salary)
                    data_z.append(row.highest_salary)
                    data_a.append(row.lowest_salary)
            return HttpResponse(json.dumps({"marks": 7, "profession":prof.profession_name,"data_x": data_x, "data_y": data_y,"data_z":data_z,"data_a":data_a}))
        else:
            return HttpResponse('getAnalysis error!')

# def forecast(request):
#     data_x=[]
#     data_y=[]
#     data_z=[]
#     if (request.POST.get.biaoming)=="地区预测":
#         list=表名.objects.all()
#         for row in list:
#             if row.profession_id==(request.POST.get.zhiyeming):
#                 #返回地区名，日期和条目数
#                 data_x.append(row.region)
#                 data_y.append(row.date)
#                 data_z.append(row.number)
#         return HttpResponse(json.Deserializer(data_x,data_y,data_z))
#     elif (request.POST.get.biaoming)=="薪水预测":
#         list=表名.objects.all()
#         for row in list:
#             if row.profession_id==(request.POST.get.zhiyeming):
#                 #返回日期和条目数
#                 data_x.append(row.date)
#                 data_y.append(row.number)
#         return HttpResponse(json.Deserializer(data_x,data_y))
#     elif (request.POST.get.biaoming)=="专业预测":
#         '''
#         list=表名.objects.all()
#         for row in list:
#             if row.profession_id==(request.POST.get.zhiyeming):
#                 #返回日期和条目数
#                 data_x.append(row)
#                 data_y.append(row)
#         '''
#         return HttpResponse("你所访问的功能待开发",status=404)
#
#     elif (request.POST.get.biaoming)=="岗位预测":
#         '''
#         list=表名.objects.all()
#         for row in list:
#             if row.profession_id==(request.POST.get.zhiyeming):
#                 返回日期h
#                 data_x.append(row)
#                 data_y.append(row)
#         '''
#         return HttpResponse("你所访问的功能待开发",status=404)
#     else :
#         return HttpResponse("你所访问的页面不存在",status=404)
#不断迭代，找到优化感兴趣度量的ARIMA(p,d,q)的值
def salary_forecast(request):
    date = []
    salary = []
    if request.method == "POST":
        pro = request.POST.get("pro")
        pid = Profession.objects.get(profession_name=pro).profession_id
        data = SalaryPrediction.objects.filter(profession_id=pid)
        for row in data:
            date.append(str(row.date))
            salary.append(row.avg_salary)
        time = pd.to_datetime(date)
        data = pd.DataFrame(salary,index=time,columns=['value'])
        res = bestParameter(data)
        predict_value = forcast(res)
        # predict_value.index.name = 'date'
        # predict_value.reset_index(level=None, drop=False, inplace=False)
        predict_value = pd.DataFrame(predict_value,columns=['date','salary'])
        # predict_value.name = 'salary'
        for row in predict_value.itertuples():
        # for index,value in predict_value.items():
            date.append(str(getattr(row,'date').strftime("%Y-%m-%d")))
            salary.append(getattr(row,'salary'))
        return HttpResponse(json.dumps({"date": date, "salary": salary}))


def region_forecast(request):
    if request.method == "POST":
        city = request.POST.get("city")
        pro = request.POST.get("pro")
        pid = Profession.objects.get(profession_name=pro).profession_id
        data=RegionPrediction.objects.filter(profession_id=pid)
        date=[]
        req=[]
        for row in data:
            if (row.region == city):
                date.append(str(row.date))
                req.append(row.number)
        time = pd.to_datetime(date)  # date转为日期类型
        data = pd.DataFrame(req, index=time, columns=['value'])
        results = bestParameter(data)
        predict_value = forcast(results)
        predict_value = pd.DataFrame(predict_value, columns=['date', 'req'])
        for row in predict_value.itertuples():
            # for index,value in predict_value.items():
            date.append(str(getattr(row, 'date').strftime("%Y-%m-%d")))
            req.append(getattr(row, 'req'))
        return HttpResponse(json.dumps({"date": date, "req": req}))


