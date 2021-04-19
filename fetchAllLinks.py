import sys

from lib import classSite

if len(sys.argv) != 2:
    print('リンクを取得するURLを指定してください。')
    exit()

f = open('data/link.txt', 'w')

site = classSite.Site()
site.getAllLinks(sys.argv[1], f)
