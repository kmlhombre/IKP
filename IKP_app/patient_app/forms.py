from django import forms

#
# from IKP_app.general_app.models import UnacceptedExaminations


class UnacceptedExaminationsForm(forms.Form):
    description = forms.CharField(max_length=50)
    file = forms.FileField()


class AppointmentsForm(forms.Form):
    appointment_type = forms.CharField(max_length=40)
    department = forms.CharField(max_length=100)
    appointment_date = forms.CharField(max_length=50)
    file = forms.FileField(required=False)
