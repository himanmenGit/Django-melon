from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

__all__ = (
    'login_view',
)


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
