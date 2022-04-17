from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db import models
import enum
import re



def validate_number(phone) -> None:
    try:
        int(phone)
    except ValueError:
        raise ValidationError("Có ký tự không phải số.")
    else:
        if len(phone) < 10: raise ValidationError("Ít hơn 10 số.")
        elif len(phone) > 10: raise ValidationError("Nhiều hơn 10 số.")
        else:
            if re.match(r'^0', str(phone)): return True
            else: raise ValidationError("Không phải số điện thoại.")


class Blank(enum.Enum):
    TEXT_FIELD = "Đang cập nhật"
    NUM_FIELD  = 0

class Trạng_thái_sản_phẩm(models.TextChoices):
    KHÓA         = 'Khóa'
    MỞ           = 'Mở'
    HẾT_HÀNG     = 'Hết hàng'
    CHƯA_CÓ_HÀNG = 'Chưa có hàng'

class Trạng_thái_người_dùng(models.TextChoices):
    KHÓA = 'Khóa'
    MỞ   = 'Mở'
    XÓA  = 'XÓA'

class Trạng_thái_hóa_đơn(models.TextChoices):
    ĐANG_XÁC_NHẬN = 'Đang xác nhận'
    ĐÃ_XÁC_NHẬN   = 'Đã xác nhận'
    HOÀN_TẤT      = 'Hoàn tất'
    ĐÃ_HỦY        = 'Đã hủy'

class Loại_ảnh(models.TextChoices):
    BANNER  = 'Banner'
    PRODUCT = 'Product'


