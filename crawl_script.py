from bs4 import BeautifulSoup
from pymongo import MongoClient
import dns
from datetime import datetime
from pprint import pprint
from time import sleep
from sys import argv
import requests
import re
# import django
# from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'do_an_thuc_tap.settings'
# django.setup()
# from ban_dt.models import (
#     ThuongHieu, DongSP, SanPham, Anh,
#     Mau, CauHinh, Gia, Trạng_thái_sản_phẩm, Loại_ảnh
# )

MONGO_URL = r"mongodb+srv://TuanTe:matkhau@nodejs.7qnbu.mongodb.net/Project?retryWrites=true&w=majority"

header = {
    'cookie': 'DMX_Personal=%7B%22CustomerId%22%3A0%2C%22CustomerSex%22%3A0%2C%22CustomerName%22%3Anull%2C%22CustomerPhone%22%3Anull%2C%22Address%22%3Anull%2C%22CurrentUrl%22%3Anull%2C%22ProvinceId%22%3A3%2C%22ProvinceName%22%3A%22H%E1%BB%93%20Ch%C3%AD%20Minh%22%2C%22DistrictId%22%3A0%2C%22DistrictType%22%3Anull%2C%22DistrictName%22%3Anull%2C%22WardId%22%3A0%2C%22WardType%22%3Anull%2C%22WardName%22%3Anull%2C%22StoreId%22%3A0%7D; ShowLocationSuggest=hide; _fbp=fb.1.1638164071726.337451399; lhc_per=vid|875355a312a0213070f1; .AspNetCore.Antiforgery.Z2GafvQY0KE=CfDJ8Hg-6B019lZOuTrZRx5b2MBBMopk2_-ZjiuziIscEo_5I0oGDmFTVuUm_g2D8jq_ual7w3ucWjpqb27v9CE9ztV0e3Ky0n8iLTaXnDYWRg_Q7NVj1PQB6R_cXmQqsCYbB3-S0lJ3EGkmwL-douBfOFw; _hjSessionUser_34921=eyJpZCI6ImJmNmIwYWUwLThjZGQtNWFkNC05YzAzLWRhMWQ3ZTkxMzM4ZSIsImNyZWF0ZWQiOjE2NDAwMTA1MDQyMzQsImV4aXN0aW5nIjp0cnVlfQ==; SEARCH_KW_HISTORY=Uc3a39_1pGDEJ1drrbFUXV0WH9KDBxM4PX_j2M8sFTRVmaV2AVrE3iJSGhMThglraoI8zxZJGsWYIBZ4La9CfQ--; .AspNetCore.Antiforgery.vxaTqZ_mpZk=CfDJ8K0bp-0BzBdClfI0XLgcMMWaDTbdNd-hCP949gAuzrWfR2HbdkgbfFrVgui3wqnIA6yaLuESXdJFunNuEVdWxKOZ66vx7evAcsuKdxWMRHiXws-iWwxfojAbtiqi9eSREVxPYRZk8dv_De5YhiLSMEk; __RequestVerificationToken_L2dhbWUtYXBw0=_rsZ0Im1MFvGzgGxFKYGNUzmcbqip1KWAQbDSay04-5pUnvFkmjHCmHLX89oGTKuzJocDwRNjgh6Si7PQ06vYHUh0wc1; chat.info=; chat.username=20220202sfVTCrxmtBudJ5SXAXwC; chat.notifychatmsg=; cebs=1; _ce.s=v~a2dc548f3eab6668766b72161931ad0bbd14435d~vpv~0; mwgishv2=1; _gid=GA1.2.635370422.1651129292; _ga=GA1.2.1170090707.1638164071; _ga_TLRZMSX5ME=GS1.1.1651129291.17.1.1651130881.47; mwgisper=0; SvID=beline2686|YmpEJ|Ymo7z',
    'referer': 'https://www.thegioididong.com/dtdd/samsung-galaxy-s22-ultra?src=osp',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

'''
class ThuongHieuRaw:
    def __init__(self, ten : str) -> None:
        self.ten = ten

    def getObject(self, ten : str = None) -> ThuongHieu:
        ten = self.ten if ten else ten
        try: 
            thuongHieu = ThuongHieu.objects.get(ten = ten)
            log(f'ThuongHieu get {ten}')
        except ObjectDoesNotExist:
            thuongHieu = ThuongHieu.objects.create(ten = ten)
            log(f'ThuongHieu create {ten}')
        except MultipleObjectsReturned:
            thuongHieu = ThuongHieu.objects.filter(ten = ten)[0]
            log(f'ThuongHieu filter {ten}')
        finally: return thuongHieu


class CauHinhRaw:
    def __init__(self, sanPham : SanPham, ram : int, rom : int) -> None:
        self.data = {
            'sanPham': sanPham,
            'ram': ram,
            'rom': rom
        }

    def getObject(self, data : dict = None) -> CauHinh:
        data = self.data if data else data
        try:
            cauHinh = CauHinh.objects.get(data)
            log(f'CauHinh get {data}')
        except ObjectDoesNotExist:
            cauHinh = CauHinh.objects.create(data)
            log(f'CauHinh create {data}')
        except MultipleObjectsReturned:
            cauHinh = CauHinh.objects.filter(data)[0]
            log(f'CauHinh filter {data}')
        finally: return cauHinh


class MauRaw:
    bangMau = {
        'Đen': 'rgb(0, 0, 0)',
        'Đỏ': '#f00',
        'Trắng': '#fff',
        'Xanh lá': 'rgb(0, 255, 0)',
        'Xám': '#5e5e59',
        'Bạc': '#e3e5e3',
        'Vàng đồng': '#fcebd3',
        'Xanh Dương': '#2276bf'
    }

    def __init__(self, sanPham : SanPham = None, ten : str = '') -> None:
        self.data = {
            'sanPham': sanPham,
            'ten': ten,
            'maMau': self.bangMau.get(ten, '#fff')
        }

    def getObject(self, data : dict = None) -> Mau:
        data = self.data if data else data
        try:
            mau = Mau.objects.get(data)
            log(f'Mau get {data}')
        except ObjectDoesNotExist:
            mau = Mau.objects.create(data)
            log(f'Mau create {data}')
        except MultipleObjectsReturned:
            mau = Mau.objects.filter(data)[0]
            log(f'Mau filter {data}')
        finally: return mau


class GiaRaw:
    def __init__(self, sanPham : SanPham = None,
                cauHinh : CauHinh = None,
                mau : Mau = None,
                gia : int = 0) -> None:
        self.data = {
            'sanPham': sanPham,
            'cauHinh': cauHinh,
            'mau': mau,
            'gia': gia,
        }

    def getObject(self, data : dict = None) -> Gia:
        data = self.data if data else data
        try:
            gia = Gia.objects.get(data)
            log(f'Gia get {data}')
        except ObjectDoesNotExist:
            gia = Gia.objects.create(data)
            log(f'Gia create {data}')
        except MultipleObjectsReturned:
            gia = Gia.objects.filter(data)[0]
            log(f'Gia filter {data}')
        finally: return gia


class AnhRaw:
    def __init__(self, sanPham : SanPham = None,
                ten : str = '', loaiAnh : Loại_ảnh = Loại_ảnh.BANNER,
                file = None, uri : str = '') -> None:
        self.data = {
            'sanPham': sanPham,
            'ten': ten,
            'loaiAnh': Loại_ảnh.PRODUCT if sanPham else loaiAnh,
            'file': file,
            'uri': uri
        }

    def getObject(self, data : dict = None) -> Anh:
        data = self.data if data else data
        try:
            anh = Anh.objects.get(data)
            log(f'Anh get {data}')
        except ObjectDoesNotExist:
            anh = Anh.objects.create(data)
            log(f'Anh create {data}')
        except MultipleObjectsReturned:
            anh = Anh.objects.filter(data)[0]
            log(f'Anh filter {data}')
        finally: return anh


class SanPhamRaw:
    def __init__(self,
                ten : str = '',
                ThuongHieu : ThuongHieu = '',
                dongSP : DongSP = None,
                moTa : str = '',
                doPG : str = '',
                doSang : int = 0,
                matCU : str = '',
                manHinh : float = 0.0,
                camTruoc : str = '',
                camSau : str = '',
                sim : str = '',
                IP : str = '',
                kt_tl : str = '',
                chatLieu : str = '',
                os : str = '',
                cpu : str = '',
                cpu_clock : str = '',
                gpu : str = '',
                pin : str = '',
                loaiPin : str = '',
                nguonSac : str = '',
                nam : str = '',
                soLuong : int = 0) -> None:
        self.data = {
            'ten': ten,
            'ThuongHieu': ThuongHieu,
            'dongSP': dongSP,
            'moTa': moTa,
            'doPG': doPG,
            'doSang': doSang,
            'matCU': matCU,
            'manHinh': manHinh,
            'camTruoc': camTruoc,
            'camSau': camSau,
            'sim': sim,
            'IP': IP,
            'kt_tl': kt_tl,
            'chatLieu': chatLieu,
            'os': os,
            'cpu': cpu,
            'cpu_clock': cpu_clock,
            'gpu': gpu,
            'pin': pin,
            'loaiPin': loaiPin,
            'nguonSac': nguonSac,
            'nam': nam,
            'soLuong': soLuong,
            'trangThai': Trạng_thái_sản_phẩm.KHÓA,
        }

    def addToModel(self, *args, **kwargs) -> None:
        try:
            sanPham = SanPham.objects.get(self.data)
            log(f'SanPham get {self.data}')
        except ObjectDoesNotExist:
            SanPham.objects.create(self.data)
            log(f'SanPham create {self.data}')
        except MultipleObjectsReturned:
            list_sanPham = SanPham.objects.filter(self.data)
            for sanPham in list_sanPham[1:]: sanPham.delete()
            list_sanPham[0].update(self.data)
            list_sanPham[0].save()
            log(f'SanPham filter {self.data}')
        else:
            sanPham.update(self.data)
            log(f'SanPham update {self.data}')

    @classmethod
    def parserHTML(cls, url : str):
        pageSanPham = BeautifulSoup(requests.get(url=url, headers=header).text, 'html.parser')
        idSP = pageSanPham.find('section', class_="detail").get('data-id')
        ul_sp = pageSanPham.find('ul', class_=idSP).find_all('div', class_="liright")
        camSau = ul_sp[2].find('span').text
        camTruoc = ul_sp[3].find('span').text
        listCauHinh = pageSanPham.find('div', class_='box03 group desk').find_all('a', class_='box03__item item ')
        colors = pageSanPham.find('div', class_='box03 color group desk').find_all('a', class_='box03__item item ')
        price = re.sub('\.', '', pageSanPham.find('p', class_='box-price-present').text[:-1])
        moTa = pageSanPham.find('div', class_="content-article")
        data = requests.get(f'https://www.thegioididong.com/Product/GetGalleryItemInPopup?productId={idSP}&isAppliance=false&galleryType=5&colorId=0', headers=header).text
        soup = BeautifulSoup(data, 'html.parser')
        img_alt = soup.find('div', class_="img").find('img').get('alt')
        parameter_items = soup.find_all('div', class_="parameter-item")
        manHinh = parameter_items[0].find_all('div', class_='ctRight')
        OS_CPU = parameter_items[3].find_all('div', class_='ctRight')
        storage = parameter_items[4].find_all('div', class_='ctRight')
        connects = parameter_items[5].find_all('div', class_='ctRight')
        power = parameter_items[6].find_all('div', class_='ctRight')
        utiliti = parameter_items[7].find_all('div', class_='ctRight')
        genaral = parameter_items[8].find_all('div', class_='ctRight')
        img_src = 'https:' + str(soup.find('div', class_="img").find('img').get('src'))
        _sanPham = {
            'ThuongHieu': ThuongHieuRaw(str(img_alt.split(' ')[0])).getObject(),
            'ten': ' '.join(str(img_alt).split(' ')[:-1]) if re.search('GB$', str(img_alt)) else str(img_alt),
            'moTa': moTa,
            'doPG': manHinh[1].text,
            'doSang': manHinh[3].text,
            'matCU': manHinh[4].text,
            'manHinh': manHinh[2].text,
            'camTruoc': camTruoc,
            'camSau': camSau,
            'sim': connects[0].text,
            'IP': utiliti[2].text,
            'kt_tl': genaral[2].text,
            'chatLieu': genaral[1].text,
            'os': OS_CPU[0].text,
            'cpu': OS_CPU[1].text,
            'cpu_clock': OS_CPU[2].text,
            'gpu': OS_CPU[3].text,
            'pin': power[0].text,
            'loaiPin': power[1].text,
            'nguonSac': power[2].text,
            'nam': genaral[3].text,
        }
        sanPham = cls(_sanPham).addToModel()
        AnhRaw(sanPham, _sanPham, uri=img_src)
        Maus = [MauRaw(sanPham, color.text).getObject() for color in colors]
        cauHinh = CauHinhRaw(
            sanPham,
            int(storage[0].text.split(' ')[0]),
            int(storage[1].text.split(' ')[0])
        ).getObject()
        for color in Maus: GiaRaw(sanPham, cauHinh, color, price)
        for cau_hinh in listCauHinh:
            soup = BeautifulSoup(requests.get(url=str(cau_hinh.get('href'))).text, 'html.parser')
            price = re.sub('\.', '', soup.find('p', class_='box-price-present').text[:-1])
            idSP = soup.find('section', class_="detail").get('data-id')
            data = requests.get(f'https://www.thegioididong.com/Product/GetGalleryItemInPopup?productId={idSP}&isAppliance=false&galleryType=5&colorId=0', headers=header).text
            soup = BeautifulSoup(data, 'html.parser')
            storage = parameter_items[4].find_all('div', class_='ctRight')
            cauHinh = CauHinhRaw(
                sanPham,
                int(storage[0].text.split(' ')[0]),
                int(storage[1].text.split(' ')[0])
            ).getObject()
            for color in Maus: GiaRaw(sanPham, cauHinh, color, price)
        return sanPham
'''
def parserHTML(url : str):
    sleep(5)
    pageSanPham = BeautifulSoup(requests.get(url=url, headers=header).text, 'html.parser')
    idSP = pageSanPham.find('section', class_="detail").get('data-id')
    ul_sp = pageSanPham.find('ul', class_=idSP).find_all('div', class_="liright")
    camSau = ul_sp[2].find('span').text
    camTruoc = ul_sp[3].find('span').text
    price = pageSanPham.find('p', class_='box-price-present').text[:-1].replace('.', '').replace('₫', '')
    try: listCauHinh = pageSanPham.find('div', class_='box03 group desk').find_all('a', class_='box03__item item')
    except:
        storage = pageSanPham.find_all('div', class_='liright')
        cauHinhs = [{
            'ram': int(storage[5].text.split(' ')[0]),
            'rom': int(storage[6].text.split(' ')[0]),
            'price': price
        }]
    else:
        storage = pageSanPham.find_all('div', class_='liright')
        cauHinhs = [
            {
                'ram': int(storage[5].text.split(' ')[0]),
                'rom': int(storage[6].text.split(' ')[0]),
                'price': price
            }
        ]
        for cau_hinh in listCauHinh:
            sleep(3)
            url = 'https://www.thegioididong.com' + str(cau_hinh.get('href'))
            soup = BeautifulSoup(requests.get(url, headers=header).text, 'html.parser')
            price = soup.find('p', class_='box-price-present').text[:-1].replace('.', '').replace('₫', '')
            storage = soup.find_all('div', class_='liright')
            cauHinhs.append({
                'ram': int(storage[5].text.split(' ')[0]),
                'rom': int(storage[6].text.split(' ')[0]),
                'price': price
            })
    colorImgs = pageSanPham.find_all('div', class_='item itemTab')
    colors = pageSanPham.find('div', class_='box03 color group desk').find_all('a', class_='box03__item item')
    maus = [
        {
            'ten': color.text,
            'ma': color.get('data-color')
        } for color in colors
    ]
    a = list()
    for colorImg in colorImgs:
        if (data_color := colorImg.get('data-color-id')) != '0':
            a.append(
                {
                    'ma': data_color,
                    'url': colorImg.find('img').get('data-src')
                }
            )

    for mau in maus:
        for colorImg in a:
            if mau['ma'] == colorImg['ma']: mau |= colorImg
    moTa = pageSanPham.find('div', class_="content-article")
    sleep(2)
    data = requests.get(f'https://www.thegioididong.com/Product/GetGalleryItemInPopup?productId={idSP}&isAppliance=false&galleryType=5&colorId=0', headers=header).text
    soup = BeautifulSoup(data, 'html.parser')
    img_alt = soup.find('div', class_="img").find('img').get('alt')
    parameter_items = soup.find_all('div', class_="parameter-item")
    manHinh = parameter_items[0].find_all('div', class_='ctRight')
    OS_CPU = parameter_items[3].find_all('div', class_='ctRight')
    connects = parameter_items[5].find_all('div', class_='ctRight')
    power = parameter_items[6].find_all('div', class_='ctRight')
    utiliti = parameter_items[7].find_all('div', class_='ctRight')
    genaral = parameter_items[8].find_all('div', class_='ctRight')
    img_src = 'https:' + str(soup.find('div', class_="img").find('img').get('src'))
    _sanPham = {
        'ThuongHieu': str(img_alt.split(' ')[0]),
        'ten': ' '.join(str(img_alt).split(' ')[:-1]) if re.search('GB$', str(img_alt)) else str(img_alt),
        'moTa': str(moTa),
        'doPG': manHinh[1].text.strip('\n'),
        'doSang': manHinh[3].text.strip('\n'),
        'matCU': manHinh[4].text.strip('\n'),
        'manHinh': manHinh[2].text.strip('\n'),
        'camTruoc': camTruoc,
        'camSau': camSau,
        'sim': connects[0].text.strip('\n'),
        'IP': utiliti[2].text.strip('\n'),
        'kt_tl': genaral[2].text.strip('\n'),
        'chatLieu': genaral[1].text.strip('\n'),
        'os': OS_CPU[0].text.strip('\n'),
        'cpu': OS_CPU[1].text.strip('\n'),
        'cpu_clock': OS_CPU[2].text.strip('\n'),
        'gpu': OS_CPU[3].text.strip('\n'),
        'pin': power[0].text.strip('\n').split(' ')[0],
        'loaiPin': power[1].text.strip('\n'),
        'nguonSac': power[2].text.strip('\n'),
        'nam': genaral[3].text.strip('\n'),
        'anh': [
            {
                'loai': 'san pham',
                'uri': img_src
            }
        ],
        'mau': maus,
        'cau hinh': cauHinhs
    }
    # pprint(_sanPham, sort_dicts=False)
    return _sanPham


def crawl_log(log_string : str, type_log : str = 'NORMAL',file : bool = True):
    content = f'[{datetime.strftime(datetime.now(), "%H:%M:%S %d/%m/%Y")}] {log_string}\n'
    if type_log == 'ERROR': print(f'\033[1;31m{content}\033[0m')
    else: print(content)
    if file:
        with open('crawl_log.txt', 'a+') as f: f.write(content)


if __name__ == '__main__':
    urls = ['https://www.thegioididong.com/dtdd/samsung-galaxy-a22-4g?src=osp', 'https://www.thegioididong.com/dtdd/iphone-13?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-s20-fan-edition?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-z-flip-3?src=osp', 'https://www.thegioididong.com/dtdd/realme-8?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a33?src=osp', 'https://www.thegioididong.com/dtdd/iphone-11?src=osp', 'https://www.thegioididong.com/dtdd/iphone-12-pro-max-256gb?src=osp', 'https://www.thegioididong.com/dtdd/iphone-13-mini?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-redmi-note-11s-5g?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-s22-ultra?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-redmi-10-4gb-128gb?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a12-2021?src=osp', 'https://www.thegioididong.com/dtdd/realme-c25y-64gb?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-s21?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-m53?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-redmi-note-11-4gb-64gb?src=osp', 'https://www.thegioididong.com/dtdd/oppo-a16?src=osp', 'https://www.thegioididong.com/dtdd/realme-c25s?src=osp', 'https://www.thegioididong.com/dtdd/realme-c21y-3gb?src=osp', 'https://www.thegioididong.com/dtdd/vivo-v20-2021?src=osp', 'https://www.thegioididong.com/dtdd/nokia-g21?src=osp', 'https://www.thegioididong.com/dtdd/oppo-reno7-z?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a73?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-z-fold-3?src=osp', 'https://www.thegioididong.com/dtdd/iphone-12?src=osp', 'https://www.thegioididong.com/dtdd/realme-9i-4gb-64gb?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-s21-plus?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a52?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-s22?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-mi-11-lite-4g?src=osp', 'https://www.thegioididong.com/dtdd/iphone-13-pro?src=osp', 'https://www.thegioididong.com/dtdd/realme-9-pro?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-s21-fe-6gb?src=osp', 'https://www.thegioididong.com/dtdd/iphone-xr-128gb?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-redmi-note-10-pro?src=osp', 'https://www.thegioididong.com/dtdd/vivo-y21?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-11t?src=osp', 'https://www.thegioididong.com/dtdd/oppo-reno7-pro?src=osp', 'https://www.thegioididong.com/dtdd/nokia-g11?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-redmi-note-11-pro-4g?src=osp', 'https://www.thegioididong.com/dtdd/realme-c35?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a13-4g?src=osp', 'https://www.thegioididong.com/dtdd/vivo-y53s?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-11t-pro-5g-8gb?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-s22-plus?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a03?src=osp', 'https://www.thegioididong.com/dtdd/vivo-y72-5g?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a53?src=osp', 'https://www.thegioididong.com/dtdd/oppo-reno7-4g?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-note-20?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-redmi-10c?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-m33-5g?src=osp', 'https://www.thegioididong.com/dtdd/iphone-13-pro-max?src=osp', 'https://www.thegioididong.com/dtdd/vivo-v23e?src=osp', 'https://www.thegioididong.com/dtdd/oppo-a76-4g?src=osp', 'https://www.thegioididong.com/dtdd/realme-c21-y-3gb?src=osp', 'https://www.thegioididong.com/dtdd/nokia-g10?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a32-4g?src=osp', 'https://www.thegioididong.com/dtdd/oppo-a95-4g?src=osp', 'https://www.thegioididong.com/dtdd/oppo-reno6?src=osp', 'https://www.thegioididong.com/dtdd/oppo-a55-4g?src=osp', 'https://www.thegioididong.com/dtdd/oppo-a74-5g?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a52s-5g?src=osp', 'https://www.thegioididong.com/dtdd/vivo-y15s-2021?src=osp', 'https://www.thegioididong.com/dtdd/vivo-y33s?src=osp', 'https://www.thegioididong.com/dtdd/oppo-a15s?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a03s?src=osp', 'https://www.thegioididong.com/dtdd/iphone-12-mini?src=osp', 'https://www.thegioididong.com/dtdd/oppo-reno5-5g?src=osp', 'https://www.thegioididong.com/dtdd/iphone-se-2022?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-redmi-note-10s-6gb?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-mi-12?src=osp', 'https://www.thegioididong.com/dtdd/iphone-se-64gb-2020-hop-moi?src=osp', 'https://www.thegioididong.com/dtdd/iphone-12-pro-256gb?src=osp', 'https://www.thegioididong.com/dtdd/vivo-v21-5g?src=osp', 'https://www.thegioididong.com/dtdd/oppo-reno4-pro?src=osp', 'https://www.thegioididong.com/dtdd/xiaomi-11-lite-5g-ne?src=osp', 'https://www.thegioididong.com/dtdd/samsung-galaxy-a23?src=osp']
    print(urls)
    try: start_point = int(argv[1])
    except IndexError:
        start_point = 0
    except ValueError:
        start_point = urls.index(argv[1])
    for url in urls[start_point:]:
        crawl_log(f'Start point: {urls.index(url)}')
        crawl_log(f'Url: {url}')
        try:
            sanPham = parserHTML(url)
        except:
            crawl_log(f'Error in point {urls.index(url)}', type_log='ERROR')
            continue
        client = MongoClient(MONGO_URL)
        db = client['Project']
        SanPhamCollection = db['SanPham']
        result = SanPhamCollection.insert_one(sanPham)
        if result: crawl_log('Insert success %s' %sanPham['ten'])
        else:
            print("\033[1;31mERROR\033[0m")
            exit()
        crawl_log(sanPham['ten'])
