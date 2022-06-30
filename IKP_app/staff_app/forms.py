from django import forms

class ExaminationsForm(forms.Form):
    description = forms.CharField(max_length=50)
    patient_pesel = forms.CharField(max_length=50)
    file = forms.FileField()
