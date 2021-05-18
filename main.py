"""
git@github.com:dimon1512b/Parse.git
"""
import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ria.com/uk/newauto/search/?categoryId=1'  # input('Enter url: ')
# COUNT_PAGES = input('Enter count pages: ')
# FORMAT_FILE = input('Enter format file - xlm or json: ')
DOMEN = 'https://auto.ria.com/'
HEADERS = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
	              'Chrome/90.0.4430.212 Safari/537.36',
	'accept': '*/*'
}


def get_html(url, params=None):
	print('Отправка get запроса')
	r = requests.get(url, headers=HEADERS, params=params)
	return r


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='proposition')
	cars = []
	for item in items:
		price_uah = item.find('span', class_='size16')
		price_usd = item.find('span', class_='green').get_text().strip()
		title = item.find('div', class_='proposition_title').get_text()
		link = DOMEN + item.find('a').get('href')
		city = item.find('span', class_='region').get_text()
		if price_uah:
			price_uah = price_uah.get_text()
		else:
			price_uah = 'Цена в гривне не указана'
		cars.append({
			'title': title,
			'link': link,
			'price_usd': price_usd,
			'price_uah': price_uah,
			'city': city
		})
	return cars


def parse(html):
	if html.status_code == 200:
		print('Страница доступна')
		get_content(html.text)

	else:
		print('Страница не доступна')


parse(get_html(URL))
