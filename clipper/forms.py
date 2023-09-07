from django import forms
from .models import Clip
from tinymce.widgets import TinyMCE
from dal import autocomplete


class AddClipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(AddClipForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget = forms.TextInput(attrs={"placeholder": "Title"})
        self.fields["url"].widget = forms.URLInput(attrs={"placeholder": "URL"})
        self.fields["content"].widget = TinyMCE(attrs={"cols": 80, "rows": 40})

    class Meta:
        model = Clip
        fields = ("title", "url", "tags", "content")
        widgets = {"tags": autocomplete.TaggitSelect2("tagcomplete")}


class EditClipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(EditClipForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget = forms.TextInput(attrs={"placeholder": "Title"})
        self.fields["url"].widget = forms.URLInput(attrs={"placeholder": "URL"})
        self.fields["content"].widget = TinyMCE(attrs={"cols": 80, "rows": 40})

    class Meta:
        model = Clip
        fields = ("title", "url", "tags", "content")
        widgets = {"tags": autocomplete.TaggitSelect2("tagcomplete")}
