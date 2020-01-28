import requests
import json
main_link = 'https://api.github.com/users/'
input_username = input('Git user_name:') # try my user name - roknikrol
get_link = requests.get(main_link+input_username+'/repos')

with open(input_username+"_repos_list.json", "w") as fp:
    for repos in get_link.json():
        json.dump(fp.writelines(repos['name'] + ' - ' + repos['html_url']+'\n'), fp)

# with open(input_username+"_repos_list.json", "w") as fp:
#     for repos in get_link.json():
#         fp.writelines(repos['name'] + ' - ' + repos['html_url']+'\n')