import whole_kg.kg_procurement_const as const
from banal import ensure_list
import re
from whole_kg.date_converter import Converter as converter


def number_of_links(result):
    # result = result.replace(b'<![CDATA[', b'')
    return len(result.html.xpath("//tr[@role='row']/@data-rk"))


def determine_tender_type(tender_page):
    if len(tender_page.html.xpath("//div[contains(@id, 'lotsTable2')]")) == 0:
        return 'products'
    else:
        return 'services'


def count_lots(tender_page):
    return len(tender_page.html.xpath("//tbody[contains(@id, 'lotsTable')]/tr"))


def check_protocol(tender_page):
    return len(tender_page.html.xpath("//a[contains(@id, 'contest')]"))


def check_eval(tender_page):
    return len(tender_page.html.xpath("//a[contains(@id, 'evaluation_findings')]"))


def check_cancellation(tender_page):
    return len(tender_page.html.xpath("//span[@class='text red'][contains(text(),'Отменён')]"))


def count_participants(participants_page):
    return len(participants_page.html.xpath("//tbody[@id='submissions_data']/tr"))


def gettext(items):
    for item in ensure_list(items):
        return item.strip()


def get_viewstate(response):
    return gettext(response.html.xpath("//input[@name='%s']/@value" % const.VIEWSTATE_KEY))


def serialize_response_dict(dict):
    for key, value in dict.items():
        if value is not None:
            try:
                responses = []
                for response in value:
                    responses.append(response.serialize())
                dict[key] = {}
                dict[key]['l'] = responses
            except TypeError:
                dict[key] = value.serialize()
    return dict


def rehash_response_dict(dict, context):
    for key, value in dict.items():
        if value is not None:
            try:
                responses = []
                for response in value['l']:
                    with context.http.rehash(response) as res:
                        responses.append(res)
                dict[key] = responses

            except KeyError:
                with context.http.rehash(value) as res:
                    dict[key] = res
    return dict


def to_int(plan_sum):
    result = 0
    if plan_sum is not None and len(plan_sum) > 0:
        try:
            result = re.findall(r'([\d,]*)', str(plan_sum))
            string = ''.join(result)
            result = int(float(string.replace(',', '.')))
        except ValueError as ve:
            print(ve)
            return None
    return result


def get_table_val(response):
    return response.html.xpath('string(//div[@class="ui-datatable ui-widget"]//@id)')  # j_idt106:j_idt107:table

# TODO: make one function for each form that returns array instead of multiple functions for the same form
def get_participants_form_jidt(tender_page):
    return tender_page.html.xpath("string(//a[contains(text(), 'Протокол вскрытия')]/@id)").split(":")[0]  # j_idt71:contest -> j_idt71


def get_form_for_search_field(tender_page):
    return tender_page.html.xpath("string(//input[contains(@value, 'Найти')]/@name)")  # tv1:j_idt71


def get_another_form_for_search_field(tender_page):
    return tender_page.html.xpath("//form[contains(@method,'post')]/@id")[1]  # tv1:j_idt68


def get_other_participants_form_jidt(tender_page):
    return tender_page.html.xpath("//a[contains(text(), 'Протокол вскрытия')]/@onclick")[0].split("'")[1]  # mojarra.jsfcljs(document.getElementById('j_idt69')... -> j_idt69


def get_participants_submissions_jidt(participants_page):
    return participants_page.html.xpath("//input[contains(@value, 'Просмотр конкурсной заявки')]/@name")  # [submissions:0:j_idt177:j_idt178, submissions:1:j_idt177:j_idt178]


def get_result_form_j_idt(search_page):
    return search_page.html.xpath("string(//div[contains(@class, 'ui-tooltip ui-widget ui-tooltip-right')]/@id)").split(':table')[0]  # j_idt106:j_idt107:table:640:j_idt166 -> j_idt106:j_idt107


def get_form_for_lots_table(tender_page):
    return tender_page.html.xpath("string(//div[contains(@class, 'ui-datatable ui-widget')]//@id)")  # j_idt71:lotsTable OR j_idt71:lotsTable2


def get_another_form_for_lots_table(tender_page):
    return tender_page.html.xpath("//form[contains(@enctype, 'application/x-www-form-urlencoded')]/@id")[2]  # [j_idt34, j_idt66, j_idt69, j_idt71:lotsTable:0:j_idt279:0:j_idt300:0:j_idt301] -> j_idt69


def compose_text(items):
    text = ''
    for item in items:
        text += item.strip() + '\n'
    if len(text) > 0:
        return text
    else:
        return None


def get_evaluation_publish_date(evaluation_page):
    result = evaluation_page.html.xpath("//td[contains(text(), 'Дата публикации итогов оценки')]/following-sibling::td//text()")
    return converter.convert_date_with_dots(gettext(result))
