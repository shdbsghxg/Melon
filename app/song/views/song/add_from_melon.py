from django.shortcuts import redirect
from ...models import Song

__all__ = (
    'song_add_from_melon',
)


def song_add_from_melon(request):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        Song.objects.update_or_create_from_melon(song_id)

        return redirect('song:song-list')
