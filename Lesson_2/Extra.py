import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
# hh
headers = {'User-agent': 'Mozilla/5.0'}
def get_den():
    page = 0
    while True:
        main_link = 'http://glzn.ru'
        html_link = main_link + '/catalog/den/' + str(page)

        response = requests.get(html_link, headers=headers).text
        html_bs = bs(response, 'lxml')
        ultags = html_bs.find_all('ul', {'class': 'catalog'})

        items_list = []
        for ultag in html_bs.find_all('ul', {'class': 'catalog'}):
            for litag in ultag.find_all('li'):
                items_dic = {}
                item_name_div = litag.find('div').getText()
                item_link = litag.find('a')['href']
                if litag.find('div', {'class': 'catalog-price'}).findParent() == litag.find('div', {'class': 'old-price'}):
                    item_price_div = litag.find('div', {'class':'new-price'}).findChildren()
                    item_price_div = item_price_div[0].getText()
                    item_price_div_disc = litag.find('div', {'class':'catalog-price'}).getText()
                else:
                    item_price_div = litag.find('div', {'class':'catalog-price'}).getText()
                    item_price_div_disc = 0
                items_dic['name'] = item_name_div
                items_dic['price'] = item_price_div
                items_dic['price_bef_disc'] = item_price_div_disc
                items_dic['link'] = main_link + item_link
                items_dic['cat'] = 'den'
                items_list.append(items_dic)
        for i in items_list:
            print(i)
        if len(ultags) == 0:
            break
        page += 1
get_den()