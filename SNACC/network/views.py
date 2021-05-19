from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import csv
from network.models import Account, Connection
import sys
from time import sleep

from network.Mapper_Threading import MT_Mapper
from network.trend_node import nodeClassifier

from network.Instascrape import InstaScrape
#Other code and steps go here

global node_db

# Create your views here.
def index(request):
    accounts = Account.objects.all()
    connections = Connection.objects.all()
    context = {
        'accounts' : accounts,
        'connections' : connections,
        }
    return render(request, "network/index.html", context)

def crawl(request):
    output_location_main = r'C:\Users\emari\Documents\Github-Projects\SNACC\SNACC_Mapper\Output'
    sys.path.append(".\SNACC_Post_Collector\.")
    node_db = nodeClassifier(output_location_main)
    post_collector = InstaScrape("https://www.instagram.com/eizagonzalez/")
    #node_db = post_collector.exportNodeDB()
    node_db.output_location = output_location_main
    #node_db.exportNetwork()
    root_driver = post_collector.driver
    mapper = MT_Mapper(root_driver,node_db)
    mapper.threadInitialize()
    #node_db = mapper.exportNodeDB()
    return HttpResponse("Done without a hitch")
    