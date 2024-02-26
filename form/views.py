
from wkhtmltopdf.views import PDFTemplateView
import contextlib
import logging

from django.conf import settings
from django.core import mail
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView, UpdateView
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from weasyprint import HTML, CSS
from operator import attrgetter
from .models import CoopForm, shareCapitalFiles
from .forms import *


# Index
def index(request):
    return HttpResponse(render(request, 'index.html'))


# How to Register
def howtoregister(request):
    return HttpResponse(render(request, 'howtoregister.html'))


# Login
class CoopLoginView(LoginView):
    redirect_authenticated_user = True
    redirect_field_name = 'next'
    template_name = 'login.html'
    fields = '__all__'

    def get_success_url(self):
        return self.get_redirect_url() or self.request.POST.get('previous_page') or self.get_default_redirect_url()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(
                self.request, f"You are logged in as {str(form.get_user()).upper()}")
            return self.form_valid(form)
        else:
            messages.error(
                self.request, 'Incorrect username or password. Note that both fields may be case-sensitive')
            return self.form_invalid(form)


# CSRF Failure View
def csrf_failure(request, reason=""):
    # context = { 'form': CoopLoginView().form_class }
    return render(request, template_name='403_csrf.html')


# Logout
class CoopLogoutView(LogoutView):
    template_name = 'logout-modal.html'
    redirect_field_name = 'next'

    def get_success_url(self):
        messages.success(self.request, 'You have been logged out')
        return self.request.META.get('HTTP_REFERER') or self.get_default_redirect_url()

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)


# Create New Form View
class RegisterView(CreateView):
    model = CoopForm
    form_class = shareCapitalForm
    context_object_name = 'form'
    template_name = 'register.html'

    def get_queryset(self):
        return CoopForm.objects.all()

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # check if "Limited Liability" is selected and share capital files are attached
        if self.request.POST.get('nature_registration') == 'Limited Liability':
            if not self.request.FILES.getlist('attach_share_capital'):
                messages.error(
                    self.request, 'Please attach share capital files or select a different option')
                return self.form_invalid(form)

        # check if "Yes" is selected and a copy of bye laws is attached
        if self.request.POST.get('have_bye_laws') == 'Yes':
            if not self.request.FILES.get('attach_bye_laws'):
                messages.error(
                    self.request, 'Please attach a copy of your bye laws or select a different option')
                return self.form_invalid(form)

        files = self.request.FILES.getlist('attach_share_capital')
        self.object = form.save(commit=False)
        self.object.save()

        if files:
            for f in files:
                instance = shareCapitalFiles.objects.create(
                    coopform=self.object, attach_share_capital=f)
                instance.save()
            messages.success(self.request, 'File(s) uploaded successfully')

        messages.success(self.request, 'Profile has been created')
        return super().form_valid(form)


