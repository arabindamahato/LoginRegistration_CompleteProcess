from django.shortcuts import render
from myapp.forms import *
from django.core.mail import send_mail

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse


# Create your views here.


# User registration function
def registration(request):
    registered = False
    if request.method == "POST" and request.FILES:
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            send_mail(
                'Registration Successfull',
                'Your registration is successfull, Thanks for registering',
                'arabindamahatojhantu@gmail.com', 
                [user.email],
                fail_silently=False,
            )
            registered = True
    user_form = UserForm()
    profile_form = ProfileForm()
    f = {'registered':registered,'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'registration.html', context=f)



# User login function
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user and user.is_active:
            login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("Not an Active user or Invalid username or password")

    return render(request, 'login.html', context={})


# Getting User Name on HTML Page 
def home(request):
    if request.session.get('username'):
        user = request.session.get('username')
        return render(request, 'home.html', context={'username':user})
    return render(request, 'home.html')



@login_required 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        user = User.objects.get(username = username)
        if user:
            user.set_password("10101")
            send_mail(
                    'New Password',
                    'Your Password is reset successfully and your new password is \"10101\"',
                    'arabindamahatojhantu@gmail.com',
                    [user.email],
                    fail_silently=False,
                    )
            user.save()
        else:
            return HttpResponse("Invalid User")
    return render(request,'forgot_pwd.html')


@login_required
def user_profile(request):
        username = request.session['username']
        user = User.objects.get(username=username)
        # print(user.password)
        profile = Profile.objects.get(user=user)
        data = {'profile':profile}
        return render(request, 'profile.html',context=data)


@login_required
def change_password(request):
    username = request.session["username"]
    user = User.objects.get(username=username)
    if request.method == "POST":
        password = request.POST["newpassword"]
        user.set_password(password)
        user.save()
        HttpResponseRedirect(reverse('logout'))
    return render(request, 'change_pwd.html')


    


git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/arabindamahato/LoginRegistration_CompleteProcess.git
git push -u origin master













