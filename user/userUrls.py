from django.contrib import admin
from django.urls import path
from . import views

app_name="user"

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.loginUsr,name="login"),
    path('logout/',views.logoutUsr,name="logout"),
    path('profile/<int:id>',views.profile,name="profile"),
    path('profile/update',views.updateProfile,name="updateProfile"),
    path('profile/updatePicture',views.updateProfilePicture,name="updatePicture"),
    path('profile/updatePassword',views.updatePassword,name="updatePassword"),
]
