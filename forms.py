from django import forms
from blogger.models import BloggerBlog

class BlogAdminForm(forms.ModelForm):
    # see the ticket here: http://code.djangoproject.com/ticket/9039 and the
    # solution form at SO: http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
    # to handle the case where we want a unique slug but we also want it to be
    # left just blank and not used

    class Meta:
        model = BloggerBlog

    def clean_slug(self):
        return self.cleaned_data['slug'] or None

    def clean_category(self):
        return self.cleaned_data['category'] or None


