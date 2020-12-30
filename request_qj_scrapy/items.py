# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RequestQjScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    catch_copy = scrapy.Field()
    salon_name = scrapy.Field()
    recommend_point = scrapy.Field()
    job_category = scrapy.Field()
    employment = scrapy.Field()
    access = scrapy.Field()
    qualification = scrapy.Field()
    entry_requirement = scrapy.Field()
    commitment_term = scrapy.Field()
    salary = scrapy.Field()
    m_salary_lower = scrapy.Field()
    m_salary_upper = scrapy.Field()
    t_salary_lower = scrapy.Field()
    t_salary_upper = scrapy.Field()
    commission_lower = scrapy.Field()
    commission_upper = scrapy.Field()
    work_time = scrapy.Field()
    holiday_list = scrapy.Field()
    holiday = scrapy.Field()
    welfare = scrapy.Field()
    open_date = scrapy.Field()
    business_time = scrapy.Field()
    regular_holiday = scrapy.Field()
    floor_space = scrapy.Field()
    seat_num = scrapy.Field()
    shampoo_stand = scrapy.Field()
    staff = scrapy.Field()
    new_customer_ratio = scrapy.Field()
    cut_unit_price = scrapy.Field()
    customer_unit_price = scrapy.Field()
    postcode = scrapy.Field()
    address = scrapy.Field()

