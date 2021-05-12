from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import csv
from network.models import Account, Connection

# Create your views here.
def index(request):
    accounts = Account.objects.all()
    connections = Connection.objects.all()
    context = {
        'accounts' : accounts,
        'connections' : connections,
        }
    return render(request, "network/index.html", context)