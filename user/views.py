from django.shortcuts import render,redirect,get_object_or_404,reverse,HttpResponse
from .forms import RegisterForm,LoginForm,UpdateForm,PasswordForm,ConfirmForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from .models import UserProfile
from django import forms
import os, random, string
# Create your views here.

def register(request):
    form=RegisterForm(request.POST or None)
    if form.is_valid():
        name=form.cleaned_data.get("name")
        lastname=form.cleaned_data.get("lastname")
        email=form.cleaned_data.get("email")
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")

        newUser=User(username=username,email=email,first_name=name,last_name=lastname,date_joined=date.today())
        newUser.set_password(password)
        newUser.save()
        #Profil fotoğrafını içeren model
        newUserProfile=UserProfile(user=newUser)
        newUserProfile.save()

        login(request,newUser)
        messages.success(request,"Successfully registered")
        return redirect("index")
    context={
        "form":form
    }
    return render(request,"register.html",context)

def loginUsr(request):
    form=LoginForm(request.POST or None)
    context={
       "form":form
    }
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")

        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"Username or password incorrect")
        else:
            messages.success(request,"Successfully logged in")
            login(request,user)
            return redirect("index")
   
    return render(request,"login.html",context)

def logoutUsr(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect("index")

def profile(request,id):
    profile=get_object_or_404(UserProfile,user_id=id)
    user=User.objects.get(id=id)
    form = ConfirmForm(request.POST or None)
    form.userid=id
    #Profili silme seçeneği onay için parola sormaktadır.Bu form onu kontrol ediyor
    if request.method=='POST':
        if form.is_valid():
            user.delete()
            messages.success(request,"Your profile has been successfully deleted")
            return redirect("index")
        else:
            messages.error(request,"You didn't enter your password correctly")

    context={
        "person":profile,
        "date":profile.user.date_joined.strftime("%d.%m.%Y"),
        "form":form
    }
    return render(request,"profile.html",context)

def updateProfile(request):
    id=request.user.id
    user = get_object_or_404(User,id = id)
    form = UpdateForm(request.POST or None,instance = user, id=id)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        messages.success(request,"Profile information has been successfully updated")
        return redirect("user:profile",id)
    
    return render(request,"update.html",{"form":form})
    

def updateProfilePicture(request):
    id=request.user.id
    profile=get_object_or_404(UserProfile,user_id=id)
    if request.method == 'POST' and request.FILES['imgFile']:
        uploadImage=request.FILES['imgFile']
        if uploadImage.name.endswith('.png') or uploadImage.name.endswith('.jpg'):
            length = 13
            chars = string.ascii_letters + string.digits + '!@#$%^&*()'
            random.seed = (os.urandom(1024))
            randomName = ''.join(random.choice(chars) for i in range(length))
            newName = '%s%s' % (str(randomName),".jpg")
            uploadImage.name=newName
            #Dosyanın adı rastgele değiştirildi.
            profile.user_image=uploadImage
            profile.save()
            messages.success(request,"Profile picture updated successfully")
        else:
            messages.error(request,"Couldn't update your profile picture")
    return redirect("user:profile",id)

def updatePassword(request):
    id=request.user.id
    user=get_object_or_404(User,id=id)
    form = PasswordForm(request.POST or None)
    form.userid=id
    if request.method=='POST':
        if form.is_valid():
            user.set_password(form.cleaned_data.get("newpassword"))
            user.save()
            #Parola güncellendiğinde direkt çıkış yapılıyor. Arka planda tekrardan login olunarak bu önleniyor
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,"Your password has been successfully updated")
            return redirect("user:profile",id)
   
    return render(request,"updatePassword.html",{"form":form})


