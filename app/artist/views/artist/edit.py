from django.shortcuts import redirect, get_object_or_404, render

from ...forms import ArtistForm
from ...models import Artist

__all__ = (
    'artist_edit',
)


def artist_edit(request, artist_pk):
    """
    modify artist w/ artist_pk

    Form: ArtistForm
    Template: artist/artist-edit.html

    bound form: ArtistForm(instance=<artist instance>)

    update instance using ModelForm
        form = ArtistForm(request.POST, request.FILES, instance=<artist instance>)
        form.save()

    :param request:
    :param artist_pk:
    :return:
    """
    artist = get_object_or_404(Artist, pk=artist_pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('artist:artist-list')
    else:
        form = ArtistForm(instance=artist)
    context = {
        'artist_form': form,
    }

    return render(request, 'artist/artist_edit.html', context)
