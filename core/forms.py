from django import forms

from core.models import CallBack, EcoParticipant


class CallBackForm(forms.ModelForm):
    class Meta:
        model = CallBack
        fields = ('name', 'phone', 'raw_type', 'weight')

    raw_type = forms.CharField(required=False)
    weight = forms.IntegerField(required=False)


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = EcoParticipant
        fields = ('name', 'phone', 'email', 'org')
