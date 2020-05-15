from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth import login, logout, authenticate
from django.utils.crypto import get_random_string

from .models import MyUser, PageRandCode, MyContent

from .forms import UserAuthenticationForm, MyUserRegistrationForm

# Create your views here.

def homepage(request):
    return render(request, 'myapp/homepage.html')

def show_user_content(request, username, rand_code):
    context = {}

    user = request.user
    try:
        myuser = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        myuser = None

    try:
        current_user = MyUser.objects.get(username=user.username)
    except MyUser.DoesNotExist:
        current_user = None

    # page_rand_codes = PageRandCode.objects.filter(myuser=myuser)
    # random_codes = [page_rand_code.random_code for page_rand_code in page_rand_codes]
    try:
        required_code = PageRandCode.objects.get(myuser=myuser).random_code
    except MyUser.DoesNotExist:
        required_code = None

    logged_in = False
    if current_user == myuser:
        logged_in = True

    print(username, rand_code)

    # if (user.is_authenticated and logged_in) or (rand_code in random_codes):
    #     mycontent_list = MyContent.objects.filter(myuser=myuser)
    #     context['myuser'] = myuser
    #     context['mycontent_list'] = mycontent_list
    #     context['logged_in'] = logged_in
    #     for random_code in random_codes:
    #         print(random_code)
    #     for mycontent in mycontent_list:
    #         print(mycontent.content)
    #     return render(request, 'myapp/show_user_content.html', context=context)
    if (user.is_authenticated and logged_in) or (rand_code == required_code):
        mycontent_list = MyContent.objects.filter(myuser=myuser)
        context['myuser'] = myuser
        context['mycontent_list'] = mycontent_list
        context['logged_in'] = logged_in
        for mycontent in mycontent_list:
            print(mycontent.content)
        return render(request, 'myapp/show_user_content.html', context=context)

    return HttpResponseNotFound('<h1>Not Found</h1>')

def register_myuser_page(request):

    context = {}

    if request.method == 'POST':
        myuser_registration_form = MyUserRegistrationForm(request.POST)
        if myuser_registration_form.is_valid():
            print('Here')
            myuser = myuser_registration_form.save()
            email = myuser_registration_form.cleaned_data.get('email')
            raw_password = myuser_registration_form.cleaned_data.get('password1')
            pagerandcode = PageRandCode.objects.create(myuser=myuser, random_code = get_random_string(length=20))
            # myuser.set_password(raw_password=raw_password)
            # myuser.pagerandcode = None
            # pagerandcode = PageRandCode()
            # pagerandcode.random_code = get_random_string(length=20)
            # # pagerandcode.myuser = myuser
            # # myuser.pagerandcode = pagerandcode
            # # myuser.save()
            # pagerandcode.save()
            # pagerandcode.myuser = myuser

            authenticated_account = authenticate(email=email, password=raw_password)
            login(request, authenticated_account)

            return redirect('homepage')

        else:
            context['myuser_registration_form'] = myuser_registration_form

    else: # GET request
        myuser_registration_form = MyUserRegistrationForm()

        context['myuser_registration_form'] = myuser_registration_form

    return render(request, 'myapp/register_myuser_page.html', context)

def login_page(request):

    context = {}

    # user = request.user
    if request.user.is_authenticated:
        return redirect('homepage')

    elif request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        print(request.POST['email'])
        print(request.POST['password'])
        if form.is_valid():
            print('Here')
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('homepage')

    else:
        form = UserAuthenticationForm()

    context['form'] = form
    return render(request, 'myapp/login_page.html', context)

def logout_page(request):
    logout(request)
    return redirect('homepage')