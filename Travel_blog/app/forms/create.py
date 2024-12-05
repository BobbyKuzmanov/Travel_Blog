from django import forms
from django.core.exceptions import ValidationError
from Travel_blog.app.models import Destination
import re


class DestinationForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('Title is required.')
        if len(title) < 3:
            raise ValidationError('Title must be at least 5 characters long.')
        if len(title) > 100:
            raise ValidationError('Title cannot exceed 100 characters.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError('Description is required.')
        if len(description) < 10:
            raise ValidationError('Description must be at least 10 characters long.')
        return description

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise ValidationError('Country is required.')
        if not re.match(r'^[A-Za-z\s\-]+$', country):
            raise ValidationError('Country name can only contain letters, spaces, and hyphens.')
        return country

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if not year:
            raise ValidationError('Year is required.')
        if year < 1900 or year > 2100:
            raise ValidationError('Please enter a valid year between 1900 and 2100.')
        return year

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image and not self.instance.pk:  # Required only for new destinations
            raise ValidationError('Image is required.')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image file too large. Size should not exceed 5 MB.')
            if not image.content_type.startswith('image/'):
                raise ValidationError('File type not supported. Please upload an image file.')
        return image

    class Meta:
        model = Destination
        fields = ('title', 'description', 'country', 'year', 'category', 'image')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter title (3-100 characters)',
                    'minlength': '3',
                    'maxlength': '100',
                    'required': True,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description (minimum 10 characters)',
                    'minlength': '10',
                    'required': True,
                }
            ),
            'country': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter country name',
                    'pattern': '^[A-Za-z\\s\\-]+$',
                    'required': True,
                }
            ),
            'year': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1900',
                    'max': '2100',
                    'required': True,
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'form-control-file',
                    'accept': 'image/*',
                    'required': True,
                }
            ),
        }
