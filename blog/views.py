from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    visits = request.session.get('visits')
    posts = Post.objects.filter(
        published_date__isnull=False).order_by(
        "-created_date")
    if visits:
        last_visit_time = request.session.get('last_visit_time')
        last_visit = datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")
        if(datetime.now() - last_visit).seconds > 3600:
            visits += 1
            request.session['visits'] = visits
            request.session['last_visit_time'] = str(datetime.now())
    else:
        request.session['visits'] = 1
        request.session['last_visit_time'] = str(datetime.now())

    context_dict = {'posts': posts, 'visits': visits}

    return render(request, 'blog/post_list.html', context_dict)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    if post:
        comments = Comment.objects.filter(post=post)
        form = CommentForm()
        context_dict = {'post': post, 'comments': comments, 'form': form}
    else:
        context_dict = {'post': post}
    return render(request, 'blog/post_detail.html', context_dict)


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', post_slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', post_slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True).order_by(
        'created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    post.publish()
    return redirect('blog.views.post_detail', post_slug=post.slug)


@login_required
def post_remove(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    post.delete()
    return redirect('blog.views.post_list')


def add_comment(request, slug):
    if request.method == 'POST':
        author = request.POST['author']

        if not author:
            author = 'Anonymous'

        comment = Comment(post=get_object_or_404(Post, slug=slug))
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.save()
        else:
            print(form.errors) # print to the console.
    return redirect('blog.views.post_detail', post_slug=slug)
