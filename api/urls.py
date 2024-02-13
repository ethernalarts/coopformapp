
from django.urls import include, re_path
from django.conf.urls.static import static
from django.conf import settings
from .api_views import *
from form.views import CoopLoginView, CoopLogoutView, finish

urlpatterns = [
    re_path(r'^test/$', test),
    re_path(r'^form/all/$', AllCooperativesList.as_view(), name='api-allcooperatives'),
    re_path(r'^form/register/$', RegisterCooperative.as_view(), name='api-registercooperative'),
    re_path(r'^form/(?P<pk>\d+)/$', RetrieveCooperative.as_view(), name='api-retrievecooperative'),
    re_path(r'^form/(?P<pk>\d+)/update/$', UpdateCooperative.as_view(), name='api-updatecooperative'),
    re_path(r'^form/(?P<pk>\d+)/delete/$', DeleteCooperative.as_view(), name='api-deletecooperative'),
    re_path(r'^form/search/$', APISearchCooperative.as_view(), name='api-searchresult'),
    re_path(r'^form/(?P<pk>\d+)/finish/$', finish, {'template_name': 'api-finish.html'}, name='api-finish'),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    
    # Authentication
    re_path(r'^login/$',CoopLoginView.as_view(template_name="api-login.html"), name='api-login'),
    re_path(r'^logout/$', CoopLogoutView.as_view(), name='api-logout'),
    
    # htmx urlpatterns/delete share capital file
    re_path(r'^form/(?P<pk>\d+)/(?P<coopform_id>\d+)/delete-scfile/$', deletesharecapitalfile, name='deletesharecapitalfile'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    