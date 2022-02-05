import routing
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
import xbmcplugin
from bs4 import BeautifulSoup
import requests
import socket
import requests.packages.urllib3.util.connection as urllib3_cn
import re
from datetime import datetime, timezone, timedelta
import random
import urllib.parse

urllib3_cn.allowed_gai_family = lambda: socket.AF_INET  # Uses IPv4 over IPv6
plugin = routing.Plugin()


def random_ua():
    ua_list = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v2272396916161516908 t7889551165227354132',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v4596890125213045288 t4157550440124640339',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v7496848312646576374 t7607367907735283829',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v2804496347624254793 t1191530496833852085',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v3736745345210846356 t1236787695256497497',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v8557470257436417323 t7889551165227354132',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v2471178984251391048 t4157550440124640339',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 RuxitSynthetic/1.0 v3190326415964944516 t6281935149377429786',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v4056739060456661247 t6331743126571670211',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v1191323528017047915 t3345461284722333977']
    return random.choice(ua_list)


def random_color():
    color_list = ['blue', 'magenta', 'yellow', 'lime', 'gold', 'aqua', 'orange']
    return random.choice(color_list)


def get_m3u8(url, sport):
    headers = {'User-Agent': random_ua(), 'referer': f"{'/'.join(url.split('/', 3)[:3])}/"}
    if 'weakstreams' in url:  # Working
        soup = BeautifulSoup(requests.get(f'{url}?sport={sport}').content,
                             'html.parser')
        stream_id = re.search(r'var vidgstream = "(.*?)"', str(soup)).group(1)
        stream_id = urllib.parse.quote(stream_id.encode('utf8')).replace('/', '%2f')
        stream_url = f'http://weakstreams.com/gethls?idgstream={stream_id}'
        return f"{requests.get(stream_url).json()['rawUrl']}"
    elif 'techoreels' in url:  # Working
        resp = requests.get(url).content.decode('UTF-8')
        stream_id = re.search(r"source: '' \+ serv \+ '(.*?)'", resp).group(1)
        if '<Response [4' not in str(requests.get(f"https://reels2watch.com/hls/{stream_id}")):
            return f"https://reels2watch.com/hls/{stream_id}"
        else:
            return f"https://nflarcadia.xyz/hls/{stream_id}"
    elif any(x in url for x in  # Working
             ['hockeyweb', 'cyclingentertainment', 'pawastreams', 'givemevibes', 'ace7', 'techtricksng']):  # Working
        return re.search(r'source: "(.*?)"',
                         str(requests.get(url, headers=headers).content.decode('UTF-8')).replace("'", '"')).group(1)
    elif 'sportsnest' in url:  # Working
        return re.search(r'source:"(.*?)"',
                         str(requests.get(url, headers=headers).content.decode('UTF-8')).replace("'", '"')).group(1)
    elif 'jmutech' in url or 'sportinglive.co' in url:  # Working
        return re.search(r'source src="(.*?)"',
                         str(requests.get(url, headers=headers).content.decode('UTF-8')).replace("'", '"')).group(1)
    elif 'uhdstreams' in url:  # Working
        soup_url = BeautifulSoup(requests.get(url).content, 'html.parser').find('iframe', {'name': 'iframe1'})['src']
        return re.search(r'source: "(.*?)"',
                         str(requests.get(soup_url, headers=headers).content.decode('UTF-8')).replace("'", '"')).group(
            1)
    elif 'givemenbastreams' in url:  # Working
        soup_url = \
        BeautifulSoup(requests.get(url).content, 'html.parser').find('iframe', {'class': 'embed-responsive-item'})[
            'src']
        return re.search(r'source: "(.*?)"',
                         str(requests.get(soup_url, headers=headers).content.decode('UTF-8')).replace("'", '"')).group(
            1)
    elif 'poscitech' in url:  # Working
        header = 'referer=https://widevine.licenses4.me/'
        stream_no = \
        BeautifulSoup(requests.get(url).content, 'html.parser').find('iframe')['src'].split('tv/ch')[1].split('.php')[0]
        try:
            m3u8_url = f"https://cdn.videocdn.click/cdn/premium{stream_no}/chunks.m3u8|{header}"
            resp = requests.get(m3u8_url)
            if '<Response [4' not in str(resp):
                return f"https://cdn.videocdn.click/cdn/premium{stream_no}/chunks.m3u8|{header}"
            return f"https://i-am-so-cool.licenses4.me/cdn/premium{stream_no}/chunks.m3u8|{header}"
        except:
            return f"https://i-am-so-cool.licenses4.me/cdn/premium{stream_no}/chunks.m3u8|{header}"
    elif 'papahd' in url:
        header = 'referer=http://bestsolaris.com/'
        soup_url = BeautifulSoup(requests.get(url).content, 'html.parser').find('iframe')['src']
        return re.search(r'source: "(.*?)"',
                         str(requests.get(soup_url, headers=headers).content.decode('UTF-8')).replace("'", '"')).group(
            1) + f'|{header}'


