from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from blog.forms import ProfileForm, PostForm
from django.contrib.auth.decorators import login_required
from .models import Post, Profile
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


def user_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    posts = Post.objects.filter(author=user, status=
                                'published').order_by('-created_at')
    return render(request, 'blog/user_profile.html', {
        'profile_user': user,
        'posts': posts,
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blog/edit_profile.html', {'form': form})


# customize 403 forbidden.
def custom_permission_denied_view(request, exception=None):
    return render(request, 'blog/403.html', status=403)

class PostListView(generic.ListView):
    # which posts in what shapes display in posts list.
    queryset = Post.objects.order_by('-updated_at').filter(status = 'published')
    # model that we work on it.
    model = Post
    # template name
    template_name = 'blog/posts_list.html'
#    context_object_name = 'posts' 


class PostDetailView(generic.DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name_suffix = "_create_form"

    def get_success_url(self):
        return reverse_lazy('posts_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    # the model that work on it.
    model = Post
    # fields that can be edited.
    fields = ['title', 'content', ]
    # adjust the template name.
    template_name_suffix = "_update_form"

    # adjust redirect.
    def get_success_url(self):
        return reverse_lazy('posts_list')
    
    # check if the current user is the author of the post.
    def test_func(self):
        # get the post object that being edited
        post = self.get_object()
        # only if it was author he can edit.
        return self.request.user == post.author
    

    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    # the model that work on it.
    model = Post
    # adjust redirect.
    success_url = reverse_lazy('posts_list')

    # check if the current user is the author of the post.
    def test_func(self):
        # get the post object that being edited
        post = self.get_object()
        # only if it was author he can delete.       
        return self.request.user == post.author
    
 