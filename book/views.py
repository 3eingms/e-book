import os
from xml.dom.minidom import Document
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Post
# Create your views here.


def home(request):
    return render(request, 'book/home.html')


def signup_user(request):
    if request.method == 'POST':
        fm = SignUp(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Sucessfully!')
            user = fm.save()
            # for adding users in group
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            fm = SignUp()
    else:
        fm = SignUp()
    return render(request, 'book/signup.html', {'fm': fm})


def loginn(request):
    # if request.user.is_authenticated:
    if request.method == 'POST':
        fm = LoginUser(request=request, data=request.POST)
    else:
        fm = LoginUser()
    if fm.is_valid():
        uname = fm.cleaned_data['username']
        upass = fm.cleaned_data['password']
        user = authenticate(username=uname, password=upass)
        if user is not None:
            login(request, user)
            # messages.success(request,'logged in sucessfully')
            return HttpResponseRedirect('/books/')
    return render(request, 'book/login.html', {'fm': fm})
    # else:
    #     return HttpResponseRedirect('/signup/')


def logouts(request):
    logout(request)
    return HttpResponseRedirect('/')

# for posting books


def show_data(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            file2 = request.FILES['file']
            file3 = request.POST['name']
            document = Post.objects.create(Book=file2, name=file3)
            document.save()
            messages.success(request, 'Book uploaded.')
        return render(request, 'book/data.html')
    else:
        return HttpResponseRedirect('/login/')


# all books
def all_book(request):
    data = Post.objects.all()
    print(data)
    return render(request, 'book/all.html', {'data': data})

# download book


def download_book(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response = HttpResponse(
                fh.read(), content_type='application/adminupload')
            response['Content-Disposition'] = 'inline;filename' + \
                os.path.basename(file_path)
            return response
    raise Http404


def delete_book(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            d = Post.objects.get(pk=id)
            messages.success(request, 'Book Deleted!')
            d.delete()
            return HttpResponseRedirect('/all/')
    else:
        return HttpResponseRedirect('login/')
