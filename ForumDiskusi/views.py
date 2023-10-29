import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#forms
from django.http import HttpResponseRedirect
from ForumDiskusi.forms import BookDiscussionForm
from django.urls import reverse

from UserProfile.models import Profile
from .models import BookDiscussion, DiscussionComment
from KatalogBuku.models import Book



@login_required(login_url='/login/')
def show_book_discussion(request, book_id):
    discussions = BookDiscussion.objects.filter(id = book_id) # nanti difilter berdasarkan book_id
    context = {
        'discussions': discussions,
        'user': request.user
    }
    return render(request, "discussion_forum.html", context)

from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login/')
def show_discussion_comment(request, discussion_id):
    comments = DiscussionComment.objects.filter(id = discussion_id)
    context = {
        'comments': comments,
        'user': request.user
    }
    return render(request, "discussion_comments.html", context)

def create_discussion(request):
    form = BookDiscussionForm(request.POST or None)

    if form.is_valid() and request.method == 'POST' :
        form.save()
        return HttpResponseRedirect(reverse('ForumDiskusi:show_book_discussion'))
    
    context = { 'form': form }
    return render(request, "create_discussion.html", context)



@csrf_exempt
def add_discussion_ajax(request):
    if request.method == 'POST':
        profile = Profile.object.filter(user=request.user).first()
        user = profile
        title = request.POST['title']
        content = request.POST['content']
        upvotes = 0
        created_at = datetime.now()

        discussion = BookDiscussion.objects.create(
            user=user,
            title=title,
            content=content,
            upvotes=upvotes,
            created_at=created_at,
        )
        discussion.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
def add_comment_ajax(request):
    if request.method == 'POST':
        profile = Profile.object.filter(user=request.user).first()
        user = profile
        title = request.POST['title']
        content = request.POST['content']
        upvotes = 0
        created_at = datetime.now()

        comment = DiscussionComment.objects.create(
            user=user,
            title=title,
            content=content,
            upvotes=upvotes,
            created_at=created_at,
        )
        comment.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()


