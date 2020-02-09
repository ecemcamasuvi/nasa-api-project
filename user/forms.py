from django import forms
from django.contrib.auth.models import User
class RegisterForm(forms.Form):
    name=forms.CharField(max_length=30,label="Name")
    lastname=forms.CharField(max_length=30,label="Last Name")
    email=forms.EmailField(label="Email",widget=forms.EmailInput)
    username=forms.CharField(max_length=15,label="Username")
    password=forms.CharField(max_length=15,min_length=8,label="Password",widget=forms.PasswordInput)
    confirm=forms.CharField(max_length=15,min_length=8,label="Confirm Password",widget=forms.PasswordInput)

    def clean(self):
        name = self.cleaned_data.get("name")
        lastname = self.cleaned_data.get("lastname")
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords don't match")

        emailControll=User.objects.filter(email=email)
        if emailControll.exists():
            raise forms.ValidationError("This email has been used before. Please choose a different email")

        usernameControll=User.objects.filter(username=username)
        if usernameControll.exists():
            raise forms.ValidationError("This username has been used before. Please choose a different username")
        values = {
            "username" : username,
            "password" : password,
            "name" : name,
            "lastname" : lastname,
            "email" : email
        }
        return values

class LoginForm(forms.Form):
    username=forms.CharField(max_length=15,label="Username")
    password=forms.CharField(max_length=15,min_length=8,label="Password",widget=forms.PasswordInput)

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email"]

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id')
        super(UpdateForm, self).__init__(*args, **kwargs)


    def clean(self):
        name = self.cleaned_data.get("first_name")
        lastname = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
       
        if User.objects.filter(email=email):
            emailControl=User.objects.get(email=email)
            if emailControl.id!=self.id:
                raise forms.ValidationError("This email has been used before. Please choose a different email")

        if User.objects.filter(username=username):
            usernameControl=User.objects.get(username=username)
            if usernameControl.id!=self.id:
                raise forms.ValidationError("This username has been used before. Please choose a different username")
        values = {
            "username" : username,
            "first_name" : name,
            "last_name" : lastname,
            "email" : email
        }
        return values

class PasswordForm(forms.Form):
  
    newpassword=forms.CharField(max_length=15,min_length=8,label="New Password",widget=forms.PasswordInput)
    confirm=forms.CharField(max_length=15,min_length=8,label="Confirm New Password",widget=forms.PasswordInput)
    password=forms.CharField(max_length=15,min_length=8,label="Previous Password",widget=forms.PasswordInput)
    userid=forms.IntegerField(widget = forms.HiddenInput(), required = False)
    def clean(self):
        newpassword=self.cleaned_data.get("newpassword")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        userid=self.cleaned_data.get("userid")
        if newpassword and confirm and newpassword != confirm:
            raise forms.ValidationError("Passwords don't match")
        
        if newpassword and password and newpassword == password:
            raise forms.ValidationError("The new password cannot be the same as the old one")

        if User.objects.filter(id=userid):
            passwordControl=User.objects.get(id=userid)
            if passwordControl.password!=password:
                raise forms.ValidationError("You entered your previous password incorrectly")

        values = {
            "password" : password,
            "newpassword" : newpassword
        }
        return values

class ConfirmForm(forms.Form):
    password=forms.CharField(max_length=15,min_length=8,label="Please Enter Your Password",widget=forms.PasswordInput)
    userid=forms.IntegerField(widget = forms.HiddenInput(), required = False)
    def clean(self):
        password = self.cleaned_data.get("password")
        userid=self.cleaned_data.get("userid")
        
        if User.objects.filter(id=userid):
            passwordControl=User.objects.get(id=userid)
            if passwordControl.password!=password:
                raise forms.ValidationError(" ")

        values = {
            "password" : password
        }
        return values
