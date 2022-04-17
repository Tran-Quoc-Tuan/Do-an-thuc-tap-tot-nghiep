from django.shortcuts import render
from .models import SanPham, Anh


def index(request):
    return render(request, 'index.html')
