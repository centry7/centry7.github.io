import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import requests
from bs4 import BeautifulSoup
import socket
import requests.packages.urllib3.util.connection as urllib3_cn


urllib3_cn.allowed_gai_family = lambda: socket.AF_INET  # Uses IPv4 over IPv6

_url = sys.argv[0]
_handle = int(sys.argv[1])

header = 'authority=cdn.videocdn.click&sec-ch-ua=" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"&sec-ch-ua-mobile=?0&user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36&sec-ch-ua-platform="Windows"&accept=*/*&origin=https://widevine.licenses4.me&sec-fetch-site=cross-site&sec-fetch-mode=cors&sec-fetch-dest=empty&referer=https://widevine.licenses4.me/&accept-language=en-US,en;q=0.9'

streams = {'Live TV': {'DaddyLive': []}}


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    return streams.keys()


def get_streams(category, provider):
    if provider == 'DaddyLive' and len(streams[category]['DaddyLive']) == 0:
        print('Scraping...')
        soup = BeautifulSoup(
            requests.get('https://daddylive.click/24-hours-channels.php').content, 'html.parser')
        channels_list = soup.find("div", {'class': 'grid-container'}).find_all('div', 'grid-item')
        for channel in channels_list:
            streams[category]['DaddyLive'].append({'name': channel.find('strong').text, 'video': f"https://cdn.videocdn.click/cdn/premium{int(''.join(filter(str.isdigit, channel.find('a', href=True)['href'])))}/chunks.m3u8|{header}"})
    return streams[category][provider]


def get_providers(category):
    return streams[category].keys()


def list_categories():
    xbmcplugin.setPluginCategory(_handle, 'My Video Collection')
    xbmcplugin.setContent(_handle, 'videos')
    categories = get_categories()
    for category in categories:
        list_item = xbmcgui.ListItem(label=category)
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        url = get_url(action='list_providers', category=category)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_streams(category, provider):
    xbmcplugin.setPluginCategory(_handle, provider)
    xbmcplugin.setContent(_handle, 'videos')
    videos = get_streams(category, provider)
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'])
        list_item.setInfo('video', {'title': video['name'],
                                    'mediatype': 'video'})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=video['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_providers(category):
    xbmcplugin.setPluginCategory(_handle, category)
    xbmcplugin.setContent(_handle, 'videos')
    providers = get_providers(category)
    for provider in providers:
        list_item = xbmcgui.ListItem(label=provider)
        list_item.setInfo('video', {'title': provider,
                                    'mediatype': 'video'})
        url = get_url(action='list_streams', category=category, provider=provider)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'list_streams':
            list_streams(params['category'], params['provider'])
        elif params['action'] == 'list_providers':
            list_providers(params['category'])
        elif params['action'] == 'play':
            play_video(params['video'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])
