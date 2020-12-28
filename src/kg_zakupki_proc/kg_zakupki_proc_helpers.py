import datetime
import re

from banal import ensure_list
import kg_zakupki_proc.kg_zakupki_proc_const as const

def get_viewstate(response):
    # return gettext(response.html.xpath("//input[@name='%s']/@value" % const.VIEWSTATE_KEY))
    return gettext(response.html.xpath("string(//input[@name='javax.faces.ViewState']/@value)"))


def get_table_val(response):
    return response.html.xpath('string(//div[@class="ui-datatable ui-widget"]//@id)')

def gettext(items):
    for item in ensure_list(items):
        return item.strip()

def get_form_suplier(response):
    return response.html.xpath("string(/html/body/div[@class='main-container']/div[@class='container']/form[@id='form']/div[@class='row reportHeader']/div[@class='col-3 report-head'][1]/span/@id)")


def count_rows(page):
    return len(page.html.xpath("/html//tr/td[2]/span"))


def to_int(plan_sum):
    result = None
    if plan_sum is not None and len(plan_sum) > 0:
        try:
            result = re.findall(r'([\d,]*)', str(plan_sum))
            string = ''.join(result)
            result = int(float(string.replace(',', '.')))
        except ValueError as ve:
            print(ve)
    return result

def get_table_val(response):
    return response.html.xpath('string(//div[@class="ui-datatable ui-widget"]//@id)')  # j_idt106:j_idt107:table

def convert(date):
        # 2019-04-29
        try:
            return datetime.datetime.strptime(date, "%Y-%m-%d")
        except IndexError as ie:
            print(ie)

def get_cookies(cookies_with_path):
    splited = cookies_with_path.split(';')
    return splited[0]