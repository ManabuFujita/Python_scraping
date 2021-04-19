from lib import classSite
from lib import classExcel

# ブック, シートを取得
excel = classExcel.Excel('data/data.xlsx', 'Sheet1')
xlsh = excel.getSheet()

# サイトを取得
site = classSite.Site()

# サイトから情報を取得し、Excelに転記する
col = 2
while not xlsh.cell(row=1,column=col).value is None:

    url = xlsh.cell(row=1,column=col).value

    # 取得済みなら処理しない
    if excel.hasFetched(col):
        col+=1
        continue

    # 重複ありなら"重複あり"と記載し、次の列に進む
    if excel.isDuplicated(col):
        xlsh.cell(row=2,column=col).value = "重複あり"
        excel.save()
        col+=1
        continue

    # データ取得
    site.getHtml(url, xlsh, col)
    excel.save()
    col+=1
