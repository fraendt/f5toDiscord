import imaplib
import email
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv

load_dotenv()

# replace this later
username = os.getenv('GMAIL_USER')
password = os.getenv('GMAIL_PASSW')

imap = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993)
imap.login(username, password)
imap.select()  # select inbox 

def check_inbox():
    try:
        _, mnr = imap.search(None, '(HEADER FROM "admin@f5bot.com")', '(UNSEEN)')
    except ConnectionResetError:
        imap.login(username, password)
    if mnr[0] == b'': # maybe save some time
        return []
    new = []
    for message_number in mnr[0].split():
        _, msg = imap.fetch(message_number, '(RFC822)')
        message = email.message_from_bytes(msg[0][1])
        html = message.get_payload()[1].get_payload()
        new.append(html)
    return new

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    keyword = soup.find('h2').text
    keyword = re.search('^Keyword: "(.*)"$', keyword).group(1)
    content = soup.find_all('p')
    ret = []
    for p in content:
        a_tag = p.find('a')
        if a_tag is None:
            continue
        link = a_tag['href']
        if 'f5bot.com' in link:
            continue
        head = str(a_tag.previous_sibling.strip())
        location = p.find('span')
        if location is None:
            continue
        location = location.text
        ret.append([keyword, head, link, location])
    return ret


    

