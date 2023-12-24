from django.shortcuts import render
from django.http import HttpResponse
from subapp.models import Account
# Create your views here.

def start(request):
    Account.objects.create(amount = 10, currency='inr')

    data = Account.objects.all()
    print(data)

    return HttpResponse("<h1> check databse </h1>")



