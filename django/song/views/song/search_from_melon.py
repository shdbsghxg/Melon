import re
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

__all__ = (
    'song_search_from_melon',
)


def song_search_from_melon(request):
    keyword = request.GET.get('keyword')
    context = {}
    if keyword:
        url = 'https://www.melon.com/search/song/index.htm'
        params = {
            'q': keyword,
        }
        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')
        tr_list = soup.select('form#frm_defaultList table > tbody > tr')

        song_info_list = []
        for tr in tr_list:
            song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
            title_cont = tr.select_one('td:nth-of-type(3) a').get('href')
            title_temp = re.search(r"'SO','(.*?)'", title_cont).group(1)
            # title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
            artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(strip=True)
            album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

            song_info_list.append({
                'song_id': song_id,
                'title': title_temp,
                'artist': artist,
                'album': album,
            })
        context['song_info_list'] = song_info_list
        print(f'-----{song_id}')
        print(f'-----{type(title_cont)}')
        print(f'-----{title_cont}')
        print(f'-----{title_temp}')
    return render(request, 'song/song_search_from_melon.html', context)
