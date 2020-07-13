from django.shortcuts import render

from myApp.models import *
from django.core import serializers
#导入HttpResponse 框架
from django.shortcuts import HttpResponse
import json
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
            print(list)
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



def function2(request,argument1,argument2,argument3):
    data_x=[]
    data_y=[]
    data_z=[]
    data_a=[]
    #绘制图三，
    if ( (argument2=="region")&(argument3=="number")):
        list = Region.objects.all()
        for row in list:
            if (row.profession_id==int(argument1)):
                data_x.append(row.region)
                data_y.append(row.number)
        return HttpResponse(data_x+data_y)
        #return render(request,"Run.html",{"masks":argument1,"data_x":data_x,"data_y":data_y})

    elif ( (argument2=="region")&(argument3=="salary")):
        list = Region.objects.all()
        for row in list:
            if(row.profession_id==int(argument1)):
                data_x.append(row.region)
                data_y.append(row.lowest_salary)
                data_z.append(row.highest_salary)
        return HttpResponse(data_x+data_y+data_z)
    # return render(request,"文件名.html",{"横坐标列表":data_x,"第一纵坐标列表":data_y,""})
    elif ( (argument2=="education")&(argument3=="number")):
        list = Education.objects.all()
        for row in list:
            if(row.profession_id==int(argument1)):
                data_x.append(row.education)
                data_y.append(row.number)
        return HttpResponse(data_x+data_y)

    elif ((argument2=="experience")&(argument3=="number")):
        list =Experience.objects.all()
        for row in list:
            if(row.profession_id==int(argument1)):
                data_x.append(row.experiene)
                data_y.append(row.number)
        return HttpResponse(data_x+data_y)

    elif ((argument2=="education")&(argument3=="salary")):
        list =Education.objects.all()
        for row in list:
            if(row.profession_id==int(argument1)):
                data_x.append(row.education)
                data_y.append(row.avg_salary)
                data_z.append(row.highest_salary)
                data_a.append((row.lowest_salary))
        return HttpResponse(data_x+data_y+data_z+data_a)

    elif (argument2.equal("experience")&argument3.equal("salary")):
        list =Experience.objects.all()
        for row in list :
            if(row.profession_id==int(argument1)):
                data_x.append(row.experiene)
                data_y.append(row.avg_salary)
                data_z.append(row.highest_salary)
                data_a.append(row.lowest_salary)
        return HttpResponse(data_x+data_y+data_z+data_a)
    else:
        return HttpResponse("function2 error")



def forecast(request,argument):
    if ():
        print("return data")