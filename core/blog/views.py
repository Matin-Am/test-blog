from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic.base import TemplateView,RedirectView
from django.views.generic import ListView,DetailView,FormView
from .models import Post
from .forms import PostCreateForm
# Create your views here.

'''
Function base view to show templates 

def indexView(request):
    data = {"name":"ali"}
    return render(request,"index.html",context=data)
'''

class IndexView(TemplateView):
    template_name = "index.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["posts"] = Post.objects.all()
        return context
    
'''
Function base view for redirecting to a specific url 

def redirectToMaktabkhooneh(request):
    return redirect("blog:redirect-maktab")
'''

class RedirectToMaktab(RedirectView):
    url = "https://maktabkhooneh.org/"
    
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post,pk=kwargs["pk"])
        print(post)
        return super().get_redirect_url(*args,**kwargs)

class PostList(ListView):
    # model = Post
    # queryset = Post.objects.all()
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        posts = Post.objects.filter(status=True)
        return posts


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"



class PostCreateView(FormView):
    template_name = "blog/post_create.html"
    success_url = "/blog/post-list/"
    form_class = PostCreateForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
