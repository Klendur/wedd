from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    HousingPreference,
    TransportInfo,
    ForumPost,
    ForumComment,
    Photo,
    PhotoGallery
)


class HousingForm(forms.ModelForm):
    class Meta:
        model = HousingPreference
        fields = ['housing_type', 'guests', 'notes']
        labels = {
            'housing_type': _('Majutuse valik'),
            'guests': _('Külaliste arv (sh sina)'),
            'notes': _('Lisainfo / märkused'),
        }
        widgets = {
            'housing_type': forms.Select(),
            'guests': forms.NumberInput(attrs={'min': 1, 'max': 20}),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': _('Valikuline...')
            }),
        }


class TransportForm(forms.ModelForm):
    class Meta:
        model = TransportInfo
        fields = ['arrival_method', 'free_seats', 'coming_from', 'notes']
        labels = {
            'arrival_method': _('Kuidas saabud?'),
            'free_seats': _('Vabu kohti autos'),
            'coming_from': _('Kust tuled?'),
            'notes': _('Lisainfo'),
        }
        widgets = {
            'arrival_method': forms.Select(),
            'free_seats': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'coming_from': forms.TextInput(attrs={
                'placeholder': _('nt Tallinn, Tartu...')
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': _('Valikuline...')
            }),
        }


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']
        labels = {
            'title': _('Pealkiri'),
            'content': _('Sõnum'),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': _('Postituse pealkiri...')
            }),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': _('Kirjuta siia...')
            }),
        }


class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']
        labels = {
            'content': _('Kommentaar'),
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': _('Lisa kommentaar...')
            }),
        }


class PhotoGalleryForm(forms.ModelForm):
    class Meta:
        model = PhotoGallery
        fields = ['caption']
        labels = {
            'caption': _('Galerii pealkiri / kirjeldus'),
        }
        widgets = {
            'caption': forms.TextInput(attrs={
                'placeholder': _('Nt: Suvepäevad 2026')
            }),
        }


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        labels = {
            'image': _('Foto'),
        }