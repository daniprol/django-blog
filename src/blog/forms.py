from django import forms
from import_export.formats.base_formats import CSV, XLSX
from import_export.forms import ImportForm

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # ValidationError is raised if email is incorrect
    comments = forms.CharField(required=False, widget=forms.Textarea)
    # Overrides the default widget (<input type="text">) with a <textarea> element


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]  # by default all


class SearchForm(forms.Form):
    query = forms.CharField()


class CustomImportForm(ImportForm):
    def clean_import_file(self):
        data = self.cleaned_data["import_file"]
        file_extension = data.name.split(".")[-1].lower()
        if file_extension == "xlsx":
            self.cleaned_data["import_format"] = XLSX()
        elif file_extension == "csv":
            self.cleaned_data["import_format"] = CSV()
        else:
            raise ValueError("Unsupported file format. Only .xlsx and .csv are supported.")
        return data
