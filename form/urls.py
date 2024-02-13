# from django.conf.urls.defaults import *
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from django_pdfkit import PDFView
from . import views


urlpatterns = [
    # register url
    re_path(r'^new/$', views.RegisterView.as_view(), name='register'),

    # all cooperatives url
    re_path(r'^allcooperatives/$',
            views.cooperativesListView.as_view(), name='allcooperatives'),

    # form details url
    re_path(r'^(?P<pk>\d+)$', views.formDetailsView.as_view(
        template_name='formdetails.html'), name='formdetails'),

    # get_printout_url
    re_path(r'^(?P<pk>\d+)/printout/$', views.formDetailsView.as_view(
        template_name='printout-test.html'), name='printout'),

    # update form url
    re_path(r'^(?P<pk>\d+)/update/$',
            views.updateFormView.as_view(), name='updateform'),

    # Delete Form URL
    re_path(r'^(?P<pk>\d+)/delete/$', views.delete_form, name='deleteform'),

    # Finish URL
    re_path(r'^(?P<pk>\d+)/finish/$', views.finish,
            {'template_name': 'finish.html'}, name='finish'),

    # Download Profile PDF
    re_path(r'^(?P<pk>\d+)/download-printout/$',
            views.generate_pdf, name='downloadpdf'),

    # search result url
    re_path(r'^search/$', views.searchQueryView.as_view(), name='searchresult'),
]


htmx_urlpatterns = [
    # delete share capital file
    re_path(r'^(?P<pk>\d+)/(?P<coopform_id>\d+)/delete-scfile/$',
            views.deletesharecapitalfile, name='deletesharecapitalfile'),

    # htmx search modal
    re_path(r'^htmx/search/$', views.htmxSearchView.as_view(),
            name='htmx_searchresult')
]

urlpatterns += htmx_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
