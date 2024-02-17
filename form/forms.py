from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from form.models import CoopForm
from django.utils.safestring import mark_safe


# Email domain validator
def validate_email_domain(value):
    if value.split("@")[-1].lower() != "edostate.gov.ng":
        raise ValidationError("Please provide your EDSG official email address")
    

# Cooperative Form
class createCoopForm(forms.ModelForm):
    nature_registration = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'flex inline-flex', 'cursor': 'pointer'}),
                                            choices=CoopForm.REGISTRATION_TYPE, initial='Without Limited Liability')
    have_bye_laws = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'flex inline-flex', 'cursor': 'pointer'}),
                                      choices=CoopForm.BYE_LAWS_CHOICES, initial='No')
    attach_bye_laws = forms.FileField(label='Attach Bye-Law', required=False)
    attach_first_minute = forms.FileField(
        label='Attach First Minute', required=True)
    attach_second_minute = forms.FileField(
        label='Attach Second Minute', required=True)
    # society_logo = forms.ImageField(label="Society's Logo", widget=forms.FileInput)


    class Meta:
        model = CoopForm
        fields = '__all__'
        widgets = {
            'first_purpose': forms.Textarea(attrs={'rows': 3}),
            'second_purpose': forms.Textarea(attrs={'rows': 3}),
            'third_purpose': forms.Textarea(attrs={'rows': 3}),
            'first_origin_meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'second_origin_meeting_date': forms.DateInput(attrs={'type': 'date'})
        }


# Attach Share Capital
class shareCapitalForm(createCoopForm):
    attach_share_capital = forms.FileField(
        label='Attach Share Capital',
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
        required=False
    )

    class Meta(createCoopForm.Meta):
        fields = createCoopForm.Meta.fields
        extra_fields = ('attach_share_capital')