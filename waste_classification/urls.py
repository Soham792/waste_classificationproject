from django.urls import path
from classifier.views import classify_waste, get_history, delete_history_item
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/classify/', classify_waste, name='classify-waste'),
    path('api/history/', get_history, name='get-history'),
    path('api/history/<int:item_id>/', delete_history_item, name='delete-history-item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)