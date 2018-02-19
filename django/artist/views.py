from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Artist


def artist_list(request):
    # show artist ist ad ul > li
    # use template 'artist/artist_list.html'
    # 'artists' for context to be delivered
    artists = Artist.objects.all()
    context = {
        'artists': artists,
    }
    return render(request, 'artist/artist_list.html', context)


def artist_add(request):
    # context = {}
    if request.method == 'POST':
        name = request.POST['name']
        Artist.objects.create(
            name=name
        )
        return redirect('artist:artist-list')
    else:
        return render(request, 'artist/artist_add.html')

    #     name = request.POST['name']
    #     real_name = request.POST['real_name']
    #     nationality = request.POST['nationality']
    #     birth_date = request.POST['birth_date']
    #     constellation = request.POST['constellation']
    #     blood_type = request.POST['blood_type']
    #     intro = request.POST['intro']
    #
    #     if name and real_name and nationality and birth_date and \
    #             constellation and blood_type and intro:
    #         post = Artist.objects.create(
    #             author=request.user,
    #             name=name,
    #             real_name=real_name,
    #             nationality=nationality,
    #             birth_date=birth_date,
    #             constellation=constellation,
    #             blood_type=blood_type,
    #             intro=intro,
    #         )
    #         return redirect('artist-list', pk=post.pk)
    #     context['form_error'] = 'input correctly'
    # return render(request, 'artist/artist_add.html', context)
