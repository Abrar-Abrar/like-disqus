from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from comments.models import Comment
from .forms import AddPost

# Create your views here.


def index(request):
    posts = Post.objects.order_by('-created_at')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts
    }
    return render(request, 'post/posts.html', context)


def single_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post_liked = False
    else:
        post_liked = True

    comments = post.comments.order_by('-created_at')
    comment_count = comments.count
    context = {
        'post': post,
        'post_liked': post_liked,
        'comments': comments,
        'comment_count': comment_count,
    }

    return render(request, 'post/single_post.html', context)


@login_required
def post_add(request):
    if request.method == 'POST':
        form = AddPost(request.POST, request.FILES)
        print(request.POST.get('category'))
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = AddPost()
    context = {
        'form': form
    }
    return render(request, 'post/post_add.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = AddPost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddPost(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'post/post_edit.html', context)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('index')
    context = {
        'post': post
    }
    return render(request, 'post/post_delete.html', context)


@login_required
def post_reaction(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post_liked = False
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        post.dislikes.add(request.user)
        post_liked = False
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
        post_liked = True
    return redirect('single_post', post.id)


def comments_order_by(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "GET":
        if request.GET.get('ordered_byy') == "by_date":
            comments = post.comments.order_by('created_at')
        else:
            comments = post.comments.order_by('-likes_no')
            for comment in comments:
                print(comment.likes_no)

    else:
        comments = post.comments.order_by('-created_at')

    comment_count = comments.count
    paginator = Paginator(comments, 3)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'comments': comments,
        'comment_count': comment_count,
    }

    return render(request, 'post/single_post.html', context)
