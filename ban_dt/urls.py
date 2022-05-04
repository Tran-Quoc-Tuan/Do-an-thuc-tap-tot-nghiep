from django.urls import path
from .views import (
    index, newest, thuongHieu, log_in, log_out,
    detail
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='index'),
    path('san_pham/newest', newest),
    path('san_pham/<str:_id>', detail),
    path('thuong_hieu/', thuongHieu),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
