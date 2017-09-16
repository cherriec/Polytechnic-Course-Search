from django.contrib import admin

from .models import Forum
from .models import ForumList
from .models import Thread
from .models import Post

admin.site.register(Forum)
admin.site.register(ForumList)
admin.site.register(Thread)
admin.site.register(Post)