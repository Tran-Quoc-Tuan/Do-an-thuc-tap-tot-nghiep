from django.contrib import admin, messages
from .models import (
    DongSP, SanPham, CauHinh, Mau, Gia,
    ThuongHieu, ChiTietGioHang, HoaDon, ChiTietHoaDon,
    BinhLuan, PhanHoi, Anh, Trạng_thái_sản_phẩm
)


class CauHinhAdmin(admin.TabularInline):
    model = CauHinh

class MauAdmin(admin.TabularInline):
    model = Mau

@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    actions = ['khoaSanPham', 'moSanPham']
    search_fields = ['ten', 'ThuongHieu__ten', 'dongSP__dongSP', 'nam']
    inlines = [MauAdmin, CauHinhAdmin]

    @admin.action(description='Khóa sản phẩm')
    def khoaSanPham(self, request, sanPham):
        updated = sanPham.update(trangThai = Trạng_thái_sản_phẩm.KHÓA)
        self.message_user(request, '%d sản phẩm đã bị khóa!' % updated, messages.WARNING)

    @admin.action(description='Mở sản phẩm')
    def moSanPham(self, request, sanPham):
        updated = sanPham.update(trangThai = Trạng_thái_sản_phẩm.MỞ)
        self.message_user(request, '%d sản phẩm đã được mở!' % updated, messages.SUCCESS)


@admin.register(Gia)
class GiaSanPham(admin.ModelAdmin):
    search_fields = ['sanPham__ten']

class PhanHoiAdmin(admin.TabularInline):
    model = PhanHoi

@admin.register(BinhLuan)
class BinhLuanAdmin(admin.ModelAdmin):
    inlines = [PhanHoiAdmin]
    search_fields = ['user__name', 'soDT', 'sanPham__ten', 'ngayDang']


class ChiTietHDAdmin(admin.TabularInline):
    model = ChiTietHoaDon

@admin.register(HoaDon)
class HoaDonAdmin(admin.ModelAdmin):
    inlines = [ChiTietHDAdmin]
    search_fields = ['user__name', 'tongTien', 'trangThai']


class DongSPAdmin(admin.TabularInline):
    model = DongSP

@admin.register(ThuongHieu)
class ThuongHieuAdmin(admin.ModelAdmin):
    inlines = [DongSPAdmin]
    search_fields = ['ten']

@admin.register(ChiTietGioHang)
class ChiTietGHAdmin(admin.ModelAdmin):
    search_fields = ['user__name', 'sanPham__ten']

admin.site.register(Anh)
