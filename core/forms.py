from django import forms

from core.models import CallBack


class CallBackForm(forms.ModelForm):
    class Meta:
        model = CallBack
        fields = ('name', 'phone', 'raw_type', 'weight')

    raw_type = forms.CharField(required=False)
    weight = forms.IntegerField(required=False)
