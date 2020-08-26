from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="img_list"),
    path('img_add', views.add_new_image_view, name='img_add'),
    path('img/<int:img_id>', views.img_edit, name="img_edit"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
