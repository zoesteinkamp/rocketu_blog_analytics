from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from blog.forms import EmailUserCreationForm
from blog.models import Post


def blog(request):
    return render(request, 'blog.html', {
        'posts': Post.objects.order_by('-created')
    })


@cache_page(60)
def post(request, pk):

    # Substitution of try/catch block to reroute users to 404 page
    post_obj = get_object_or_404(Post, pk=pk)

    return render(request, 'post.html', {
        'post': post_obj
    })


def filter_by_tags(request, tag_name):

    return render(request, 'filter_by_tags.html', {
        'posts': Post.objects.filter(tags__name=tag_name),

    })


def email_signup(request):
    pass


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })
