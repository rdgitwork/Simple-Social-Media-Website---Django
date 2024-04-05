from django.shortcuts import render
from posts.models import Post
from django.http import JsonResponse
from profiles.models import Profile
from .forms import PostForm




# Create your views here.

def post_list_and_create(request):
    form = PostForm(request.POST or None)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if the request is AJAX
        if form.is_valid():
            author =  Profile.objects.get(user=request.user)
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
            return JsonResponse({'success': True})  # Return a success response for AJAX requests
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)  # Return form errors if invalid
    else:
        context = {'form': form}
        return render(request, 'posts/main.html', context)

def load_post_data_view(request, num_posts):
    visible = 3
    upper = num_posts
    lower = upper - visible
    size = Post.objects.all().count()

    qs = Post.objects.all()
    data = []
    for obj in qs:
        item = {
            'id': obj.id,
            'title': obj.title,
            'body': obj.body,
            'liked': True if request.user in obj.liked.all() else False,
            'count': obj.like_count,
            'author': obj.author.user.username
        }
        data.append(item)
    return JsonResponse({'data': data[lower:upper],'size': size})

def like_unlike_post(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        pk = request.POST.get('pk')
        obj = Post.objects.get(pk=pk)
        if request.user in obj.liked.all():
            liked = False
            obj.liked.remove(request.user)
        else:
            liked = True
            obj.liked.add(request.user)
        return JsonResponse({'liked': liked, 'count': obj.like_count})

def hello_world_view(request):
    return JsonResponse({'text': 'Hello World x2'})
