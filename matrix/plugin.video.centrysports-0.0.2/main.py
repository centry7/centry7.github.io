import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import requests
from bs4 import BeautifulSoup
import socket
import re
import requests.packages.urllib3.util.connection as urllib3_cn


urllib3_cn.allowed_gai_family = lambda: socket.AF_INET  # Uses IPv4 over IPv6

_url = sys.argv[0]
_handle = int(sys.argv[1])

streams = {'Live TV': {'DaddyLive': [], 'USTVGO': []}}

'''
Weak_Spell http://weakstreams.com

Once you land on stream page, search for this iframe in iframe:
<iframe class="iframe-player" src="http://weakstreams.com/weakstreams/9830214" allowfullscreen="" __idm_frm__="52990" scrolling="no"></iframe>
Go to http://weakstreams.com/weakstreams/9830214 and search for gethlsurl function.
You will get a url like this http://weakstreams.com/gethls?idgstream=WE83VjYzQ2t3OU91UmYvVXdOR2tuQT09OjqNsjRCbcOZD4ULQJda7Muj.
Then you'll get m3u8 url.

givemeredditstream http://givemenbastreams.com

Get php link from iframe which looks like this http://givemenbastreams.com/nba.php?g=bucks.
Then search for m3u8 link from here.

CyclingStreams http://thecyclingentertainment.com (VPN)
Just search for m3u8.

topstreamer https://topstreams.info (VPN)
Just search for m3u8

hockeynews http://hockeyweb.site
Just search for m3u8. m3u8 showing 403 error, try using headers.

MediaStreams https://techoreels.com
Search for var servs and add n1.m3u8. m3u8 showing 403 error, try using headers.

Azulito http://jmutech.xyz
Just search for m3u8. m3u8 showing 403 error, try using headers.

SportsCentral http://sportsnest.co
Just search for m3u8. m3u8 showing 403 error, try using headers.

mntvlive13 http://uhdstreams.club
Just search for php.
Go to php site and search for m3u8. m3u8 showing 403 error, try using headers.


Couldnt, scrape 1stream, thebaldstreamer, rainostream(Did not attempt).
'''


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    return streams.keys()


