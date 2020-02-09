import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
# hh
vacancy_label = 'Data' + '+' + 'scientist'
# vacancy_label = input('Введите навзание вакансии: ')
# vacancy_label = vacancy_label.replace(' ', '+')
headers = headers = {'User-agent' :'Mozilla/5.0'}
page = 0
vacancies_list =[]
while True:
    main_link = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text='
    html_link = main_link + vacancy_label + '&page=' + str(page)

    response = requests.get(html_link, headers=headers).text
    html_bs = bs(response, 'lxml')
    html_bs_vacbody = html_bs.find('div', {'class': 'vacancy-serp'})

    for i in html_bs_vacbody:
        vacancies_dict = {}
        vac_name_a = i.find('a', {'class' :'bloko-link HH-LinkModifier'})
        try :
            vac_link = str(vac_name_a['href'])
            vac_name_text = vac_name_a.getText()
        except TypeError :
            vac_link = ''
            vac_name_text = 0
        try :
            vac_compen = vac_name_a.findParent().findParent().findParent().findParent()
            vac_compen = vac_compen.find('div', {'class' :'vacancy-serp-item__compensation'}).getText()
            vac_compen = vac_compen.replace(u'\xa0', u' ')
            if type(vac_compen) == str :
                if len(re.findall(r'[\D]+', vac_compen.replace(' ', '').replace('-', ''))) > 1 :
                    currency = re.findall(r'[\D]+', vac_compen.replace(' ', '').replace('-', ''))[1]
                    min_max_ind = re.findall(r'[\D]+', vac_compen.replace(' ', '').replace('-', ''))[0]
                else :
                    currency = re.findall(r'[\D]+', vac_compen.replace(' ', '').replace('-', ''))[0]
                    min_max_ind = ''
                if len(re.findall(r'[0-9]+', vac_compen.replace(' ', ''))) > 1 :
                    vac_compen_min = re.findall(r'[0-9]+', vac_compen.replace(' ', ''))[0]
                    vac_compen_max = re.findall(r'[0-9]+', vac_compen.replace(' ', ''))[1]
                else :
                    vac_compen_max = re.findall(r'[0-9]+', vac_compen.replace(' ', ''))[0]
        except AttributeError:
            vac_compen = 0
            vac_compen_max = 0
            vac_compen_min = 0
            currency = ''
            min_max_ind = ''

        vacancies_dict['Name'] = vac_name_text
        vacancies_dict['Salary_min'] = vac_compen_min
        vacancies_dict['Salary_max_all'] = vac_compen_max
        vacancies_dict['Min_max_ind_all'] = min_max_ind
        vacancies_dict['Currency'] = currency
        vacancies_dict['Hyperlink'] = vac_link
        vacancies_dict['Source'] = 'hh' if vac_link != '' else ''
        if vacancies_dict['Name'] != 0:
            vacancies_list.append(vacancies_dict)


    if html_bs.find('a',{'class':'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}) == None:
        break
    page += 1


for i in vacancies_list:
    print(i)
# # writ to csv
# hh_df = pd.DataFrame(vacancies_list)
# hh_df.dropna()
# hh_df.to_csv('DS_vacancies1.csv', sep=';', encoding='windows-1251')