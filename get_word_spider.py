import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
raw_html = requests.get('http://cet4.koolearn.com/20171229/820652.html', headers=headers)
raw_html.encoding = 'utf-8'
print(raw_html.text)



