import requests
from bs4 import BeautifulSoup

from data import config

class Site:

    def __init__(self):
        self.session = ''
        self.is_login = False

    def startSession(self):
        self.session = requests.session()

    def login(self):
        if self.session == '':
            self.startSession()
        self.session.post(config.login_url, data=config.info)
        self.is_login = True

    def getHtml(self, target_url, xlsh, col):

        # loginしてなければする
        if not self.is_login:
            self.login()

        # fetch HTML
        res2 = self.session.get(target_url)
        bs2 = BeautifulSoup(res2.text, 'html.parser')

        # 社名
        val = bs2.find('h1', {'class': 'iconDisp company'}).get_text()
        xlsh.cell(row=2,column=col).value = val
        print(val)

        # アピールポイント
        val = bs2.find('p', {'class': 'appealText'}).get_text()
        xlsh.cell(row=5,column=col).value = val

        # table = bs2.find('table', {'class': 'tbl01 jobView'}).tbody
        table = bs2.find_all('table', {'class': 'jobView'})

        for tbl in table:

            tr = tbl.find_all('tr')

            for t in tr:

                if not t.find('td') is None:
                    td = t.find('td').text.replace('\r', '').replace('\n', '').replace(' ', '')
                else:
                    continue

                if not t.find('th') is None:
                    th = t.find('th').text.replace('\r', '').replace('\n', '').replace(' ', '')

                r = 6
                while not xlsh.cell(row=r,column=1).value is None:
                    if xlsh.cell(row=r,column=1).value == th :
                        if xlsh.cell(row=r,column=col).value is None:
                            xlsh.cell(row=r,column=col).value = td
                        else:
                            xlsh.cell(row=r,column=col).value += td
                        break
                    r+=1

    def getAllLinks(self, target_url, f):

        # loginしてなければする
        if not self.is_login:
            self.login()

        # fetch HTML
        res2 = self.session.get(target_url)
        bs2 = BeautifulSoup(res2.text, 'html.parser')

        links = bs2.find_all('a')
        for link in links:
            url = link.get('href')
            if url is None:
                continue
            if config.link_target in url:
                f.write(config.link_prefix+url+'\n')
