# coding=utf-8
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import JsonResponse, HttpResponseNotFound, Http404
from django.views.generic import TemplateView, FormView

from core.forms import CallBackForm, ParticipantForm
from core.models import  MainRaw, Advantage, Clients, RawDetails, MainPage, EcoProject, EcoPhoto


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = {
            'page': MainPage.objects.all().first(),
            'eco': EcoProject.objects.first(),
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
        main_raw = MainRaw.objects.filter(slug=slug).first()
        if not main_raw:
            raise Http404()

        if main_raw.archive:
            context = {
                'page': MainPage.objects.all().first(),
                'text': main_raw.details_text,
                'header': main_raw.details_header,
                'button_text': u'Заказать уничтожение документов'
            }
        else:
            context = {
                'page': MainPage.objects.all().first(),
                'text': main_raw.details_text,
                'header': main_raw.details_header,
                'raw_details': main_raw.rawdetails_set.all(),
                'button_text': u'Заказать вывоз прямо сейчас'
            }
        return context


class EcoView(TemplateView):
    template_name = 'eco-project.html'

    def get_context_data(self, **kwargs):
        return {
            'eco': EcoProject.objects.first(),
            'page': MainPage.objects.first(),
            'photos': EcoPhoto.objects.all()
        }


class EcoFormView(FormView):
    form_class = ParticipantForm
    template_name = 'eco-project.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({'status': 'ok', 'message': u'Мы приняли вашу заявку'})

    def form_invalid(self, form):
        errors = {k: v[0] for k, v in form.errors.items()}
        return JsonResponse({
            "status": 'not ok',
            "errors": errors,
        })