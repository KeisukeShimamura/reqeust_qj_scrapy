import scrapy
from bs4 import BeautifulSoup
from request_qj_scrapy.items import RequestQjSalonScrapyItem
import logging

class RequestQjSalonSpider(scrapy.Spider):
  name = 'request_qj_salon_spider'
  allowed_domains = ['www.qjnavi.jp']
  start_urls = [
    'https://www.qjnavi.jp/search?technical_rank=biyoshi,biyoshi-assistant,biyoshi-colorist',
  ]
  scrapied_salon = []

  def parse(self, response):
    soup = BeautifulSoup(response.text, 'html.parser')
    salon_list = soup.find_all('section', class_='box--companyThum')
    for salon in salon_list:
      yield scrapy.Request(salon.find('a').get('href'), self.parse_salon_page)

    # 次ページへ
    next_link = soup.find("li", class_="pager__next").findNext('a')
    yield scrapy.Request(next_link.get('href'), callback=self.parse)

  def parse_salon_page(self, response):
    soup = BeautifulSoup(response.text, 'html.parser')
    item = RequestQjSalonScrapyItem()

    item['サロン名'] = soup.find('p', class_='box--jobOffer__name').find('span').get_text().strip()
    if item['サロン名'] in self.scrapied_salon:
      return

    tel_ele = soup.find('dl', class_='box--jobOffer__contactTel')
    if tel_ele is not None:
      item['電話番号'] = tel_ele.find('dt').get_text().strip()

    table = soup.find('table', class_='box--jobOffer__buleTabel')
    tr_list = table.find_all('tr')
    for tr in tr_list:
      title = tr.find('td', class_='box--jobOffer__buleTabelTitl')
      content = tr.find('td', class_='box--jobOffer__buleTabelCont')
      if title.get_text() == '勤務先':
        temp = content.get_text().strip().split()
        access = ''
        for t in temp:
          if '駅' in t:
            if access != '':
              access += '|'
            access += t
          else:
            access += ' ' + t
        item['最寄駅'] = access

    table = soup.find('table', class_='box--jobOffer__grayTabel')
    tr_list = table.find_all('tr')
    for tr in tr_list:
      title = tr.find('td', class_='box--jobOffer__grayTabelTitl')
      if title is None:
        title = tr.find('td', class_='box--jobOffer__buleTabelTitl')
      content = tr.find('td', class_='box--jobOffer__grayTabelCont')
      if content is None:
        content = tr.find('td', class_='box--jobOffer__buleTabelCont')
      if title.get_text() == '所在地':
        temp = content.get_text().split()
        item['住所'] = ''
        for i, t in enumerate(temp):
          if i > 0:
            if t == '地図を表示':
              break
            item['住所'] += t
            item['住所'] += ' '
        item['住所'] = item['住所'].strip()

    self.scrapied_salon.append(item['サロン名'])

    yield item
