# coding=utf-8
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import JsonResponse, HttpResponseNotFound, Http404
from django.views.generic import TemplateView, FormView

from core.forms import CallBackForm
from core.models import  MainRaw, Advantage, Clients, RawDetails, MainPage


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = {
            'page': MainPage.objects.all().first(),
            'raw': MainRaw.objects.all(),
            'advantage': Advantage.objects.all(),
            'clients': Clients.objects.all()
        }
        return context


class CallBackView(FormView):
    http_method_names = ['post']
    form_class = CallBackForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({'status': 'ok', 'message': u'Мы скоро Вам перезвоним'})

    def form_invalid(self, form):
        errors = {k: v[0] for k, v in form.errors.items()}
        return JsonResponse({
            "status": 'not ok',
            "errors": errors,
        })


class RawView(TemplateView):
    template_name = 'raw_page.html'

    def get_context_data(self, slug, **kwargs):
        raw_details = RawDetails.objects.filter(main_raw__slug=slug)
        if not raw_details:
            raise Http404()
        main_raw = MainRaw.objects.filter(slug=slug).first()
        context = {
            'page': MainPage.objects.all().first(),
            'raw_details': raw_details,
            'header': main_raw.details_header,
            'text': main_raw.text
        }
        print context
        return context