"""
git@github.com:dimon1512b/Parse.git
"""
import requests
from bs4 import BeautifulSoup
import csv
import json

URL = 'https://auto.ria.com/uk/newauto/search/?categoryId=1'
COUNT_PAGES = int(input('Enter count pages: '))
FORMAT_FILE = input('Enter format file - xlm or json: ').lower()
DOMAIN = 'https://auto.ria.com/'
FILE_CSV = 'cars.csv'
FILE_JSON = 'cars.json'
HEADERS = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
	              'Chrome/90.0.4430.212 Safari/537.36',
	'accept': '*/*'
}


def save_file(items, path):
	if FORMAT_FILE == 'xlm':
		with open(path, 'w', newline='') as file:
			writer = csv.writer(file, delimiter=';')
			writer.writerow(['Марка', 'Ссылка', 'Цена в $', 'Цена в UAH', 'Город'])
			for item in items:
				writer.writerow([item['title'], item['link'], item['price_usd'], item['price_uah'], item['city']])
	elif FORMAT_FILE == 'json':
		with open(path, 'w', encoding='utf8') as file:
			json.dump(items, file, ensure_ascii=False)


def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='proposition')
	cars = []
	for item in items:
		price_uah = item.find('span', class_='size16')
		price_usd = item.find('span', class_='green').get_text().strip()
		title = item.find('div', class_='proposition_title').get_text()
		link = DOMAIN + item.find('a').get('href')
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


def get_count_pages(html):
	soup = BeautifulSoup(html, 'html.parser')
	pages_soup = soup.find_all('a', class_='page-link')
	pages_lst = []
	for elem in pages_soup:
		if elem.get_text().isdigit() == True:
			pages_lst.append(int(elem.get_text()))
	return pages_lst


def get_html(url, params=None):
	try:
		r = requests.get(url, headers=HEADERS, params=params)
		return r
	except Exception:
		print('Ошибка подключения')


def parse():
	html = get_html(URL)
	pages = get_count_pages(html.text)[-1]
	cars_extend = []
	for page in range(1, pages + 1):
		html = get_html(URL, params={'page': page})
		try:
			if html.status_code == 200:
				print(f'Parse page {page} из {COUNT_PAGES}...')
				cars_extend.extend(get_content(html.text))

		except Exception:
			print('Страница не доступна')
		if page == COUNT_PAGES:
			print('Finished')
			break
	if FORMAT_FILE == 'xlm':
		save_file(cars_extend, FILE_CSV)
	elif FORMAT_FILE == 'json':
		save_file(cars_extend, FILE_JSON)


parse()
