from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from blogging.models import Post

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
    queryset = Post.objects.order_by('-published_date').exclude(published_date__isnull=True)
    template_name = 'blogging/list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blogging/detail.html'
