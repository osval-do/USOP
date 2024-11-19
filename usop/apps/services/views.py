from django.shortcuts import render
from django.urls import path 
from viewflow.contrib.auth import AuthViewset 
from viewflow.urls import Application, Site, ModelViewset

from .models import Region, Service


viewsets=[
    Application(
        title='Regions', 
        icon='world', 
        app_name='services', 
        viewsets=[
            ModelViewset(model=Region),
            ModelViewset(model=Service),
        ]
    ),
]