def get_streams(category, provider):
    if provider == 'DaddyLive':
        header = 'authority=cdn.videocdn.click&sec-ch-ua=" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"&sec-ch-ua-mobile=?0&user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36&sec-ch-ua-platform="Windows"&accept=*/*&origin=https://widevine.licenses4.me&sec-fetch-site=cross-site&sec-fetch-mode=cors&sec-fetch-dest=empty&referer=https://widevine.licenses4.me/&accept-language=en-US,en;q=0.9'
        soup = BeautifulSoup(
            requests.get('https://daddylive.click/24-hours-channels.php').content, 'html.parser')
        channels_list = soup.find("div", {'class': 'grid-container'}).find_all('div', 'grid-item')
        for channel in channels_list:
            try:
                streams[category][provider].append({'name': channel.find('strong').text, 'video': f"https://cdn.videocdn.click/cdn/premium{int(''.join(filter(str.isdigit, channel.find('a', href=True)['href'])))}/chunks.m3u8|{header}"})
            except:
                pass
    elif provider == 'USTVGO':
        channel_key = {'ABC ': 'ABC', 'ABC 7 New York': 'ABCNY', 'ACC Network': 'ACCN', 'AE ': 'AE', 'AMC ': 'AMC', 'Animal ': 'Animal', 'BBCAmerica': 'BBCAmerica', 'Big Ten Network': 'BTN', 'BET ': 'BET', 'Boomerang ': 'Boomerang', 'Bravo ': 'Bravo', 'C-SPAN': 'CSPAN', 'CBS ': 'CBS', 'CBS 2 New York': 'CBSNY', 'CBS Sports Network': 'CBSSN', 'Cinemax': 'Cinemax', 'CMT': 'CMT', 'Cartoon Network': 'CN', 'CNBC ': 'CNBC', 'CNN ': 'CNN', 'Comedy ': 'Comedy', 'CW ': 'CW', 'CW 11 New York': 'CWNY', 'Destination America': 'DA', 'Discovery': 'Discovery', 'Disney ': 'Disney', 'DisneyJr ': 'DisneyJr', 'DisneyXD ': 'DisneyXD', 'Do it yourself ( DIY ) ': 'DIY', 'E!': 'E', 'ESPN ': 'ESPN', 'ESPN2 ': 'ESPN2', 'ESPNU': 'ESPNU', 'ESPNews': 'ESPNews', 'FoodNetwork ': 'FoodNetwork', 'FOX ': 'FOX', 'FOX 5 New York': 'FOXNY', 'FoxBusiness ': 'FoxBusiness', 'FoxNews': 'FoxNews', 'Freeform ': 'Freeform', 'Fox Sports 1 (FS1)': 'FS1', 'Fox Sports 2 (FS2)': 'FS2', 'FX': 'FX', 'FX Movie Channel ': 'FXMovie', 'FXX ': 'FXX', 'Golf Channel  ': 'GOLF', 'Game Show Network ': 'GSN', 'Hallmark Channel ': 'Hallmark', 'HBO ': 'HBO', 'HGTV ': 'HGTV', 'History': 'History', 'HLN': 'HLN', 'Hallmark Movies & Mysteries': 'HMM', 'Investigation Discovery': 'ID', 'ION (WPXN) New York': 'IONNY', 'Lifetime': 'Lifetime', 'Lifetime Movie Network': 'LifetimeM', 'MLB Network': 'MLB', 'Motor Trend': 'MotorTrend', 'MSNBC': 'MSNBC', 'MTV': 'MTV', 'National Geographic ': 'NatGEO', 'Nat Geo Wild': 'NatGEOWild', 'NBA TV': 'NBA', 'NBC ': 'NBC', 'NBC 4 New York': 'NBCNY', 'NBC Sports ( NBCSN )': 'NBCSN', 'NFL Network ': 'NFL', 'NFL RedZone': 'NFLRZ', 'Nickelodeon ': 'Nickelodeon', 'Nicktoons ': 'Nicktoons', 'One America News Network': 'OAN', 'Oprah Winfrey Network (OWN) ': 'OWN', 'Olympic Channel ': 'OLY', 'Oxygen ': 'Oxygen', 'Paramount ': 'Paramount', 'PBS ': 'PBS', 'POP ': 'POP', 'Science ': 'Science', 'SEC Network': 'SECN', 'Showtime ': 'Showtime', 'StarZ ': 'StarZ', 'SundanceTV ': 'SundanceTV', 'SYFY ': 'SYFY', 'TBS ': 'TBS', 'Turner Classic Movies (TCM)': 'TCM', 'Telemundo ': 'Telemundo', 'Tennis Channel ': 'Tennis', 'TLC ': 'TLC', 'TNT ': 'TNT', 'Travel Channel ': 'Travel', 'truTV ': 'TruTV', 'TV Land ': 'TVLand', 'The Weather Channel': 'TWC', 'Univision': 'Univision', 'USA Network ': 'USANetwork', 'VH1 ': 'VH1', 'We TV ': 'WETV', 'WWE Network': 'WWE', 'YES Network': 'YES'}
        soup = BeautifulSoup(
            requests.get('https://ustvgo.tv').content, 'html.parser')
        channels_list = soup.find('div', {'class': 'entry-content'}).find_all('a')
        for channel in channels_list:
            try:
                m3u8 = f'https://h5.ustvgo.la/{channel_key[channel.text]}/myStream/playlist.m3u8?wmsAuthSign=c2VydmVyX3RpbWU9MS8yOS8yMDIyIDY6Mjg6MjggQU0maGFzaF92YWx1ZT1aWGdNakRreFY2bElqckdYT2Nha1RBPT0mdmFsaWRtaW51dGVzPTI0MA=='
                streams[category][provider].append({'name': channel.text, 'video': m3u8})
            except:
                pass
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
