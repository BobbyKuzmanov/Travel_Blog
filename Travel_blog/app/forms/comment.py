from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control rounded-2',
                'rows': '3',
                'placeholder': 'Write your comment here...',
                'style': 'resize: none; max-height: 100px;'
            }
        )
    )
