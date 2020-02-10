from pymongo import MongoClient
from pprint import pprint
from lesson_2.lesson_2_hh import headhunter_vac as vac
import pandas as pd

class MongoWrite:
    clinet = MongoClient('localhost', 27017)
    db = clinet['headhunter_vacancies']
    vacancies = db.headhunter_vacancies
    def vac_to_mongo(self):
        self.vacancies.insert_many(vac())

# vac_var.vac_to_mongo()

vac()

def vacancy_search(vac_name):
    vac_var = MongoWrite()
    objects = vac_var.vacancies.find({'Name': vac_name, 'Salary_max_all':{'$ne':0}},
                                     {'Name':1,
                                      'Salary_max_all':1,
                                      'Currency':1,
                                      # 'Hyperlink':1,
                                      '_id':0 }
                                     ).sort('Salary_max_all', -1)
    result = pd.DataFrame(objects)
    result.index += 1
    print(result)

vacancy_search('Data Scientist')

