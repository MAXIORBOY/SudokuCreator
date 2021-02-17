from django import forms
from django.forms import formset_factory

class NewForm(forms.Form):
    field = forms.CharField(label='', max_length=1, required=False, widget=forms.Textarea(attrs={'rows': 1,
                                                                                                 'cols': 1,
                                                                                                 'onkeyup': "this.value = this.value.replace(/[^1-9]+/g, '')",
                                                                                                 'style': 'resize: none;' 'text-align: center;' 'height: 42px;' 'width: 42px;' 
                                                                                                 'border-top-width: 0px;' 'border-right-width: 0px;' 'border-left-width: 0px;' 'border-bottom-width: 0px;'}))

NewFormSet = formset_factory(NewForm, max_num=81, extra=81)
