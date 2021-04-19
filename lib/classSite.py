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
        self.session.post(siteInfo.login_url, data=siteInfo.info)
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
        xlsh.cell(row=3,column=col).value = val

        # table = bs2.find('table', {'class': 'tbl01 jobView'}).tbody
        table = bs2.find_all('table', {'class': 'jobView'})

        for tbl in table:

            tr = tbl.find_all('tr')

            for t in tr:
                # print(t)

                th = t.find('th')
                if not th is None:
                    th = th.text.replace('\r', '').replace('\n', '').replace(' ', '')
                td = t.find('td')
                if not td is None:
                    td = td.text.replace('\r', '').replace('\n', '').replace(' ', '')


                r = 2
                while not xlsh.cell(row=r,column=1).value is None:
                    if xlsh.cell(row=r,column=1).value == th :
                        xlsh.cell(row=r,column=col).value = td
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
            if siteInfo.link_target in url:
                f.write(siteInfo.link_prefix+url+'\n')
