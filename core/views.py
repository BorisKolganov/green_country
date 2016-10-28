# coding=utf-8
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView

from core.forms import CallBackForm
from core.models import Page


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = {
            'pages': Page.objects.all()
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


class PageView(TemplateView):
    template_name = 'custom_page.html'

    def get_context_data(self, string, **kwargs):
        print string
        print self.request
        return {}
