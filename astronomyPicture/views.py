from django.shortcuts import render,HttpResponse,redirect,reverse
import requests,urllib.parse
from .models import AstronomyPicture
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

#Ana sayfada günün fotoğrafı listeleniyor, listelenen fotoğraf veri tabanına kaydediliyor.
@login_required(login_url="user:login")
def index(request):
    url = "https://api.nasa.gov/planetary/apod?api_key=DIgPWf5KzhMqas706mfEMWnFQhiXs3FxmYOi4TWp"
    response = requests.get(url)
    data = response.json()
    try:
        ownerName=data['copyright']
    except KeyError:
        ownerName=None
    photoInfo=AstronomyPicture(
        owner=ownerName,
        title=data['title'],
        explanation=data['explanation'],
        url=data['url'],
        hdurl=data['hdurl'],
        media_type=data['media_type'],
        service_version=data['service_version'],
        date=data['date']
    )
    try:
        AstronomyPicture.objects.get(url=data['url'],date=data['date'])
    except AstronomyPicture.DoesNotExist:
        photoInfo.save()
    return render(request, 'index.html', {"photoInfo":photoInfo})

#Daha önceden ana sayfada görüntülenmiş fotoğrafları listeliyor.
@login_required(login_url="user:login")
def listAll(request):
    keyword = request.GET.get("keyword")
    if keyword:
        #Başlık ya da yayıncı içeriğini aratma
        photos = AstronomyPicture.objects.filter(Q(title__contains = keyword) | Q(owner__contains=keyword))
        return render(request,"explore.html",{"photos":photos})
    photos=AstronomyPicture.objects.all()
    return render(request, 'explore.html', {"photos":photos})

#Search işlemini sağlıyor. 
@login_required(login_url="user:login")
def listSelected(request,keyword):
    url="https://images-api.nasa.gov/search?q="+keyword
    response = requests.get(url)
    items=json.loads(response.text)['collection']['items']
    descriptions=[]
    titles=[]
    dates=[]
    photoInfos=[]
    firstimg=[]#Gösterilecek olan resimlerin listesi
    firstvid=[]#Gösterilecek olan videoların listesi
    for item in items[:5]:
        temp_imgItems=[]
        temp_vidItems=[]
        urlforimg=item['href']
        imgresponse = requests.get(urlforimg)
        imgItems = imgresponse.json()
        for imgItem in imgItems:
            if imgItem.endswith('.jpg') and imgItem.find("video")==-1:
                temp_imgItems.append(imgItem)
            elif imgItem.endswith('.mp4') and imgItem.find("video")>-1:
                temp_vidItems.append(imgItem)
        if temp_imgItems:
            firstimg.append(temp_imgItems[0])
        else:
            firstimg.append(None)
        if temp_vidItems:
            firstvid.append(temp_vidItems[0])
        else:
            firstvid.append(None)
        #href etiketinin içerisinde bulunan url ile istekte bulunarak fotoğraflar elde edildi
        for data in item['data']:
            descriptions.append(data['description'])
            titles.append(data['title'])
            dates.append(data['date_created'])
    #Elde edilen listeler indislerine göre AstronomyPicture modeli içerisinde birleştirildi.        
    for title in titles:
        i=titles.index(title)
        photoInfo=AstronomyPicture(
            title=title,
            explanation=descriptions[i],
            date=dates[i],
            url=firstimg[i],
            hdurl=firstvid[i],#burada video için kullanıldı
        )
        photoInfos.append(photoInfo)
    context={
        "photoInfos":photoInfos,
    }
    return render(request, 'result.html',context )

#Search işlemi için gereken anahtar kelimenin alındığı kısım
@login_required(login_url="user:login")
def searchPage(request):
    keyword = request.GET.get("keyword")
    if keyword:
        return redirect(reverse("search",kwargs={"keyword":keyword}))
    return render(request,"search.html")

@login_required(login_url="user:login")
def detail(request,id):
    photo=AstronomyPicture.objects.get(id=id)
    return render(request, 'detail.html', {"photoInfo":photo})
