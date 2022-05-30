from django import forms

#
# from IKP_app.general_app.models import UnacceptedExaminations


class UnacceptedExaminationsForm(forms.Form):
    description = forms.CharField(max_length=50)
    file = forms.FileField()

