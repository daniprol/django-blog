from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # ValidationError is raised if email is incorrect
    comments = forms.CharField(required=False, widget=forms.Textarea)
    # Overrides the default widget (<input type="text">) with a <textarea> element
