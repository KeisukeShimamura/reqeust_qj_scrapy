import scrapy
from bs4 import BeautifulSoup
from request_qj_scrapy.items import RequestQjScrapyItem
import logging

class RequestQjSpider(scrapy.Spider):
  name = 'request_qj_spider'
  allowed_domains = ['www.qjnavi.jp']
  start_urls = [
    'https://www.qjnavi.jp/tokyo',
    'https://www.qjnavi.jp/kanagawa',
    'https://www.qjnavi.jp/chiba',
    'https://www.qjnavi.jp/saitama',
    'https://www.qjnavi.jp/osaka',
    'https://www.qjnavi.jp/hokkaido',
  ]

  def parse(self, response):
    soup = BeautifulSoup(response.text, 'html.parser')
    salon_list = soup.find_all('section', class_='box--companyThum')
    for salon in salon_list:
      yield scrapy.Request(salon.find('a').get('href'), self.parse_salon_page)

  def parse_salon_page(self, response):
    soup = BeautifulSoup(response.text, 'html.parser')
    item = RequestQjScrapyItem()

    item['url'] = response.url
    item['catch_copy'] = soup.find('div', class_='box--jobOffer__read').get_text().strip()
    item['salon_name'] = soup.find('p', class_='box--jobOffer__name').find('span').get_text().strip()
    item['recommend_point'] = soup.find('p', class_='box--jobOffer__txt').get_text().strip()

    table = soup.find('table', class_='box--jobOffer__buleTabel')
    tr_list = table.find_all('tr')
    for tr in tr_list:
      title = tr.find('td', class_='box--jobOffer__buleTabelTitl')
      content = tr.find('td', class_='box--jobOffer__buleTabelCont')
      if title.get_text() == '雇用形態':
        item['employment'] = content.get_text().strip()
      elif title.get_text() == '募集職種・技術ランク':
        item['job_category'] = content.get_text().strip()
      elif title.get_text() == '勤務地':
        item['access'] = content.get_text().strip()
      elif title.get_text() == '必須免許・資格':
        item['qualification'] = content.find('ul').get_text().strip()
        item['entry_requirement'] = content.find('p').get_text().strip()
      elif title.get_text() == 'こだわり':
        item['commitment_term'] = content.find('ul').get_text().strip()
      elif title.get_text() == '給与':
        item['salary'] = content.find('p').get_text().strip()
        salary_items = content.find_all('span', class_='tag-gray')
        for itm in salary_items:
          if itm.get_text() == '月給':
            item['m_salary_lower'] = itm.next_element.findNext('span').get_text().strip()
            if item['m_salary_lower'].replace('.', '').isnumeric():
              item['m_salary_lower'] = float(item['m_salary_lower']) * 10000
            else:
              item['m_salary_lower'] = ''
            item['m_salary_upper'] = itm.next_element.findNext('span').findNext('span').get_text().strip()
            if item['m_salary_upper'].replace('.', '').isnumeric():
              item['m_salary_upper'] = float(item['m_salary_upper']) * 10000
            else:
              item['m_salary_upper'] = ''
          elif itm.get_text() == '時給':
            item['t_salary_lower'] = itm.next_element.findNext('span').get_text().strip()
            item['t_salary_upper'] = itm.next_element.findNext('span').findNext('span').get_text().strip()
          elif itm.get_text() == '歩合':
            item['commission_lower'] = itm.next_element.findNext('span').get_text().strip()
            item['commission_upper'] = itm.next_element.findNext('span').findNext('span').get_text().strip()
      elif title.get_text() == '勤務時間':
        item['work_time'] = content.get_text().strip()
      elif title.get_text() == '休日':
        # holiday_list
        item['holiday'] = content.get_text().strip()
      elif title.get_text() == '福利厚生・手当て':
        item['welfare'] = content.get_text().strip()

    table = soup.find('table', class_='box--jobOffer__grayTabel')
    tr_list = table.find_all('tr')
    for tr in tr_list:
      title = tr.find('td', class_='box--jobOffer__grayTabelTitl')
      if title is None:
        title = tr.find('td', class_='box--jobOffer__buleTabelTitl')
      content = tr.find('td', class_='box--jobOffer__grayTabelCont')
      if content is None:
        content = tr.find('td', class_='box--jobOffer__buleTabelCont')
      # 各項目取得
      if title.get_text() == '開店・リニューアル':
        item['open_date'] = content.get_text().strip()
      elif title.get_text() == '営業時間':
        item['business_time'] = content.get_text().strip()
      elif title.get_text() == '定休日':
        item['regular_holiday'] = content.get_text().strip()
      elif title.get_text() == '店舗情報':
        dt_list = tr.find_all('dt')
        for dt in dt_list:
          if dt.get_text == '坪数':
            item['floor_space'] = dt.next_element.findNext('dd').get_text().replace(' 坪', '')
          elif dt.get_text == 'セット面':
            item['seat_num'] = dt.next_element.findNext('dd').get_text().replace(' 面', '')
          elif dt.get_text == 'シャンプー台':
            item['shampoo_stand'] = dt.next_element.findNext('dd').get_text().strip()
          elif dt.get_text == 'スタッフ':
            item['staff'] = dt.next_element.findNext('dd').get_text().replace(' 名', '')
          elif dt.get_text == '新規客割合':
            item['new_customer_ratio'] = dt.next_element.findNext('dd').get_text().replace(' %', '')
          elif dt.get_text == '標準カット単価':
            item['cut_unit_price'] = dt.next_element.findNext('dd').get_text().replace(' 円', '')
          elif dt.get_text == '顧客単価':
            item['customer_unit_price'] = dt.next_element.findNext('dd').get_text().replace(' 円', '')
      elif title.get_text() == '所在地':
        temp = content.get_text().split()
        item['address'] = ''
        for i, t in enumerate(temp):
          if i == 0:
            item['postcode'] = t.replace('〒', '').strip()
          else:
            if t == '地図を表示':
              break
            item['address'] += t
            item['address'] += ' '
        item['address'] = item['address'].strip()

    yield item
