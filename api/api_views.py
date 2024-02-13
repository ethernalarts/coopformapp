
from operator import attrgetter
from django.template import loader
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from form.models import CoopForm, shareCapitalFiles
from .serializers import *

from rest_framework import generics, permissions, response, status, pagination
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer


# Pagination for ListAPIView
class AllCooperativesListPagination(pagination.PageNumberPagination):
    page_size = 4


# All Cooperatives API View
class AllCooperativesList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api-cooperativeslist.html'
    serializer_class = CooperativesListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = AllCooperativesListPagination

    def get_queryset(self):
        return CoopForm.objects.all().order_by('id')

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        page_size = self.pagination_class.page_size
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        is_paginated = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page_obj, many=True)
        data = serializer.data

        context = {
            'coops': data,
            'paginator': paginator,
            'page_obj': page_obj,
            'is_paginated': is_paginated,
            'total_cooperatives': paginator.count
        }

        return self.get_paginated_response(context)

    def get_paginated_response(self, context):
        return response.Response(context)


# API Search Results View
class APISearchCooperative(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api-searchresult.html'
    serializer_class = CooperativesListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = AllCooperativesListPagination

    # get search query object
    def get_queryset(self, query=None):
        query = self.request.GET.get(
            "q", None) if self.request.GET.get("q") else ''
        queryset = []
        queries = query.split(" ")
        for q in queries:
            results = CoopForm.objects.filter(
                Q(society_name__icontains=q) |
                Q(society_category__icontains=q) 
            ).distinct()

            queryset.extend(iter(results))
        return sorted(list(set(queryset)), key=attrgetter('society_name'), reverse=True)

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        page_size = self.pagination_class.page_size
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        is_paginated = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page_obj, many=True)
        searchresult = serializer.data

        context = {
            'paginator': paginator,
            'page_obj': page_obj,
            'is_paginated': is_paginated,
            'searchresult': searchresult,
            'query': str(self.request.GET.get("q")),
            'count_query': paginator.count,
        }

        return response.Response(context)


# Register Cooperative API View
class RegisterCooperative(LoginRequiredMixin, generics.CreateAPIView):
    login_url = 'api-login'
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api-register.html'
    serializer_class = RegisterCooperativeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post']

    def get(self, request, serializer_errors=None, *args, **kwargs):
        serializer = self.get_serializer()

        context = {
            'tag': serializer,
            'defaultdate': str(datetime.date.today()),
            'errors': serializer_errors,
        }
        
        return response.Response(context)

    def post(self, request, *args, **kwargs):
        # check if "Limited Liability" is selected and share capital files are attached
        if self.request.data.get('nature_registration') == 'Limited Liability':
            if not self.request.FILES.getlist('attach_share_capital'):
                messages.error(
                    self.request, 'Please attach share capital files or select a different option')
                return response.Response(self.get())

        # check if "Have Bye Laws - Yes" is selected and a copy of bye laws is attached
        if self.request.data.get('have_bye_laws') == 'Yes':
            if not self.request.FILES.get('attach_bye_laws'):
                messages.error(
                    self.request, 'Please attach a copy of your bye laws or select a different option')
                return response.Response(self.get())

        # serialize, create and save the object
        try:
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
        except Exception:
            messages.error(
                self.request, 'This form has errors. Please scroll down to address them')
            return response.Response(self.get(serializer_errors=serializer.errors))
        else:
            return self.create(serializer)

    def create(self, serializer):
        self.perform_create(serializer)

        # upload share capital files
        if self.request.FILES:
            sharefiles = self.request.FILES.getlist('attach_share_capital')
            if sharefiles:
                for file in sharefiles:
                    file_data = {"coopform": serializer.data['id'],
                                 "attach_share_capital": file}
                    file_serializer = ShareCapitalSerializer(data=file_data)
                    file_serializer.is_valid(raise_exception=True)
                    file_serializer.save()
                messages.success(self.request, 'File(s) uploaded successfully')

        messages.success(self.request, 'Profile has been created')
        instance = get_object_or_404(CoopForm, pk=serializer.data['id'])
        return redirect('api-retrievecooperative', pk=instance.pk)


