from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

from members.forms import SignupForm

User = get_user_model()


def login_view(request):
    context = {
        'errors': [],
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        is_valid = True
        if not User.objects.filter(username=username).exists():
            error = 'User does not exists'
            context['errors'].append(error)
            is_valid = False
        if not check_password(password, User.objects.get(username=username).password):
            error = 'Password does not match'
            is_valid = False
            context['errors'].append(error)
        if is_valid:
            user = authenticate(request, username=username, password=password)
            # authenticate -> login, redirect to 'index'
            if user is not None:
                login(request, user)
                return redirect('index')
    return render(request, 'members/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')
    # /logout/
    # no matter what method is ( GET or POST )


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # is_valid=True
            # if User.objects.filter(username=username).exists():
            #     form.add_error('username','username already exists')
            #     is_valid=False
            # if password != password_confirm:
            #     form.add_error('password','password confirmation failed')
            #     is_valid=False
            # if is_valid:
            User.objects.create_user(username=username, password=password)
            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'signup_form': form,
    }
        # username = request.POST['username']
        # password = request.POST['password']
        # password_confirm = request.POST['password_confirm']
        #
        # is_valid = True
        # if User.objects.filter(username=username).exists():
        #     error = 'Username already exists'
        #     context['errors'].append(error)
        #     is_valid = False
        # if password != password_confirm:
        #     error = 'Password confirmation failed'
        #     context['errors'].append(error)
        #     is_valid = False
        # if is_valid:
        #     user = User.objects.create_user(
        #         username=username,
        #         password=password,
        #     )
        #     user.save()
        #     return redirect('index')
    return render(request, 'members/signup.html', context)
    # /signup/
    # consider - username, password, password 2(for confirmation)
    # check whether username exists,
    # if not -> create user / redirect to index
    # if it is -> signup again