# UpdateForm View
class updateFormView(LoginRequiredMixin, UpdateView):
    model = CoopForm
    form_class = shareCapitalForm
    context_object_name = 'obj'
    template_name = 'updateform.html'

    def get_object(self, queryset=None):
        return get_object_or_404(CoopForm, pk=self.kwargs['pk'])

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_share_capital_files(self):
        return shareCapitalFiles.objects.filter(coopform_id=self.kwargs.get('pk')).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(updateFormView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = shareCapitalForm(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['form'] = shareCapitalForm(instance=self.object)
        context['sharefiles'] = self.get_share_capital_files()
        return context

    def checks(self):
        # if "Without Limited Liability" is selected,
        # delete the associated share capital files
        if self.request.POST.get('nature_registration') == 'Without Limited Liability':
            if self.get_share_capital_files():
                self.get_share_capital_files().delete()
                messages.success(
                    self.request, 'Share Capital File(s) have been deleted')

        # if "No" is selected, delete the associated bye laws file
        if self.request.POST.get('have_bye_laws') == 'No':
            if self.object.attach_bye_laws:
                self.object.attach_bye_laws.delete()
                messages.success(
                    self.request, 'Bye Laws file has been deleted')

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = self.request.FILES.getlist('attach_share_capital')

        # perform some checks
        self.checks()

        # check if limited liability is selected and share capital files are attached
        if self.request.POST.get('nature_registration') == 'Limited Liability':
            if not self.get_share_capital_files() and not files:
                messages.error(
                    self.request, 'Please attach share capital files (5a) or choose a different option')
                return self.form_invalid(form)

        # check if yes is selected and a copy of bye laws is attached
        if self.request.POST.get('have_bye_laws') == 'Yes':
            if not self.object.attach_bye_laws and not self.request.FILES.get('attach_bye_laws'):
                messages.error(
                    self.request, 'Please attach a copy of your bye laws (9a) or choose a different option')
                return self.form_invalid(form)

        if not form.is_valid():
            return self.form_invalid(form)

        coopform = form.save(commit=False)
        coopform.save()

        if files:
            for f in files:
                instance = shareCapitalFiles.objects.create(
                    coopform=coopform, attach_share_capital=f)
                instance.save()
            messages.success(self.request, 'File(s) uploaded successfully')

        messages.success(self.request, 'Profile has been updated')
        return self.form_valid(form)


# Form Details View
class formDetailsView(DetailView):
    model = CoopForm
    form_class = shareCapitalForm
    context_object_name = 'form'

    def get_object(self):
        return get_object_or_404(CoopForm, pk=self.kwargs['pk'])

    def get_share_capital_files(self):
        return shareCapitalFiles.objects.filter(coopform_id=self.object.id).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(formDetailsView, self).get_context_data(**kwargs)
        context['tag'] = shareCapitalForm
        context['sharefiles'] = self.get_share_capital_files()
        return context


# All Cooperatives List View
class cooperativesListView(ListView):
    model = CoopForm
    context_object_name = 'coops'
    paginate_by = 4

    def get_template_names(self):
        if self.request.htmx:
            if self.request.GET.get("page"):
                return "htmx_cooperatives_list.html"
            return "searchresult.html"
        return "allcooperatives.html"

    def get_queryset(self):
        return CoopForm.objects.all().order_by('society_name')

    def get_context_data(self, **kwargs):
        context = super(cooperativesListView, self).get_context_data(**kwargs)
        context['total_cooperatives'] = CoopForm.objects.all().count()
        return context


# Search view
class searchQueryView(ListView):
    model = CoopForm
    template_name = 'searchresult.html'
    context_object_name = 'searchresults'
    paginate_by = 4

    # get search query object
    def get_queryset(self, query=None):
        query = self.request.GET.get("q")

        if query:
            queries = query.split(" ")
            queryset = []
            for q in queries:
                results = CoopForm.objects.filter(
                    Q(society_name__icontains=q) |
                    Q(society_category__icontains=q)
                ).distinct()

                queryset.extend(iter(results))
            return sorted(list(set(queryset)), key=attrgetter('society_name'), reverse=True)
        else:
            results = CoopForm.objects.none()
            return list(results)

    # context data
    def get_context_data(self, **kwargs):
        context = super(searchQueryView, self).get_context_data(**kwargs)
        context['query'] = str(self.request.GET.get("q"))
        context['count_query'] = len(self.get_queryset())

        return context


# htmx search modal
class htmxSearchView(ListView):
    model = CoopForm
    context_object_name = 'searchresults'
    paginate_by = 4

    def get_template_names(self):
        if self.request.GET.get("page"):
            return "htmx_load_more.html"
        return "htmx_search_results.html"

    # get search query object
    def get_queryset(self, query=None):
        query = self.request.GET.get("q")

        if not query:
            return []
        queries = query.split(" ")
        queryset = []
        for q in queries:
            results = CoopForm.objects.filter(
                Q(society_name__icontains=q) |
                Q(society_category__icontains=q)
            ).distinct()

            queryset.extend(iter(results))
        return sorted(list(set(queryset)), key=attrgetter('society_name'), reverse=True)

    # context data
    def get_context_data(self, **kwargs):
        context = super(htmxSearchView, self).get_context_data(**kwargs)
        context['count_query'] = len(self.get_queryset())
        context['query'] = str(self.request.GET.get("q"))

        return context


# Delete Share Capital file
def deletesharecapitalfile(request, pk, coopform_id):

    # get the template to render
    template = loader.get_template('snippets/sharecapitalfiles.html')

    # delete the file object
    shareCapitalFiles.objects.get(id=pk).delete()

    # retrieve the new updated files list
    sharefiles = shareCapitalFiles.objects.filter(coopform_id=coopform_id)

    # pass to context menu
    context = {
        'sharefiles': sharefiles,
    }

    return HttpResponse(template.render(context))


# Delete Form view
@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_form(request, pk):

    # get the return template to render
    template = loader.get_template('delete-success.html')

    # retrieve the form object
    coopform = get_object_or_404(CoopForm, id=pk)

    # save the society_name as context data
    society_name = coopform.society_name

    context = {'society_name': society_name}

    # delete the form object
    coopform.delete()

    return HttpResponse(template.render(context, request))


# test
def test(request):
    return HttpResponse(render(request, 'finish.html'))


# finish view
@permission_required('form.view_finish', login_url='/login/')
def finish(request, pk, template_name):

    # retrieve the form object
    coopform = get_object_or_404(CoopForm, id=pk)

    context = {
        'society_name': coopform.society_name,
        'category': coopform.society_category,
        'lga': coopform.society_lga_of_activities,
        'created': coopform.created,
        'form_url': request.build_absolute_uri(coopform.get_absolute_url())
    }

    return sendmail(request, context, template_name)


# Send a notification email on submission
def sendmail(request, context, template_name):

    subject = "NEW COOPERATIVE SOCIETY REGISTERED"

    text_content = 'This is to notify you that a new Cooperative Society has been registered on the website. \n\n'
    text_content += f'NAME: {context.get("society_name").upper()} COOPERATIVE SOCIETY\nCATEGORY: {context.get("category").upper()} \n'
    text_content += f'LGA: {context.get("lga").upper()}\nREGISTERED ON: {context.get("created")} \n\n'
    text_content += f'Visit here for more details: {context.get("form_url")}'

    html_content = loader.render_to_string(
        'notif-email.html',
        {
            'society_name': context.get('society_name'),
            'category': context.get('category'),
            'lga': context.get('lga'),
            'created': context.get('created'),
            'form_url': context.get('form_url'),
        }
    )

    from_email = f'Blades of Steel<{settings.EMAIL_HOST_USER}>'
    recipient_list = [settings.RECIPIENT_ADDRESS]

    msg = mail.EmailMultiAlternatives(
        subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()

    except Exception:
        # messages.error(request, f'{e}')
        pass

    # else:
    #     messages.success(request, 'Email was sent')

    # deactivate user after sending email
    u = User.objects.get(username=request.user.username)
    u.is_active = False
    u.save()

    # delete the session data
    with contextlib.suppress(KeyError):
        request.session.flush()

    template = loader.get_template(template_name)
    return HttpResponse(template.render({'society_name': context.get('society_name')}, request))


# Download as PDF view
def generate_pdf(request, pk):

    import pdfkit

    # # context objects
    coopform = get_object_or_404(CoopForm, id=pk)

    # # get the society's name as context data
    society_name = coopform.society_name.replace(' ', '_').lower()

    url = request.build_absolute_uri(coopform.get_printout_url())

    # # get the object's css stylesheets
    # pdf_stylesheets = [CSS(f"{settings.THEME_STATIC}css/dist/styles.css")]

    # # generate pdf
    # #pdf_file = HTML(url).write_pdf(stylesheets=pdf_stylesheets)
    pdf_file = HTML(url).write_pdf()

    # path_wkthmltopdf = b"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    # config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }

    #pdf_file = pdfkit.from_url(url, False, options=options)
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{society_name}_profile_printout.pdf"'

    return response


""" SESSION VIEWS """

# delete session


def delete_session(request):
    with contextlib.suppress(KeyError):
        request.session.flush()
        # for key in request.session.keys():
        #     del request.session[key]
        # del request.session['name']
        # del request.session['password']
    return HttpResponse("<h1>dataflair<br>Session Data cleared</h1>")
