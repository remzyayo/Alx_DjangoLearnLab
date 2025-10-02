from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, UserUpdateForm, PostForm, CommentForm
from .models import Post, Comment 
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    posts = Post.objects.order_by('-published_date')[:10]
    return render(request, 'blog/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileForm(instance=user.profile)

    return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form': p_form})


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'  # blog/templates/posts/post_list.html
    context_object_name = 'posts'
    paginate_by = 10  # optional: paginate the list

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

# Tagging and Search

class SearchResultsView(ListView):
    model = Post
    template_name = 'posts/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)   # works with django-taggit
            ).distinct().order_by('-published_date')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class PostsByTagView(ListView):
    model = Post
    template_name = 'posts/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags_name_iexact=tag_name).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context

