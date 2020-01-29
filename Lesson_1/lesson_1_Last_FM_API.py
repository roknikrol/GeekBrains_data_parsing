import requests
import json
import pandas as pd
import numpy as np

main_link = 'http://ws.audioscrobbler.com/2.0/'
api_key = '2f02c90c31c2e91b33a8ced8162ec51e'
headers = {'user-agent': 'GeekBrains'}
params = {
    'api_key': api_key,
    'method': 'chart.gettopartists',
    'format': 'json',
    'page': 1
}
get_link = requests.get(main_link, headers=headers, params=params)
output = json.loads(get_link.text)

def artists_table():
    result = {}
    name = []
    listners = []
    playcount = []
    for repos in output['artists']['artist']:
        name.append(repos['name'])
        listners.append(int(repos['listeners']))
        playcount.append(int(repos['playcount']))
    result = {'name': name, 'listeners': listners, 'playcount': playcount}
    artist_list = pd.DataFrame(result)
    artist_list.index += 1
    artist_list['Play_ratio'] = artist_list['playcount']/artist_list['listeners']
    artist_list.to_csv(r'top50_artistis_table', header='Artists Last FM')
    print(artist_list)

artists_table()



with open("top50_artistis_list.json", 'w', encoding='UTF-8') as fp:
    for repos in output['artists']['artist']:
        json.dump(fp.writelines(repos['name'] + ' - ' + repos['listeners'] + ' - ' + repos['playcount']+'\n'), fp)
# end
