from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request,"index.html")
def register(request):
    if request.method=="POST":
        first=request.POST['fname']
        last=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['Email']
        p1=request.POST['pass']
        p2=request.POST['cpass']
        if p1==p2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email Exits")
                return render(request,"register.html")
            elif User.objects.filter(username=uname).exists():
                messages.info(request,"Username available")
                return render(request,"register.html")
            else: 
                #Store value in database
                user=User.objects.create_user(first_name=first,last_name=last,username=uname,email=email,password=p1)
                user.save()
                return HttpResponseRedirect('login')
        else:
            messages.info(request,"Password not matched")
            return render(request,"register.html")
    else:
        return render(request,"register.html")
    return render(request,"register.html")
def login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        ps=request.POST['pass']
        user=auth.authenticate(username=uname,password=ps)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect ('index')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
        
    return render(request,"login.html")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('index')
def about(request):
    return render(request,"about.html")
def data(request):
    if request.method=="POST":
        Nitrogen=float(request.POST['Nitro'])
        Phosphorous=float(request.POST['Phos'])
        Potassium=float(request.POST['Potas'])
        Temperature=float(request.POST['Temp'])
        Humidity=float(request.POST['Hum'])
        Phval=float(request.POST['Ph'])
        Rainfall=float(request.POST['Rain'])
        import pandas as pd 
        df=pd.read_csv(r"static\dataset\Crop_recommendation.csv")
        print(df.head)
        print(df.isnull().sum())
        print(df.dropna(inplace=True))
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()
        X=df.drop("crop",axis=1)
        y=df["crop"]
        from sklearn.linear_model import LogisticRegression
        log=LogisticRegression()
        log.fit(X,y)
        import numpy as np 
        pred_input=np.array([[Nitrogen,Phosphorous,Potassium,Temperature,Humidity,Phval,Rainfall]],dtype=object)
        pred_outcome=log.predict(pred_input)
        print(pred_outcome)
        return render(request,"recommend.html",{"Nitro":Nitrogen,"Phos":Phosphorous,"Potas":Potassium,"Temp":Temperature,"Hum":Humidity,
        "Ph":Phval,"Rain":Rainfall,"prediction":pred_outcome})
        
    return render(request,"data.html")
def recommend(request):
    return render(request,"recommend.html")
def fdata(request):
    if request.method=="POST":
        Nitrogen=int(request.POST['Nitro'])
        Phosphorous=int(request.POST['Phos'])
        Potassium=int(request.POST['Potas'])
        Temperature=int(request.POST['Temp'])
        Humidity=int(request.POST['Hum'])
        Moist=int(request.POST['Mois'])
        soil=request.POST['Soil']
        crop=request.POST['Crop']
        import pandas as pd
        df=pd.read_csv(r"static/dataset2/Fertilizer Prediction.csv")
        print(df.head)
        print(df.isnull().sum())
        print(df.dropna(inplace=True))
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()
        soil1=l.fit_transform([soil])
        Soil=l.fit_transform(df["SOIL"])
        df["Soil"]=Soil

        crop1=l.fit_transform([crop])
        Crop=l.fit_transform(df["CROP"])
        df["Crop"]=Crop
        df=df.drop(["CROP","SOIL"],axis=1)

        X=df.drop("Fertilizer",axis=1)
        y=df["Fertilizer"]
        from sklearn.linear_model import LogisticRegression
        log=LogisticRegression()
        log.fit(X,y)
        import numpy as np
        pred_input=np.array([[soil1,crop1,Nitrogen,Phosphorous,Potassium,Temperature,Humidity,Moist]],dtype=object)
        pred_outcome=log.predict(pred_input)
        print(pred_outcome)
        return render(request,"frecommend.html",{"Nitro":Nitrogen,"Phos":Phosphorous,"Potas":Potassium,"Temp":Temperature,
        "Hum":Humidity,"Mois":Moist,"Soil":soil,"Crop":crop,"prediction":pred_outcome})
    return render(request,"fdata.html")
def frecommend(request):
    return render(request,"frecommend.html")
  