from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

from .forms import SignupForm

User = get_user_model()


def login_view(request):
    # POST 요청 일 때는
    # authenticate -> login 후 'index'로 redirect
    #   실패시에는 다시 GET 요청의 로직으로 이동
    #
    # GET 요청 일 때는
    # members/login.html 파일을 보여줌
    #   해당 파일에는 username, password input과 '로그인' 버튼이 있음
    #   from은 method POST로 다시 이 view로의 action(빈 값)을 가짐

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

    # POST/GET 상관없이 쏜다!
    # 유저 인증 성공 했으면
    if request.user.is_authenticated:
        return redirect('index')
    # 유저 인증 실패 했으면
    return render(request, 'members/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            is_valid = True

            if User.objects.filter(username=username).exists():
                form.add_error('username', '이미 사용되고 있는 아이디 입니다.')
                is_valid = False
            if password != password2:
                form.add_error('password2', '비밀번호와 비밀번호 확인란이 값이 다릅니다.')
                is_valid = False
            if is_valid:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('index')
    else:
        form = SignupForm()
    context = {
        'signup_form': form
    }
    return render(request, 'members/signup.html', context)
