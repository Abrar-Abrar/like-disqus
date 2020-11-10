from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignUpForm, UserProfileForm
from .utils import send_confirmation_email
from .tokens import confirm_email_token_generator
from .decorators import unauthenticated_user
from .models import Member

User = get_user_model()

# Create your views here.


@unauthenticated_user
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_confirmation_email(request, user)
            return render(request, 'registration/signup-success.html')
        else:
            messages.info(
                request, 'Password should be letters, numbers, \
                   and symbols!')
            messages.info(request, 'Be sure that both password are identical')
            messages.info(request, 'You should fill all fields!')
            messages.info(request, 'Dont assign with same email twice!')

    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required
def account_settings(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = UserProfileForm(instance=member)

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form}
    return render(request, 'profile/account_settings.html', context)


def activate_email(request, uid, token):
    user = get_object_or_404(User, pk=uid)
    if confirm_email_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponseBadRequest('Bad Token')
