from django.shortcuts import render
from .models import SanPham, Anh


def index(request):
    a = Anh.objects.all()
    return render(request, 'test.html', {'images': a})
