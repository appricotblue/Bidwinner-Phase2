from django.urls import path,include
from RealCostApp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('generate-app-token/', views.appAuthToken ,name='generate-app-token'),
    path('add-convert-pdf-image/',views.addPdfToImage,name='add-convert-pdf-image'),
    path('delete-pdf-image/',views.deletePdfImage,name='delete-pdf-image'),
    path('delete-pdf-file/',views.deletePdf,name='delete-pdf-file'),
    path('list-pdf-details/',views.listPdfToImage,name='list-pdf-details'),
    path('add-auto-rename-image/',views.addAutoRenameImage,name='add-auto-rename-image'),
    path('similar-image/',views.find_similar_image,name='similar-image')
]    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

