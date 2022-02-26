from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from blogging.forms import PostForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.models import User
from blogging.models import Post, Category

from rest_framework import viewsets
from rest_framework import permissions
from blogging.serializers import UserSerializer, PostSerializer, CategorySerializer

from django.contrib.syndication.views import Feed
from django.urls import reverse

from django.contrib.auth.decorators import login_required


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.created_date = timezone.now()
            post_instance.published_date = timezone.now()
            post_instance.author = request.user
            post_instance.save()
            return redirect("/")
    else:
        form = PostForm()
        return render(request, "blogging/add.html", {"form": form})


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


class PostListView(ListView):
    queryset = Post.objects.order_by("-published_date").exclude(
        published_date__isnull=True
    )
    template_name = "blogging/list.html"


class PostDetailView(DetailView):
    queryset = Post.objects.exclude(published_date__isnull=True)
    template_name = "blogging/detail.html"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class LatestPostsFeed(Feed):
    title = "Latest posts from my blog"
    link = "/postfeed/"
    description = "All of the latests posts to be published on my blog."

    def items(self):
        return Post.objects.order_by("-published_date")[:5]

    def item_title(self, item):
        return item.title

    def item_text(self, item):
        return item.text

    def item_author(self, item):
        return item.author

    def item_published_date(self, item):
        return item.published_date

    def item_link(self, item):
        return reverse("blog_detail", args=[item.pk])