@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(show_directory, "LiveTV"), ListItem("Live TV"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(show_directory, "Sports"), ListItem("Sports"), True)
    endOfDirectory(plugin.handle)


@plugin.route('/category/<cat>')
def show_directory(cat):
    if cat == 'LiveTV':
        addDirectoryItem(plugin.handle, plugin.url_for(show_live, "DaddyLive"), ListItem('Daddy Live'), True)
        addDirectoryItem(plugin.handle, plugin.url_for(show_live, "USTVGO"), ListItem('USTVGO'), True)
    elif cat == 'Sports':
        addDirectoryItem(plugin.handle, plugin.url_for(show_sports, "SoccerStreams"), ListItem('Soccer Streams'), True)
        addDirectoryItem(plugin.handle, plugin.url_for(show_sports, "NBAStreams"), ListItem('NBA Streams'), True)
        addDirectoryItem(plugin.handle, plugin.url_for(show_sports, "NHLStreams"), ListItem('NHL Streams'), True)
    endOfDirectory(plugin.handle)


@plugin.route('/categories/LiveTV/<provider>')
def show_live(provider):
    headers = {
        'user-agent': random_ua(),
        'referer': '',
    }
    if provider == 'DaddyLive':
        stream = 0
        stream_domain = ['https://cdn.videocdn.click', 'https://i-am-so-cool.licenses4.me']
        header = 'referer=https://widevine.licenses4.me/'
        soup = BeautifulSoup(requests.get('https://daddylive.click/24-hours-channels.php').content, 'html.parser')
        channels_list = soup.find("div", {'class': 'grid-container'}).find_all('div', 'grid-item')
        for channel in channels_list[:3]:
            try:
                m3u8_url = f"https://cdn.videocdn.click/cdn/premium{int(''.join(filter(str.isdigit, channel.find('a', href=True)['href'])))}/chunks.m3u8|{header}"
                resp = requests.get(m3u8_url)
                if '<Response [4' not in str(resp):
                    stream = 0
                    break
                stream = 1
            except:
                stream = 1
        for channel in channels_list:
            try:
                title = channel.find('strong').text
                li = ListItem(title)
                li.setInfo('video', {'title': title, 'mediatype': 'video'})
                m3u8_url = f"{stream_domain[stream]}/cdn/premium{int(''.join(filter(str.isdigit, channel.find('a', href=True)['href'])))}/chunks.m3u8|{header}"
                addDirectoryItem(plugin.handle, m3u8_url, li)
            except:
                pass
    elif provider == 'USTVGO':
        channel_key = {'ABC ': 'ABC', 'ABC 7 New York': 'ABCNY', 'ACC Network': 'ACCN', 'AE ': 'AE', 'AMC ': 'AMC',
                       'Animal ': 'Animal', 'BBCAmerica': 'BBCAmerica', 'Big Ten Network': 'BTN', 'BET ': 'BET',
                       'Boomerang ': 'Boomerang', 'Bravo ': 'Bravo', 'C-SPAN': 'CSPAN', 'CBS ': 'CBS',
                       'CBS 2 New York': 'CBSNY', 'CBS Sports Network': 'CBSSN', 'Cinemax': 'Cinemax', 'CMT': 'CMT',
                       'Cartoon Network': 'CN', 'CNBC ': 'CNBC', 'CNN ': 'CNN', 'Comedy ': 'Comedy', 'CW ': 'CW',
                       'CW 11 New York': 'CWNY', 'Destination America': 'DA', 'Discovery': 'Discovery',
                       'Disney ': 'Disney', 'DisneyJr ': 'DisneyJr', 'DisneyXD ': 'DisneyXD',
                       'Do it yourself ( DIY ) ': 'DIY', 'E!': 'E', 'ESPN ': 'ESPN', 'ESPN2 ': 'ESPN2',
                       'ESPNU': 'ESPNU', 'ESPNews': 'ESPNews', 'FoodNetwork ': 'FoodNetwork', 'FOX ': 'FOX',
                       'FOX 5 New York': 'FOXNY', 'FoxBusiness ': 'FoxBusiness', 'FoxNews': 'FoxNews',
                       'Freeform ': 'Freeform', 'Fox Sports 1 (FS1)': 'FS1', 'Fox Sports 2 (FS2)': 'FS2', 'FX': 'FX',
                       'FX Movie Channel ': 'FXMovie', 'FXX ': 'FXX', 'Golf Channel  ': 'GOLF',
                       'Game Show Network ': 'GSN', 'Hallmark Channel ': 'Hallmark', 'HBO ': 'HBO', 'HGTV ': 'HGTV',
                       'History': 'History', 'HLN': 'HLN', 'Hallmark Movies & Mysteries': 'HMM',
                       'Investigation Discovery': 'ID', 'ION (WPXN) New York': 'IONNY', 'Lifetime': 'Lifetime',
                       'Lifetime Movie Network': 'LifetimeM', 'MLB Network': 'MLB', 'Motor Trend': 'MotorTrend',
                       'MSNBC': 'MSNBC', 'MTV': 'MTV', 'National Geographic ': 'NatGEO', 'Nat Geo Wild': 'NatGEOWild',
                       'NBA TV': 'NBA', 'NBC ': 'NBC', 'NBC 4 New York': 'NBCNY', 'NBC Sports ( NBCSN )': 'NBCSN',
                       'NFL Network ': 'NFL', 'NFL RedZone': 'NFLRZ', 'Nickelodeon ': 'Nickelodeon',
                       'Nicktoons ': 'Nicktoons', 'One America News Network': 'OAN',
                       'Oprah Winfrey Network (OWN) ': 'OWN', 'Olympic Channel ': 'OLY', 'Oxygen ': 'Oxygen',
                       'Paramount ': 'Paramount', 'PBS ': 'PBS', 'POP ': 'POP', 'Science ': 'Science',
                       'SEC Network': 'SECN', 'Showtime ': 'Showtime', 'StarZ ': 'StarZ', 'SundanceTV ': 'SundanceTV',
                       'SYFY ': 'SYFY', 'TBS ': 'TBS', 'Turner Classic Movies (TCM)': 'TCM', 'Telemundo ': 'Telemundo',
                       'Tennis Channel ': 'Tennis', 'TLC ': 'TLC', 'TNT ': 'TNT', 'Travel Channel ': 'Travel',
                       'truTV ': 'TruTV', 'TV Land ': 'TVLand', 'The Weather Channel': 'TWC', 'Univision': 'Univision',
                       'USA Network ': 'USANetwork', 'VH1 ': 'VH1', 'We TV ': 'WETV', 'WWE Network': 'WWE',
                       'YES Network': 'YES'}
        m3u8 = f'https://h5.ustvgo.la_tobereplaced_myStream/playlist.m3u8?wmsAuthSign=c2VydmVyX3RpbWU9MS8yOS8yMDIyIDY6Mjg6MjggQU0maGFzaF92YWx1ZT1aWGdNakRreFY2bElqckdYT2Nha1RBPT0mdmFsaWRtaW51dGVzPTI0MA=='
        soup = BeautifulSoup(
            requests.get('https://ustvgo.tv').content, 'html.parser')
        channels_list = soup.find('div', {'class': 'entry-content'}).find_all('a')
        for channel in channels_list:
            try:
                channel_soup = BeautifulSoup(
                    requests.get(channel['href']).content, 'html.parser')
                channel_url = 'https://ustvgo.tv/' + \
                              channel_soup.find('div', {'class': 'iframe-container'}).find('iframe')['src']
                headers['referer'] = channel_url
                response = requests.get(channel_url, headers=headers)
                php_soup = BeautifulSoup(response.content, 'html.parser')
                m3u8 = re.search(r"var hls_src='(.*?)'", str(php_soup)).group(1)
                m3u8 = m3u8.replace(f'/{channel_key[channel.text]}/', '_tobereplaced_')
                break
            except:
                pass
        for channel in channels_list:
            try:
                title = channel.text
                li = ListItem(title)
                li.setInfo('video', {'title': title, 'mediatype': 'video'})
                m3u8_url = m3u8.replace('_tobereplaced_', f'/{channel_key[channel.text]}/')
                addDirectoryItem(plugin.handle, m3u8_url, li)
            except:
                pass
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    endOfDirectory(plugin.handle)


