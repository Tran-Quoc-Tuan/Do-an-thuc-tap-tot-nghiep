from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
# from .models import SanPham, Anh
from .mongodb import SanPham, ThuongHieu, GioHang
import pprint
import json
from django.http import HttpResponse
from django.http.response import JsonResponse


def XMLHttpResponse(request, data):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(json.dumps(data), content_type="application/json")
    return HttpResponse(pprint.pformat(data, sort_dicts=False), content_type="application/json")


def index(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(json.dumps(SanPham.newest()), content_type="application/json")
    return render(request, 'index.html')


def newest(request):
    return XMLHttpResponse(request, SanPham.newest())


def thuongHieu(request):
    try:
        thuongHieu = request.GET['thuong hieu']
        print(thuongHieu)
    except KeyError:
        return XMLHttpResponse(request, ThuongHieu.all())
    else:
        return XMLHttpResponse(request, SanPham.get_with_ThuongHieu(thuongHieu))


def detail(request, _id):
    return XMLHttpResponse(request, SanPham.chiTiet(_id))



def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            print(login(request, user))
            return HttpResponse("Login success!")
        else: return HttpResponse("Login false!")
    return render(request, 'index.html')


def log_out(request):
    logout(request)
    return redirect('index')
