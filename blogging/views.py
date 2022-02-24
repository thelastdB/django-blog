from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from blogging.forms import PostForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from blogging.models import Post


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
