from logging import PlaceHolder
from typing import ValuesView
from django import forms

class search_form(forms.Form):
    search_entry = forms.CharField(max_length=30, required=False, label="")
    search_entry.widget.attrs.update({"class" : "search"}, PlaceHolder = "Search Encyclopedia")


class NewPage(forms.Form):
    title = forms.CharField(max_length=30, label="Title",required=False)
    content = forms.CharField(widget = forms.Textarea(), required=False, label='')

class EditPage(forms.Form):
    content = forms.CharField(widget = forms.Textarea(attrs={"value" : "This is some text"}), required=False, label='')

