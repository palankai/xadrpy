from django.contrib.comments.forms import CommentForm
from django import forms
from models import Feedback
from django.utils import translation

class FeedbackForm(CommentForm):
    title = forms.CharField(max_length=300, required=False)
    site_name = forms.CharField(max_length=300, required=False)

    def get_comment_model(self):
        return Feedback

    def get_comment_create_data(self):
        data = super(FeedbackForm, self).get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        data['language_code'] = translation.get_language()
        return data

class TrackbackForm(forms.Form):
    url = forms.URLField()
    title = forms.CharField(required=False)
    blog_name = forms.CharField(required=False)
    excerpt = forms.CharField(required=False)
