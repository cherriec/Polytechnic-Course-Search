from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from .models import Forum
from .models import ForumList
from .models import Thread
from .models import Post
from .forms import PostForm
from .forms import ThreadForm
from .forms import DeletePost
from .forms import DeleteThread

def forumlist(request):
    ''' This function renders the html page to display all the ForumList objects. '''
    forumlist = ForumList.objects.all()
    return render(request, 'forum/ForumList.html', {"forumlist": forumlist})

def forumview(request, pk):
    ''' This function renders the html page to display all the Forum objects under the selected ForumList instance.'''
    forum = Forum.objects.filter(under_ForumList=pk).order_by("title")
    forum_name = ForumList.objects.get(pk=pk)
    return render(request, 'forum/ForumView.html', {"forum": forum, "pk":pk, "forum_name":forum_name.title})

def threadview(request, pk):
    ''' This function renders the html page to display all the Thread objects under the selected Forum instance. '''
    thread = Thread.objects.filter(under_forum=pk).order_by("date_created")
    thread_name = Forum.objects.get(pk=pk)
    return render(request, 'forum/ThreadView.html', {"thread": thread, "pk":pk, "forum_pk":thread_name.under_ForumList.pk,
                                                     "thread_name":thread_name.title} )

def postview(request, pk):
    ''' This function renders the html page to display all the Post objects under the selected Thread instance. '''
    post = Post.objects.filter(under_thread=pk).order_by("date_created")
    title = Thread.objects.get(pk=pk)
    back = Thread.objects.get(pk=pk).under_forum
    main = Forum.objects.get(pk=back.pk).under_ForumList
    thread_creator = Thread.objects.get(pk=pk).author
    return render(request, 'forum/PostView.html', {"post": post, "title": title.title, "pk": pk, 'thread_pk':back.pk, 'main':main.pk, 'thread_creator': thread_creator})


def replypost(request, pk):
    ''' This function renders the html page to allow a user to reply to a thread by rendering a PostForm form.
        After checking that the form is valid, a new Post object is created which is
        linked to the selected Thread instance. '''
    subject = Thread.objects.get(pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date_published = timezone.now()
            post.under_thread = Thread.objects.get(pk=pk)
            post.save()
            return redirect("postview", pk=pk)
    else:
        form = PostForm()
    return render(request, 'forum/ReplyPost.html', {'form': form, 'subject': subject.title, "post_pk":subject.pk})


def editpost(request, pk):
    ''' This function renders the html page to allow the user to edit their own post by rendering the PostForm form.
        After checking that the form is valid, it updates and saves the Post instance. '''
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date_published = timezone.now()
            post.under_thread = Thread.objects.get(pk=post.under_thread.pk)
            post.save()
            return redirect("postview", pk=post.under_thread.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/EditPost.html', {'form': form, 'post':post, 'subject':post.title, "back":post.under_thread.pk})


def addthread(request, pk):
    ''' This function renders the html page to allow the user to create a new thread in the selected forum by
        rendering the ThreadForm and PostForm forms.
        After checking that the forms are retrieved, the data retrieved is used to create new Thread and Post instances
        which are linked to the User instance. '''
    title = Forum.objects.get(pk=pk)
    if request.method == "POST":
        form = ThreadForm(request.POST)
        form1 = PostForm(request.POST)
        if form.is_valid() or form1.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.date_published = timezone.now()
            thread.under_forum = Forum.objects.get(pk=pk)
            thread.save()
            post = form1.save(commit=False)
            post.title = thread.title
            post.author = request.user
            post.date_published = timezone.now()
            post.under_thread = thread
            post.save()
            return redirect("postview", pk=thread.pk)
    else:
        form = ThreadForm()
        form1 = PostForm()
    return render(request, 'forum/AddThread.html', {'form': form, 'form1':form1, 'title':title.title, 'thread_pk':title.pk})

def delete_post(request, pk):
    ''' This function renders the html page to allow a user to delete their own post by rendering a DeletePost form.
        After checking that the form is valid, the Post instance is deleted. '''
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = DeletePost(request.POST)
        if form.is_valid():
            post.delete()
            return redirect("postview", pk=post.under_thread.pk)
    else:
        form = DeletePost()
    return render(request, 'forum/DeletePost.html', {'form': form, 'post':post, 'subject':post.title, "back":post.under_thread.pk})

def delete_thread(request, pk):
    ''' This function renders the html page to allow a user to delete their own thread by rendering a DeleteThread form.
        After checking that the form is valid, the Thread instance is deleted. '''
    thread = Thread.objects.get(pk=pk)
    if request.method == "POST":
        form = DeleteThread(request.POST)
        if form.is_valid():
            thread.delete()
            return redirect("threadview", pk=thread.under_forum.pk)
    else:
        form = DeleteThread()
    return render(request, 'forum/DeleteThread.html', {'form': form, 'thread':thread, 'subject':thread.title, "back":thread.under_forum.pk})