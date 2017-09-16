from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from .models import Post
from .models import Thread

class PostForm(ModelForm):
    ''' This defines the form used to receive user input to create and enter text for a post in the forum.
            This form saves the data to the Post model.
            title is a field defining the title of the post.
            body is a field defining the body text of the post. '''
    class Meta:
        model = Post
        fields = ['title', 'body']
        labels = {
            'title': _('Post Title'),
            'body': _('Post Body')
        }

class ThreadForm(ModelForm):
    ''' This defines the form used to receive user input to create a thread in the forum.
            This form saves the data to the Thread model.
            title is a field defining the title of the thread. '''
    class Meta:
        model = Thread
        fields = ['title']
        labels = {
            'title': _('Thread / Post Title')
        }

class DeletePost (ModelForm):
    ''' This defines the form used to receive user confirmation to delete a post in the forum. '''
    class Meta:
        model = Post
        fields = []

class DeleteThread (ModelForm):
    ''' This defines the form used to receive user confirmation to delete a thread in the forum. '''
    class Meta:
        model = Thread
        fields = []