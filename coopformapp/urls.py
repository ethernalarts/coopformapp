from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from form import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),     
    path('howtoregister/', views.howtoregister, name='howtoregister'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('test/', views.test),
    
    # Form
    path('form/', include('form.urls')), 
    
    # Auth
    re_path(r'^login/$', views.CoopLoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.CoopLogoutView.as_view(), name='logout'),
    
    # API
    path('api/', include('api.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
