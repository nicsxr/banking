from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from .models import Account, Transaction, Card
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .management.commands import currency
from uuid import UUID

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
        card = Card(owner=user, money=10)
        card.save()
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
    user_card = Card.objects.get(owner = user)
    my_transactions = Transaction.objects.filter(Q(sender = user_card) | Q(receiver = user_card)).order_by('-time_sent')
    cards = Card.objects.filter(owner=user)
    context = {
        'transactions': my_transactions,
        'cards': cards,
        'currency': currency
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def transaction_view(request, id):

    #check if provided string is uuid
    try:
        UUID(id, version=4)
    except ValueError:
        messages.warning(request, 'Invalid argument!')
        return redirect('/dashboard') 

    #get transaction
    try:
        transaction = Transaction.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.warning(request, 'Transaction does not exist!')
        return redirect('/dashboard')

    #need to check permission !!!!!!!!!!!!!!1

    context = {
        'transaction': transaction
    }
    return render(request, 'dashboard/transaction.html', context)

@login_required
def send_view(request):
    user = request.user
    sender_card = Card.objects.get(owner = user)
    form = SendMoneyForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            #check if card exists
            try:
                receiver_card = Card.objects.get(number = form.cleaned_data.get('receiver_card'))
            except ObjectDoesNotExist:
                messages.warning(request, 'Card Not Found!')
                return redirect('/dashboard')
            #transaction
            if receiver_card:
                #check if he's sending to other
                if sender_card.number == receiver_card.number:
                    messages.warning(request, 'You can not send money to yourself!')
                    return redirect('/dashboard')
                #check if user has sufficient funds
                moneyToSend = abs(form.cleaned_data.get('money'))
                if sender_card.money - moneyToSend < 0:
                    messages.warning(request, 'Not enough money!')
                    return redirect('/dashboard')
                
                sender_card.money -= round(moneyToSend, 2)
                receiver_card.money += round(moneyToSend, 2)
                receiver_card.save()
                sender_card.save()
                transcation = Transaction(sender=sender_card, receiver=receiver_card, sent_money=moneyToSend)
                transcation.save()
                messages.success(request, 'Money Sent! <b>Details</b>: ' + str(moneyToSend) + '$ to ' + receiver_card.owner.username)
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

@login_required
def CHECK_CARD_OWNER(request, card):
    try:
        card_owner = Card.objects.get(number = card).owner.username
        return HttpResponse(card_owner)
    except ObjectDoesNotExist:
        return HttpResponse("Card doesn't exist")


def logout_view(request):
    logout(request)
    return redirect('/')
