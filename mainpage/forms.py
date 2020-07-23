from django import forms
from .models import UserReviews


class ReviewForm(forms.ModelForm):
    """Форма для створення відгуку користувача"""
    class Meta:
        model = UserReviews
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Write you\'r Article!',
                                          'class': 'col-md-7 form-control h-100 mt-3'})
        }
