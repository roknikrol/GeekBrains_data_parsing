import requests

main_link = 'https://api.github.com/users/'
input_username = input('Git user_name:') # try my user name - roknikrol
get_link = requests.get(main_link+input_username+'/repos')

for repos in get_link.json():
    print(repos['name'] + ' - ' + repos['html_url'])
