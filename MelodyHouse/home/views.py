
from django.shortcuts import redirect, render, HttpResponse
from profile_app.models import Post
from upload_app.models import Album,Song



def homeView(request):
    if request.user.is_authenticated:
        return redirect('profile_app:profile-view')
    else:
        user = request.user
        albums = Album.objects.all()
        side_albums = albums.all().order_by('-date_time')[:8]
        side_albums = list(side_albums)

        post = Post.objects.all()
        post = post.all().order_by("-date_time")

        context = {
            'side_albums': side_albums,
            'post': post,
            'user': user
        }
        return render(request, 'home/HomePage.html', context)
