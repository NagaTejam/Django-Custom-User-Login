from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm,EditProfileForm,ServiceForm,AForm,SForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.utils.http import is_safe_url
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sessions.models import Session
from django.contrib.auth import update_session_auth_hash
from .models import User
from django.contrib import messages
from .decorators import login_check
# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = RegisterForm(data=request.POST)
        if user_form.is_valid(): 
            user_form.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = RegisterForm()
    return render(request, 'signup.html', {
        'user_form':user_form,
        'registered':registered})

'''
def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if request.user.is_admin:
            login(request,user)
            return HttpResponseRedirect(reverse('employee'))
        elif user:
            if user.is_active:
                login(request,user)
                if request.user.is_superuser:
                    return HttpResponseRedirect(reverse('employee'))
                else:
                    return HttpResponseRedirect(reverse('view_profile'))
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Some one tried to login and failed!")
            print("Username:{} and password: {}".format(username,password))
            return HttpResponse("Invalid Login details supplied")
    else:
        return render(request,'login.html',{})
'''
@login_check
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST or None,instance=request.user)
        if user_form.is_valid(): 
            user_form.save()
            return redirect('view_profile')
    else:
        user_form = EditProfileForm(request.POST or None,instance=request.user)
    return render(request,'edit_profile.html',{'user_form':user_form,})

@login_check
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('view_profile')
    else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'change_password.html', {'form': form})

@login_check
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_check
def view_profile(request):
    sess = request.session.get('sess',0)
    request.session['sess'] = sess + 1
    args= {'user':request.user,'sess':sess}
    return render(request,'profile.html',args)

def login_page(request):
    user_form = LoginForm(request.POST or None)
    args = {
        'user_form':user_form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if user_form.is_valid():
        username = user_form.cleaned_data.get('username')
        password = user_form.cleaned_data.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('view_profile')
        else:
            print("Error")
    return render(request,'login.html',args)

#User = get_user_model()

@login_check
def service(request):
    if request.method == 'POST':
        user_form = ServiceForm(data=request.POST)
        u=Session.objects.all()
        if user_form.is_valid():
            user_form.email = request.user.email
            user_form.save()
        else:
            print(user_form.errors)
    else:
        user_form = ServiceForm()
    return render(request, 'service.html', {
        'user_form':user_form})

@login_check
def admin(request):
    Users = User.objects.all()
    args = {'usr':request.user,'Users':Users}
    return render(request,'admin.html',args)

def destroy(request, emp_id):  
    u = User.objects.get(sys_id = emp_id)
    u.delete()
    messages.success(request, ('Item has been ! Deleted'))  
    return redirect("admin")

def edit(request,emp_id):
    if request.method == 'POST':
        emp = User.objects.get(sys_id=emp_id)
        if request.user.is_admin:
            form = AForm(request.POST or None, instance=emp)
        else :
            form = SForm(request.POST or None, instance=emp)    

        if form.is_valid():
            form.save()
            messages.success(request, ('Item has been edited'))
            return redirect('admin')
    else:
        emp = User.objects.get(sys_id=emp_id)
        if request.user.is_admin:
            form = AForm(request.POST or None,instance=emp)
        else :
            form = SForm(request.POST or None,instance=emp)
    return render(request, 'edit.html', {'emp': emp,'form':form})