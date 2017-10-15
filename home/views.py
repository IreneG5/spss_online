# -*- coding: utf-8 -*-
from django.shortcuts import render


def get_index(request):
    """ Render home page """
    return render(request, 'index.html')
