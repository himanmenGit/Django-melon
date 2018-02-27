from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render

from ..forms import SignupForm

User = get_user_model()
__all__ = (
    'signup_view',
)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    context = {
        'signup_form': form
    }
    return render(request, 'members/signup.html', context)
