import requests
from bs4 import BeautifulSoup as bs
import re
import os
from dotenv import load_dotenv

load_dotenv()

# replace this later
username = os.getenv('GMAIL_USER')
password = os.getenv('GMAIL_PASSW')

def add_keyword(keyword, whole):
    s = requests.Session()
    p = s.get('https://f5bot.com/login')
    soup = bs(p.text, 'html.parser')
    form = soup.find('form')
    csrf = form.find('input', {'name':'csrf'})['value']
    data = {'email': username, 'password': password, 'csrf': csrf}
    p = s.post('https://f5bot.com/login-post', data=data)
    soup = bs(p.text, 'html.parser')
    add = soup.find('form', {'action':'/add-alert'})
    csrf = add.find('input', {'name': 'csrf'})['value']
    flags = ''
    whole_word_only = False
    keyword = 'pepega2'
    data = {'keyword': keyword, 'flags': '', 'csrf': csrf}
    if whole_word_only:
        data['whole']=True
    s.post('https://f5bot.com/add-alert', data=data)
