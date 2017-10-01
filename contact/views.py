# -*- coding: utf-8 -*-
from django.shortcuts import render


# Create your views here.
def get_contact(request):
    return render(request,'contact.html')