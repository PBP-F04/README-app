import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

#forms
from django.http import HttpResponseRedirect
from ForumDiskusi.forms import BookDiscussionForm
from django.urls import reverse

from UserProfile.models import Profile
from .models import BookDiscussion, DiscussionComment
from KatalogBuku.models import Book
from django.utils import timezone



@login_required(login_url='/login/')
def show_book_discussion(request, book_id):
    discussions = BookDiscussion.objects.filter(book_id=book_id) # nanti difilter berdasarkan book_id

    search_query = request.GET.get('search')  # Get the search query from the request

    if search_query:
        discussions = discussions.filter(Q(title__icontains=search_query))

    context = {
        'discussions': discussions,
        'user': request.user,
        'book_id': book_id,
        'book': Book.objects.get(id=book_id),
    }
    # print(discussions)
    return render(request, "discussion_forum.html", context)

from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q



@login_required(login_url='/login/')
def show_discussion_comment(request, discussion_id):
    comments = DiscussionComment.objects.filter(discussion_id = discussion_id)
    search_query = request.GET.get('search')

    if search_query:
        comments = comments.filter(Q(title__icontains=search_query))
    
    context = {
        'comments': comments,
        'user': request.user,
        'discussion_id': discussion_id,
        'discussion': BookDiscussion.objects.get(id=discussion_id),
    }
    return render(request, "discussion_comments.html", context)

@login_required(login_url='/login/')
def create_discussion(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = BookDiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.book = book
            discussion.user = Profile.objects.filter(user=request.user).first()
            discussion.save()
            return redirect('ForumDiskusi:show_book_discussion', book_id=book_id)
    else:
        form = BookDiscussionForm()

    context = {
        'form': form,
        'book_id': book_id,
    }
    return render(request, "create_discussion.html" , context)


from django.core import serializers

def get_comment_json(request, discussion_id):
    comment = DiscussionComment.objects.filter(discussion_id = discussion_id)
    return HttpResponse(serializers.serialize('json', comment))

@csrf_exempt
def add_comment_ajax(request, discussion_id):
    if request.method == 'POST':
        discussion = BookDiscussion.objects.filter(id = discussion_id).first()
        user = Profile.objects.filter(user=request.user).first()
        user_name = user.name
        title = request.POST['title']
        content = request.POST['content']
        upvotes = 0
        created_at_iso8601 = datetime.datetime.now().isoformat()
        created_at = created_at_iso8601.replace("T", " ")[:-7]
        # print(created_at)
        print(user_name)

        comment = DiscussionComment.objects.create(
            user=user,
            discussion = discussion,
            title=title,
            content=content,
            upvotes=upvotes,
            created_at=created_at,
        )
        comment.save()

        context = {
            'user_name': user_name,
        }
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()