@plugin.route('/categories/Sports/<site>')
def show_sports(site):
    if site == 'SoccerStreams':
        tournaments = requests.get(
            f'https://sportscentral.io/new-api/matches?timeZone=-330&date={datetime.today().strftime("%Y-%m-%d")}').json()
        for tournament in tournaments:
            tournament_name = f"[B][COLOR {random_color()}]{tournament['name']}[/COLOR][/B]"
            tournament_img = tournament['logo']
            for event in tournament['events']:
                event_id = event['id']
                if event['status']['type'] == 'notstarted':
                    status = '[COLOR red]vs[/COLOR]'
                elif event['status']['type'] == 'canceled':
                    status = '[COLOR red]POSTPONED[/COLOR]'
                elif event['status']['type'] == 'finished':
                    status = '[COLOR red]FT[/COLOR]'
                elif event['status']['type'] == 'inprogress':
                    status = '[COLOR red]LIVE[/COLOR]'
                else:
                    status = f"[COLOR red]{event['status']['type']}[/COLOR]"
                start_time = datetime.fromtimestamp(event['startTimestamp']).strftime('%H:%M')
                event_title = f"{tournament_name} | {event['homeTeam']['name']} {status} {event['awayTeam']['name']} [{start_time}]"
                list_item = ListItem(event_title)
                list_item.setArt({'icon': tournament_img})
                addDirectoryItem(plugin.handle, plugin.url_for(show_reddit_sports, f'soccer/{event_id}'),
                                 list_item, True)
    elif site == 'NHLStreams':
        tournaments = requests.get(
            f'https://sportscentral.io/api/nhl-tournaments?&date={datetime.now(timezone(timedelta(hours=-5), "EST")).strftime("%Y-%m-%d")}').json()
        for tournament in tournaments:
            tournament_name = f"[B][COLOR grey]{tournament['name']}[/COLOR][/B]"
            tournament_img = tournament['logo']
            for event in tournament['events']:
                event_id = event['id']
                status = f"[COLOR red]{event['statusDescription']}[/COLOR]"
                start_time = datetime.fromtimestamp(event['startTimestamp']).strftime('%H:%M')
                event_title = f"{tournament_name} | {event['homeTeam']['name']} {status} {event['awayTeam']['name']} [{start_time}]"
                list_item = ListItem(event_title)
                list_item.setArt({'icon': tournament_img})
                addDirectoryItem(plugin.handle, plugin.url_for(show_reddit_sports, f'ice-hockey/{event_id}'),
                                 list_item, True)
    elif site == 'NBAStreams':
        tournaments = requests.get(
            f'https://sportscentral.io/api/nba-tournaments?&date={datetime.now(timezone(timedelta(hours=-5), "EST")).strftime("%Y-%m-%d")}').json()
        for tournament in tournaments:
            tournament_name = f"[B][COLOR blue]{tournament['name']}[/COLOR][/B]"
            tournament_img = tournament['logo']
            for event in tournament['events']:
                event_id = event['id']
                status = f"[COLOR red]{event['statusDescription']}[/COLOR]"
                start_time = datetime.fromtimestamp(event['startTimestamp']).strftime('%H:%M')
                event_title = f"{tournament_name} | {event['homeTeam']['name']} {status} {event['awayTeam']['name']} [{start_time}]"
                list_item = ListItem(event_title)
                list_item.setArt({'icon': tournament_img})
                addDirectoryItem(plugin.handle, plugin.url_for(show_reddit_sports, f'basketball/{event_id}'),
                                 list_item, True)

    endOfDirectory(plugin.handle)


