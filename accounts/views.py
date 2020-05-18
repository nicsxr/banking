from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Account, Transaction
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .management.commands import currency

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import UserLoginForm, UserRegisterForm, SendMoneyForm, AccountUpdateForm


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            messages.success(request, 'Successfully logged in! Welcome back ' + username )
            return redirect(next)
        return redirect('/dashboard')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            messages.success(request, 'Registration complete! Welcome to your dashboard ' + user.username)
            return redirect(next)
        messages.success(request, 'Registration complete! Welcome to your dashboard ' + user.username)
        return redirect('/dashboard')

    context = {
        'form': form,
    }
    return render(request, "signup.html", context)

@login_required
def dashboard_view(request):
    user = request.user
    my_transactions = Transaction.objects.filter(sender = user.username).order_by('-time_sent')
    context = {
        'transactions': my_transactions,
        'currency': currency
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def send_view(request):
    user = request.user
    form = SendMoneyForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            #check if card exists
            try:
                receiver = Account.objects.get(card_number = form.cleaned_data.get('receiver_card'))
            except ObjectDoesNotExist:
                messages.warning(request, 'Card Not Found!')
                return redirect('/dashboard')
            #transaction
            if receiver:
                #check if he's sending to other
                if user.card_number == receiver.card_number:
                    messages.warning(request, 'You can not send money to yourself!')
                    return redirect('/dashboard')
                #check if user has sufficient funds
                moneyToSend = abs(form.cleaned_data.get('money'))
                if user.money - moneyToSend < 0:
                    messages.warning(request, 'Not enough money!')
                    return redirect('/dashboard')
                
                user.money -= round(moneyToSend, 2)
                receiver.money += round(moneyToSend, 2)
                receiver.save()
                user.save()
                transcation = Transaction(sender=user.username, receiver=receiver.username, sent_money=moneyToSend)
                transcation.save()
                messages.success(request, 'Money Sent! <b>Details</b>: ' + str(moneyToSend) + '$ to ' + receiver.username)
                return redirect('/dashboard')
        else:
            messages.warning(request, 'Something went wrong')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/send.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated succesfully!')
            return redirect('/dashboard')
        else:
            messages.warning(request, 'Something went wrong!')
            return redirect('/dashboard/profile')

    else:
        form = AccountUpdateForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')
