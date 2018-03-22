from django.shortcuts import redirect, render

from ...forms import ArtistForm
from ...models import Artist

__all__ = (
    'artist_add',
)


def artist_add(request):
    # context = {}
    if request.method == 'POST':
        # for sending a file to DB w/ form[ enctyoe = multupart/form-data ]
        # file is not in request.POST but in request.FILES
        # so, send request.FILES also to form
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artist:artist-list')
    else:
        form = ArtistForm()

    context = {
        'artist_form': form,
    }
    return render(request, 'artist/artist_add.html', context)

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

