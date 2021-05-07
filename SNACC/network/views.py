from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import csv

# Create your views here.
def index(request):
    context = {}
    data = []
    with open(os.path.join(settings.BASE_DIR, 'Partial_Run.csv'), newline = '') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        i = 0 
        for row in rows: 
            if i != 0:
                data.append(row)
            i += 1
        context["connections"] = data
        return render(request, "network/index.html", context)