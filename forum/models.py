from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ForumList (models.Model):
    ''' This defines the ForumList model which represents a parent list of forums. 
        title is a string defining the title of the forum list.'''
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title

class Forum(models.Model):
    ''' This defines the Forum model which represents a forum. Every forum is grouped under a parent list of forums.
        title is a string defining the title of the forum.
        under_ForumList is a foreign key to a ForumList model, which is the parent list. '''
    title = models.CharField(max_length=60)
    under_ForumList = models.ForeignKey(ForumList)

    def __str__(self):
        return self.title

    def num_thread(self):
        return self.thread_set.count()

class Thread(models.Model):
    ''' This defines the Thread model, which represents a thread of posts in a forum.
        title is a string defining the title of the thread.
        author is a foreign key to the User model, which represents the user who created the thread.
        date_created defines the date and time the thread was created.
        under_forum is a foreign key to the Forum model, which contains a list of threads. '''
    title = models.CharField(max_length=60)
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    under_forum = models.ForeignKey(Forum)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        if self.post_set.count() == 0:
            return 0
        else:
            return self.post_set.count() -1

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("-date_created")[0]

class Post(models.Model):
    ''' This defines the Post model, which represents a post under a thread of posts in a forum.
        title is a string defining the title of the post.
        date_created and date_published define the date and time the post was created and published.
        author is a foreign key to a User model, which represents the user who created the post.
        under_thread is a foreign key to a Thread model, which contains a list of posts.
        body defines the body text of the post. '''
    title = models.CharField(max_length=60)
    date_created = models.DateTimeField(default=timezone.now)
    date_published = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User)
    under_thread = models.ForeignKey(Thread)
    body = models.TextField(max_length = 10000)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()


