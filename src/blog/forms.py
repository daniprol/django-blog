from django import forms

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
    trigram = forms.BooleanField(label="Use trigram search", required=False)
    # ALTERNATIVE:
    # trigram = forms.CharField(
    #     label="Use trigram search",
    #     widget=forms.CheckboxInput,
    #     required=False
    # )
