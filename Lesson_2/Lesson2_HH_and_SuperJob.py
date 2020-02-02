import requests
from bs4 import BeautifulSoup as bs
# hh
main_link = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text='
page = 7
vacancy_label = 'Data' + '+' + 'scientist'
headers = {'User-agent': 'Mozilla/5.0'}
html_link = main_link + vacancy_label + '&page=' + str(page)

while True:
    response = requests.get(html_link, headers=headers).text
    html_bs = bs(response, 'lxml')
    html_link = main_link + vacancy_label + '&page=' + str(page)
    page += 1
    html_bs_vacbody = html_bs.find('div', {'class': 'vacancy-serp vacancy-serp_xs-mode'})

    vac_len = len(html_bs_vacbody)
    if vac_len == 1:
        break

    html_bs_vacbody = html_bs.find('div', {'class': 'vacancy-serp vacancy-serp_xs-mode'})
    vacancies_list = []
    # end_point = html_bs.find('div', {'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})

    for i in html_bs_vacbody:
        vacancies_dict = {}
        vac_name_a = i.find('a', {'class': 'bloko-link HH-LinkModifier'})
        # expections for None objects in parsed html
        try:
            vac_link = vac_name_a['href']
            vac_name_text = vac_name_a.getText()
            vac_compen = vac_name_a.findParent().findParent().findParent().findParent()
        except TypeError:
            pass
        # exceptions for vacancies where salary is empty
        try:
            vac_compen = vac_compen.find('div', {'class': 'vacancy-serp-item__compensation'}).getText()
            vac_compen = vac_compen.replace(u'\xa0', u' ')
            if vac_compen.find('-'):
                vac_compen = vac_compen.split('-')
                vac_compen_min = vac_compen[0]
                # vac_compen_max = vac_compen[1]
        except AttributeError:
            vac_compen = 0
        vacancies_dict['Name'] = vac_name_text
        vacancies_dict['Salary'] = vac_compen
        vacancies_dict['Hyperlink'] = vac_link
        vacancies_dict['Source'] = 'hh'
        vacancies_dict['page'] = page
        vacancies_list.append(vacancies_dict)
    print(html_link)
    print(page)
    # break

for i in vacancies_list:
    print(i)
