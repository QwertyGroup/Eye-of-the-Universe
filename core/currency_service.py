from requests import get as rq_get
from bs4 import BeautifulSoup

def get_message():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    page = rq_get("https://minfin.com.ua/currency/", headers)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table',{'class':'table-response mfm-table mfcur-table-lg mfcur-table-lg-currency has-no-tfoot'})
    table_body = table.tbody
    currencies = table_body.find_all('tr')
    text = ''
    for currency in currencies[:2]:
        tds = currency.find_all('td')
        text += tds[0].a.text + '\n'
        td3 = tds[3]
        ds = td3['data-small'] 
        dt = td3.text.strip().replace('\n','').replace('/',' / ')
        text += ds + ': ' + dt + '\n*message_separator*'

    return text

def get_image():
    pass