@plugin.route('/categories/Sports/<path:event_id>')
def show_reddit_sports(event_id):
    stream_list_link = BeautifulSoup(
        requests.get(
            f"https://sportscentral.io/streams-table/{event_id.split('/')[1]}/{event_id.split('/')[0]}").content,
        'html.parser')
    streams = stream_list_link.find_all('div', {'class': 'stream-item'})
    for stream in streams:
        votes = stream.find('div', {'class': 'votes-count'}).text.strip()
        streamer = stream.find('span', {'class': 'username'}).text.replace('verified streamer', '').strip()
        channel = stream.find('span', {'class': 'label label-channel-name'}).text
        language = stream.find('span', {'class': 'label label-primary language'}).text
        resolution = stream.find('div', {'class': 'labels'}).find('span').text
        bitrate = stream.find('span', {'class': 'label label-bitrate'}).text
        stream_link = stream.find('div', {'class': 'watch-section'}).find('a')['href']
        if any(x in stream_link for x in
               ['hockeyweb', 'cyclingentertainment', 'pawastreams', 'givemevibes', 'ace7', 'techtricksng',
                'weakstreams',
                'techoreels', 'sportsnest', 'jmutech', 'uhdstreams', 'givemenbastreams', 'poscitech', 'papahd']):
            title = f'[{resolution} @ {bitrate}] {channel}[{language}] ({streamer}) - {votes} votes'
            li = ListItem(title)
            li.setInfo('video', {'title': title, 'mediatype': 'video'})
            try:
                m3u8_url = get_m3u8(stream_link, event_id.split('/')[0])
                if '|referer' not in m3u8_url and 'ace7' not in stream_link:
                    m3u8_url = m3u8_url + f"|referer={'/'.join(stream_link.split('/', 3)[:3])}/"
                addDirectoryItem(plugin.handle, m3u8_url, li)
            except Exception as e:
                pass
    endOfDirectory(plugin.handle)


if __name__ == '__main__':
    plugin.run()
