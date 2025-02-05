
from django import forms
from .models import SteganoFile

class SteganoFileForm(forms.ModelForm):
    class Meta:
        model = SteganoFile
        fields = ['original_file', 'file_type', 'auto_delete']