class ThuongHieu(models.Model):
    ten = models.CharField(max_length=40, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Tên thương hiệu")

    def __str__(self) -> str: return self.ten


class DongSP(models.Model):
    ThuongHieu = models.ForeignKey(ThuongHieu, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Thương hiệu")
    dongSP     = models.CharField(max_length=50, verbose_name="Dòng sản phẩm")

    def __str__(self) -> str: return f'{self.dongSP} - {self.ThuongHieu}'


class SanPham(models.Model):
    ten        = models.CharField(max_length=30, default='Unknow', verbose_name="Tên sản phẩm")
    slug       = models.SlugField(blank=True, null=True,verbose_name="Slug")
    ThuongHieu = models.ForeignKey(ThuongHieu, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Thương hiệu")
    dongSP     = models.ForeignKey(DongSP, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Dòng sản phẩm")
    moTa       = models.TextField(default=Blank.TEXT_FIELD.value, verbose_name="Mô tả")
    doPG       = models.CharField(max_length=20, blank=True, null=True, default=Blank.TEXT_FIELD.value, verbose_name="Độ phân giải màn hình")
    doSang     = models.PositiveIntegerField(default=Blank.NUM_FIELD.value, blank=True, null=True, verbose_name="Độ sáng tối đa")
    matCU      = models.CharField(max_length=20, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Chất liệu mặt trước")
    manHinh    = models.DecimalField(max_digits=2, decimal_places=1, default=Blank.NUM_FIELD.value, blank=True, null=True, verbose_name="Kích thước màn hình")
    camTruoc   = models.TextField(default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Thông số camera trước")
    camSau     = models.TextField(default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Thông số camera sau")
    sim        = models.TextField(default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Thông số về SIM")
    IP         = models.CharField(max_length=5, default=None, blank=True, null=True, verbose_name="Tiêu chuẩn kháng nước, bụi")
    kt_tl      = models.TextField(default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Kích thước, trọng lượng")
    chatLieu   = models.CharField(max_length=30, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Chất liệu sản phẩm")
    os         = models.CharField(max_length=20, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Hệ điều hành cài sẵn")
    cpu        = models.CharField(max_length=20, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Chip xử lý")
    cpu_clock  = models.CharField(max_length=10, default="NaN GHz", blank=True, null=True, verbose_name="Tốc độ xử lý")
    gpu        = models.CharField(max_length=20, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Chip đồ họa")
    pin        = models.CharField(max_length=20, default="NaN mAh", blank=True, null=True, verbose_name="Dung lượng pin")
    loaiPin    = models.CharField(max_length=20, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Loại pin")
    nguonSac   = models.CharField(max_length=10, default="NaN w", blank=True, null=True, verbose_name="Công suất sạc tối đa")
    nam        = models.CharField(max_length=10, default=None, blank=True, null=True, verbose_name="Năm ra mắt")
    soLuong    = models.PositiveIntegerField(default=Blank.NUM_FIELD.value, blank=True, null=True, verbose_name="Số lượng sản phẩm")
    trangThai  = models.CharField(max_length=20, default=Trạng_thái_sản_phẩm.KHÓA, choices=Trạng_thái_sản_phẩm.choices, verbose_name="Trạng thái sản phẩm")

    def __str__(self) -> str: return self.ten


class Anh(models.Model):
    sanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Thuộc sản phẩm")
    ten = models.CharField(max_length=20)
    loaiAnh = models.CharField(max_length=7, default=Loại_ảnh.PRODUCT, choices=Loại_ảnh.choices)
    file = models.FileField(blank=True, null=True, upload_to="media/", verbose_name="File ảnh")
    uri = models.URLField(blank=True, null=True, verbose_name="File ảnh")

    def __str__(self) -> str:
        return f"{self.sanPham} - {self.ten}"


class CauHinh(models.Model):
    sanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    ram     = models.PositiveIntegerField(default=Blank.NUM_FIELD.value, blank=True, null=True, verbose_name="Dung lượng RAM")
    rom     = models.PositiveIntegerField(default=Blank.NUM_FIELD.value, blank=True, null=True, verbose_name="Dung lượng ROM")

    def __str__(self) -> str: return f'{self.sanPham} - {str(self.ram)}GB/{str(self.rom)}GB'


class Mau(models.Model):
    sanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    ten     = models.CharField(max_length=20, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Tên màu")
    maMau   = models.CharField(max_length=20, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Mã màu")

    def __str__(self) -> str: return f'{self.sanPham} - {self.ten}'


class Gia(models.Model):
    sanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    cauHinh = models.ForeignKey(CauHinh, on_delete=models.CASCADE, verbose_name="Loại cấu hình")
    mau     = models.ForeignKey(Mau, on_delete=models.CASCADE, verbose_name="Loại màu")
    gia     = models.PositiveIntegerField(default=Blank.NUM_FIELD.value, blank=True, null=True, verbose_name="Giá sản phẩm")

    def __str__(self) -> str:
        return f"{self.sanPham} - {str(self.cauHinh.ram)}GB/{str(self.cauHinh.rom)}GB - {self.mau.ten}"


class CustomUser(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE, editable=False, auto_created=True)
    ngaySinh  = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    soDT      = models.CharField(max_length=10, validators=[validate_number], blank=True, null=True, verbose_name="Số điện thoại")
    diaChi    = models.CharField(max_length=50, default=Blank.TEXT_FIELD.value, blank=True, null=True, verbose_name="Địa chỉ")
    trangThai = models.CharField(max_length=10, choices=Trạng_thái_người_dùng.choices, default=Trạng_thái_người_dùng.KHÓA, verbose_name="Trạng thái người dùng")


class ChiTietGioHang(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    sanPham = models.ForeignKey(SanPham, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Sản phẩm")
    gia     = models.PositiveIntegerField(blank=True, null=True, verbose_name="Giá sản phẩm")

    def __str__(self) -> str: return str(self.gia)


class HoaDon(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    ngayLap   = models.DateTimeField(auto_now=True, verbose_name="Ngày lập hóa đơn")
    tongTien  = models.PositiveBigIntegerField(default=Blank.NUM_FIELD.value, verbose_name="Tổng tiền")
    trangThai = models.CharField(max_length=15, default=Trạng_thái_hóa_đơn.ĐANG_XÁC_NHẬN, choices=Trạng_thái_hóa_đơn.choices, verbose_name="Trạng thái")

    def __str__(self) -> str:
        return f'{self.user} - {datetime.strftime(self.ngayLap, "%H:%M:%S %d/%m/%Y")}'


class ChiTietHoaDon(models.Model):
    hoaDon  = models.ForeignKey(HoaDon, on_delete=models.CASCADE, verbose_name="Hóa đơn")
    sanPham = models.ForeignKey(SanPham, on_delete=models.PROTECT, verbose_name="Sản phẩm")
    soLuong = models.PositiveSmallIntegerField(default=1, verbose_name="Số lượng")
    donGia  = models.PositiveIntegerField(default=0, verbose_name="Đơn giá")

    def __str__(self) -> str: return self.hoaDon


class BinhLuan(models.Model):
    sanPham  = models.ForeignKey(SanPham, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    user     = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Người dùng")
    hoTen    = models.CharField(max_length=50, blank=True, null=True, verbose_name="Họ tên người đăng")
    soDT     = models.CharField(max_length=10, validators=[validate_number], blank=True, null=True, verbose_name="Số điện thoại")
    ngayDang = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    noiDung  = models.TextField(verbose_name="Nội dung bình luận")

    def __str__(self) -> str:
        return f'{self.sanPham} - {self.user | self.hoTen} - {datetime.strftime(self.ngayLap, "%H:%M:%S %d/%m/%Y")}'


class PhanHoi(models.Model):
    binhLuan = models.ForeignKey(BinhLuan, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Bình luận")
    user     = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Người dùng")
    hoTen    = models.CharField(max_length=50, blank=True, null=True, verbose_name="Họ tên người đăng")
    soDT     = models.CharField(max_length=10, validators=[validate_number], blank=True, null=True, verbose_name="Số điện thoại")
    ngayDang = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    noiDung  = models.TextField(verbose_name="Nội dung bình luận")

    def __str__(self) -> str:
        return f'{self.sanPham} - {self.user | self.hoTen} - {datetime.strftime(self.ngayLap, "%H:%M:%S %d/%m/%Y")}'
