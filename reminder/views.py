import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from twilio.base.exceptions import TwilioRestException

from reminder.forms import RemindForm, RemindUserForm
from reminder.models import Remind, RemindUser
from twilio.rest import Client


def home(request):
    return render(request, 'reminder/home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'reminder/signup.html', {'signup_form': RemindUserForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],)
                user.save()
                if user is not None:
                    login(request, user)
                    return redirect('home')
            except IntegrityError:
                return render(request, 'reminder/signup.html',
                              {'signup_form': RemindUserForm(), 'error': 'User is already exist'})
        else:
            return render(request, 'reminder/signup.html',
                {'signup_form': RemindUserForm(), 'error': 'Passwords didn`t match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'reminder/loginuser.html', {'form': AuthenticationForm()})
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'reminder/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Wrong data. Please try again'})


def logoutuser(request):
    if request.method == 'POST':  # excecute the command just if we push the button
        logout(request)
        return redirect('home')


def create(request):
    if request.method == 'GET':
        return render(request, 'reminder/create.html', {'form': RemindForm()})
    else:
        try:
            form = RemindForm(request.POST, )
            newremind = form.save(commit=False)  # commit=False - to not save object to the DB yet
            newremind.author = request.user
            newremind.save()
            return redirect('home')
        except ValueError:
            return render(request, 'reminder/create.html',
                          {'form': RemindForm()}, {'error': 'Enter right data please.'})


def remindlist(request):
    content = Remind.objects.filter(author=request.user).order_by('remind_date')
    return render(request, 'reminder/remindlist.html', {'content': content})


def remindetail(request, rdr_pk):
    reminder = get_object_or_404(Remind, pk=rdr_pk, author=request.user)
    if request.method == 'GET':
        form = RemindForm(instance=reminder)
        return render(request, 'reminder/remindetail.html', {'reminder': reminder, 'form': form})
    else:
        try:
            form = RemindForm(request.POST, instance=reminder)
            form.save()
            return redirect('remindlist')
        except ValueError:
            return render(request, 'reminder/create.html',
                          {'form': RemindForm()}, {'error': 'Enter right data please.'})


def delete(request, rdr_pk):
    reminder = get_object_or_404(Remind, pk=rdr_pk, author=request.user)
    if request.method == 'POST':
        reminder.delete()
        return redirect('remindlist')


def sendsms(request):
    content = Remind.objects.all()
    account_sid = "AC015c112c2b5761b3a756f528befee2c9"
    auth_token = "a146165a8ac791c156d05d4033838842"
    if request.method == 'POST':
        for smscontent in content:
            if smscontent.remind_date == datetime.date.today():
                tempusers = User.objects.filter(username=smscontent.author)
                for recipient in tempusers:
                    try:
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                            body="I just want to remind, that you have some task for today {date}: {task}. {time} is the deadline!".format(date=str(smscontent.remind_date), task=str(smscontent.title), time=str(smscontent.remind_time)),
                            to=str(recipient.username),
                            from_="+18568889437")
                        print(message.sid)
                    except TwilioRestException:
                        pass
    return redirect('home')
