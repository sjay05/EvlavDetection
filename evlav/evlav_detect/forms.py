from django import forms

class UploadFileForm(forms.Form):
  file1 = forms.FileField()
  file2 = forms.FileField()
