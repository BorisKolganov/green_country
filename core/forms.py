from django import forms

from core.models import CallBack


class CallBackForm(forms.ModelForm):
    class Meta:
        model = CallBack
        fields = ('name', 'phone')
