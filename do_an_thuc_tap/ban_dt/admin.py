from re import S
from django.contrib import admin
from .models import (
    DongSP, SanPham, CauHinh, Mau, Gia,
    ThuongHieu, ChiTietGioHang, HoaDon, ChiTietHoaDon,
    BinhLuan, PhanHoi, Anh
)
admin.site.register(DongSP)
admin.site.register(SanPham)
admin.site.register(CauHinh)
admin.site.register(Mau)
admin.site.register(Gia)
admin.site.register(ThuongHieu)
admin.site.register(ChiTietGioHang)
admin.site.register(HoaDon)
admin.site.register(ChiTietHoaDon)
admin.site.register(BinhLuan)
admin.site.register(PhanHoi)
admin.site.register(Anh)
