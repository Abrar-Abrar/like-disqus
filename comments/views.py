from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Comment
from .forms import AddComment
from posts.models import Post
from django import forms

# Create your views here.


@login_required
def comment_add(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = AddComment(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('single_post', post_id)
    else:
        form = AddComment()
    context = {
        'form': form
    }
    return render(request, 'comment/comment_add.html', context)


@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    if request.method == 'POST':
        form = AddComment(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('single_post', post.id)
    else:
        form = AddComment(instance=comment)
    context = {
        'form': form
    }
    return render(request, 'comment/comment_add.html', context)


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    if request.method == "POST":
        comment.delete()
        return redirect('single_post', post.id)
    context = {
        'comment': comment,
        'post_id': post.id
    }
    return render(request, 'comment/comment_delete.html', context)


@login_required
def comment_reaction(request):
    comment = get_object_or_404(Comment, pk=request.POST.get('comment_id'))
    post = comment.post
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        comment.likes_no = comment.likes.count()
        comment.dislikes.add(request.user)
        comment.dislikes_no = comment.dislikes.count()
        comment.save()
    else:
        comment.likes.add(request.user)
        comment.likes_no = comment.likes.count()
        comment.dislikes.remove(request.user)
        comment.dislikes_no = comment.dislikes.count()
        comment.save()
    return redirect('single_post', post.id)
