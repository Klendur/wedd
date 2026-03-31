from django import forms
from django.utils.translation import gettext_lazy as _
from .models import HousingPreference, TransportInfo, ForumPost, ForumComment, Photo


class HousingForm(forms.ModelForm):
    class Meta:
        model = HousingPreference
        fields = ['name', 'housing_type', 'guests', 'notes']
        labels = {
            'name': _('Sinu nimi'),
            'housing_type': _('Majutuse valik'),
            'guests': _('Külaliste arv (sh sina)'),
            'notes': _('Lisainfo / märkused'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Eesnimi Perekonnanimi')}),
            'guests': forms.NumberInput(attrs={'min': 1, 'max': 20}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': _('Valikuline...')}),
        }


class TransportForm(forms.ModelForm):
    class Meta:
        model = TransportInfo
        fields = ['name', 'arrival_method', 'free_seats', 'coming_from', 'notes']
        labels = {
            'name': _('Sinu nimi'),
            'arrival_method': _('Kuidas saabud?'),
            'free_seats': _('Vabu kohti autos'),
            'coming_from': _('Kust tuled?'),
            'notes': _('Lisainfo'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Eesnimi Perekonnanimi')}),
            'free_seats': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'coming_from': forms.TextInput(attrs={'placeholder': _('nt Tallinn, Tartu...')}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': _('Valikuline...')}),
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
            'title': forms.TextInput(attrs={'placeholder': _('Postitus pealkiri...')}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': _('Kirjuta siia...')}),
        }


class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']
        labels = {
            'content': _('Kommentaar'),
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': _('Lisa kommentaar...')}),
        }


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        labels = {
            'image': _('Foto'),
            'caption': _('Pealdis (valikuline)'),
        }
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': _('Kirjelda fotot...')}),
        }
