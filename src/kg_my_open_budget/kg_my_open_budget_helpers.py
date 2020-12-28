import kg_my_open_budget.kg_my_open_budget_const as const
import datetime
import calendar

from banal import ensure_list

def get_row_item(page_html, counter, item):

    result = page_html.xpath(const.X_PATH_TABLE_ROW.format(str(counter)) + item)
    str_result = ''.join(result).strip()
    return str_result


def get_month_parameter(date):

    monthes_in_russian = {1: 'Январь',
                          2: 'Февраль',
                          3: 'Март',
                          4: 'Апрель',
                          5: 'Май',
                          6: 'Июнь',
                          7: 'Июль',
                          8: 'Август',
                          9: 'Сентябрь',
                          10: 'Октябрь',
                          11: 'Ноябрь',
                          12: 'Декабрь'
                          }

    return monthes_in_russian[date.month] + ' ' + str(date.year)

def get_viewstate(response):
    return gettext(response.html.xpath("//input[@name='%s']/@value" % const.VIEWSTATE_KEY))

def gettext(items):
    for item in ensure_list(items):
        return item.strip()

def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])

    return datetime.date(year, month, day)


def get_cookies(cookies_with_path):
    splited = cookies_with_path.split(';')
    return splited[0]


def get_date(source_date):
    return datetime.datetime.strptime(source_date, "%d.%m.%Y")