# Update Cooperative API View
class UpdateCooperative(LoginRequiredMixin, generics.UpdateAPIView):
    login_url = 'api-login'
    template_name = 'api-updateform.html'
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateCooperativeSerializer
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_object(self):
        return get_object_or_404(CoopForm, pk=self.kwargs['pk'])

    def get(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        society_category = serializer['society_category'].choices

        sharefiles = shareCapitalFiles.objects.filter(
            coopform_id=instance.pk)
        sharefiles_serializer = ShareCapitalSerializer(sharefiles, many=True)
        sharefilesdata = sharefiles_serializer.data
        
        context = {
            'form': data,
            'obj': instance,
            'sharefiles': sharefilesdata,
            'coopform_id': instance.pk,
            'tag': serializer,
            'LGA': data.get('LGA'),
            'BYE_LAWS_CHOICES': data.get('BYE_LAWS_CHOICES'),
            #'categories': data.get('SOCIETY_CATEGORY'),
            'categories': list(society_category.items()),
            'REGISTRATION': data.get('REGISTRATION_TYPE'),
        }

        return response.Response(context)

    def files_to_exclude(self, data, serializer):
        # if these fields are empty in request.POST, but not empty in the database, 
        # add to exclusion list
        files = ['society_logo', 'attach_first_minute',
                 'attach_second_minute', 'attach_bye_laws']
        
        # add to exclude_fields
        for file in files:
            if file in data and not self.request.data.get(file):
                serializer.exclude_fields([file])        
    
    def upload_share_capital_files(self, instance):
        # upload share capital files
        if self.request.FILES:
            sharefiles = self.request.FILES.getlist('attach_share_capital')
            if sharefiles:
                for file in sharefiles:
                    file_data = {"coopform": instance.pk,
                                 "attach_share_capital": file}
                    file_serializer = ShareCapitalSerializer(data=file_data)
                    file_serializer.is_valid(raise_exception=True)
                    file_serializer.save()
                messages.success(self.request, 'File(s) uploaded successfully')

    def checks(self, instance):
        # if "Without Limited Liability" is selected, 
        # delete the associated share capital files
        if self.request.data.get('nature_registration') == 'Without Limited Liability':
            sharefiles = shareCapitalFiles.objects.filter(
                coopform_id=instance.pk)
            if sharefiles:
                sharefiles.delete()
                messages.success(
                    self.request, 'Share Capital File(s) have been deleted')
        
        # if "No" is selected, delete the associated bye laws file
        if self.request.data.get('have_bye_laws') == 'No':
            if instance.attach_bye_laws:
                instance.attach_bye_laws.delete()
                messages.success(
                    self.request, 'Bye Laws file has been deleted')
        
        # if society's logo checkbox is selected, delete the society logo
        if 'delete_society_logo' in self.request.POST:
            instance.society_logo.delete()
            messages.success(
                self.request, 'Society Logo has been deleted')
    
    def post(self, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        data = self.get_serializer(instance).data

        serializer = self.get_serializer(
            instance,
            data=self.request.data,
            partial=partial
        )

        # check if "Limited Liability" is selected and share capital files are attached
        if self.request.data.get('nature_registration') == 'Limited Liability':
            if not data['attach_share_capital'] and not self.request.FILES.getlist('attach_share_capital'):
                messages.error(
                    self.request, 'Please attach share capital files (5a) or choose a different option')
                return self.get(self.request, pk=instance.pk)

        # check if "Yes" is selected and a copy of bye laws is attached
        if self.request.data.get('have_bye_laws') == 'Yes':
            if not instance.attach_bye_laws and not self.request.FILES.get('attach_bye_laws'):
                messages.error(
                    self.request, 'Please attach a copy of your bye laws (9a) or choose a different option')
                return self.get(self.request, pk=instance.pk)
        
        # fields to exclude if they are empty in request.POST, but not empty in the database
        self.files_to_exclude(data, serializer)
        
        # upload share capital files
        self.upload_share_capital_files(instance)
        
        # perform some checks
        self.checks(instance)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            messages.error(self.request, f'{e}')
            return self.get(self.request, pk=instance.pk)
        else:
            self.perform_update(serializer)
            messages.success(self.request, 'Profile has been updated')
            return redirect('api-retrievecooperative', pk=instance.pk)


# Delete Share Capital file
@api_view(('DELETE', 'GET', ))
def deletesharecapitalfile(request, pk, coopform_id):

    # get the template to render
    template = loader.get_template('snippets/api-sharecapitalfiles.html')

    # delete the file object
    shareCapitalFiles.objects.get(id=pk).delete()

    # retrieve the new updated files list
    sharefiles = shareCapitalFiles.objects.filter(coopform_id=coopform_id)

    # serialize the list
    sharefiles_serializer = ShareCapitalSerializer(sharefiles, many=True)
    files = sharefiles_serializer.data

    # pass to context menu
    context = {
        'sharefiles': files,
        'coopform_id': coopform_id,
    }

    return HttpResponse(template.render(context))


# Retrieve Cooperative API View
class RetrieveCooperative(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api-profiledetails.html'
    serializer_class = RetrieveCooperativeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get',]

    def get_object(self):
        return get_object_or_404(CoopForm, pk=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        sharefiles = shareCapitalFiles.objects.filter(
            coopform_id=self.kwargs.get('pk'))
        sharefiles_serializer = ShareCapitalSerializer(sharefiles, many=True)
        sharefilesdata = sharefiles_serializer.data

        context = {
            'form': data, 
            'tag': serializer,
            'sharefiles': sharefilesdata, 
        }

        return response.Response(context)


# Delete API View
class DeleteCooperative(generics.DestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api-deletesuccess.html'
    serializer_class = DeleteCooperativeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post',]

    def get_object(self):
        try:
            return CoopForm.objects.get(pk=self.kwargs['pk'])
        except CoopForm.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        societyname = self.get_serializer(instance).data.get('society_name')
        context = {'society_name': societyname}
        self.perform_destroy(instance)
        return response.Response(context)


# test
def test(request):
    return HttpResponse(render(request, 'api-finish.html'))
