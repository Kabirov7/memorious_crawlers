from memorious.logic.http import ContextHttpResponse

import kg_zakupki_proc_old.kg_zakupki_proc_old_const as const
from requests import RequestException
# import wget
import json
import kg_zakupki_proc_old.kg_zakupki_proc_old_helpers as h
import urllib.request

from time import sleep

import shutil


def initialize(context, data):
    _initiate_session(context, data, const.PAGE_LINK)

    context.emit(rule='fetch_links')


def fetch_links(context, data):
    def download_file(name, url, table_name, contract_num, num):
        names = []
        if url:
            for k in range(len(name)):
                file_expantion = name[k].split('.')[-1]
                file_name = name[k][:-(1 + len(file_expantion))].replace('-', '_').replace(' ', '_')
                file_name = f'{table_name}_{contract_num}_num{k}_{file_name}.{file_expantion}'

                response = _initiate_session(context, data, url[k])
                with context.load_file(response.serialize()['content_hash']) as fh:
                    f = open(f'D:\work\hakim\example\\files\\{file_name}', 'wb+')  #TODO: CHANGE DIRICTORY TO SAVE FILES
                    f.write(fh.read())
                    f.close()
                names.append(file_name)
            return names
        else:
            return []

    response_page = _initiate_session(context, data, const.PAGE_LINK)

    j_idt75 = response_page.html.xpath(const.J_IDT75)
    table_val = h.get_table_val(response_page)
    view_state = h.get_viewstate(response_page)

    view_state_i = view_state

    single_table = []

    lot_info_table = []

    okgz_table = []

    delivery_table = []
    delivery_files_path = []

    graph_table = []
    graph_files_path = []

    page_is = {
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': table_val,
        'javax.faces.partial.execute': table_val,
        'javax.faces.partial.render': table_val,
        'javax.faces.behavior.event': 'page',
        'javax.faces.partial.event': 'page',
        table_val + '_pagination': 'true',
        table_val + '_first': 0,
        table_val + '_rows': 10,
        table_val + '_skipChildren': 'true',
        table_val + '_encodeFeature': 'true',
        table_val.split(':')[0]: table_val.split(':')[0],
        table_val + '_selection': '',
        j_idt75: '',
        'form:supplier_input': '',
        'form:supplier_hinput': '',
        'form:dateFrom_input': '',
        'form:dateTo_input': '',
        table_val + '_rppDD': 10,
        'javax.faces.ViewState': view_state
    }

    response = _fetch_post(context, data, const.PAGE_LINK, page_is)

    contract_num = response.html.xpath(const.X_PATH_CONTRACT_NUMBER)
    j_idt = response.html.xpath(const.J_IDT93)
    procuring = response.html.xpath(const.X_PATH_PROCURING)
    provider = response.html.xpath(const.X_PATH_PROVIDER)
    type = response.html.xpath(const.X_PATH_TYPE)
    date = response.html.xpath(const.X_PATH_DATE)

    for i in range(len(j_idt)):
        try:
            single_proc = {
                'contract_number': contract_num[i],
                'procuring': procuring[i],
                'provider': provider[i],
                'type': type[i],
                'date': date[i],
            }
        except:
            single_proc = {
                'contract_number': contract_num[i],
                'procuring': procuring[i],
                'provider': '-',
                'type': type[i],
                'date': date[i],
            }
        single_table.append(single_proc)

        j_idt[i] = j_idt[i].split('{')[-1].split('}')[0].split("'")[1]
        form_preview = {
            table_val.split(':')[0]: table_val.split(':')[0],
            j_idt75: '',
            'form:supplier_input': '',
            'form:supplier_hinput': '',
            'form:dateFrom_input': '',
            'form:dateTo_input': '',
            table_val + '_rppDD': '',
            table_val + '_selection': int(contract_num[i].split("-")[-1]),
            'javax.faces.ViewState': view_state,
            j_idt[i]: j_idt[i],
        }
        page_ans = _fetch_post(context, data, const.PAGE_LINK, form_preview)

        sleep(0.5)

        lot_info = page_ans.html.xpath(const.LOT_INFO)

        lot_line = {
            'contract_number': contract_num[i],
            "type": lot_info[0].replace('\n', '').replace('\t', ''),
            "provider": lot_info[1].replace('\n', '').replace('\t', ''),
            "lot_num": lot_info[3].replace('\n', '').replace('\t', ''),
            "date_singing": lot_info[4].replace('\n', '').replace('\t', ''),
            "choose_case": lot_info[5].replace('\n', '').replace('\t', ''),
        }
        lot_info_table.append(lot_line)

        okgz_info = page_ans.html.xpath("//span[@id='product-info']//thead/tr/th/text()")
        okgz_class = page_ans.html.xpath(const.OKGZ_CLASS)
        okgz_unit = page_ans.html.xpath(const.OKGZ_UNIT)
        okgz_count = page_ans.html.xpath(const.OKGZ_COUNT)
        okgz_price_unit_item = page_ans.html.xpath(const.OKGZ_PRICE_UNIT_ITEM)
        okgz_price_sum = page_ans.html.xpath(const.OKGZ_PRICE_SUM)

        if len(okgz_info) == 8:
            okgz_brand = page_ans.html.xpath(const.OKGZ_BRAND_8)
            okgz_made_in = page_ans.html.xpath(const.OKGZ_MADE_IN_8)
            okgz_specification = page_ans.html.xpath(const.OKGZ_SPECIFICATION_8)
        elif len(okgz_info) == 6:
            okgz_specification = page_ans.html.xpath(const.OKGZ_SPECIFICATION_6)
            okgz_brand = [''] * len(okgz_specification)
            okgz_made_in = [''] * len(okgz_specification)

        del_number = page_ans.html.xpath(const.DELIVERY_NUMBER)
        del_start = page_ans.html.xpath(const.DELIVERY_START_DATE)
        del_end = page_ans.html.xpath(const.DELIVERY_FINISH_DATE)
        del_adres = page_ans.html.xpath(const.DELIVERY_ADRES_AND_PLACE)
        del_condition_payment = page_ans.html.xpath(const.DELIVERY_CONDITION_PAYMENT)
        del_doc_name = page_ans.html.xpath(const.DELIVERY_DOC_NAME)
        del_doc_url = page_ans.html.xpath(const.DELIVERY_DOC_URL)

        del_doc_names = download_file(del_doc_name, del_doc_url, 'delivery', contract_num[i], del_number)


        graph_number = page_ans.html.xpath(const.GRAPHIC_NUMBER)
        graph_satrt = page_ans.html.xpath(const.GRAPHIC_START_DATE)
        graph_end = page_ans.html.xpath(const.GRAPHIC_FINISH_DATE)
        graph_payment_type = page_ans.html.xpath(const.GRAPHIC_PAYMENT_TYPE)
        graph_condition_payment = page_ans.html.xpath(const.GRAPHIC_CONDITION_PAYMENT)
        graph_doc_name = page_ans.html.xpath(const.GRAPHIC_DOC_NAME)
        graph_doc_url = page_ans.html.xpath(const.GRAPHIC_DOC_URL)

        graph_doc_names = download_file(graph_doc_name, graph_doc_url, 'payment', contract_num[i], graph_number)

        for l in range(len(okgz_class)):
            okgz_line = {
                'contract_number': contract_num[i],
                'okgz_class': okgz_class[l],
                'okgz_unit': okgz_unit[l],
                'okgz_count': okgz_count[l],
                'okgz_price_unit_item': okgz_price_unit_item[l],
                'okgz_price_sum': okgz_price_sum[l],
                'okgz_brand': okgz_brand[l],
                'okgz_made_in': okgz_made_in[l],
                'okgz_specification': okgz_specification[l],
            }
            okgz_table.append(okgz_line)

        for l in range(len(del_number)):
            db_line = {
                'contract_number': contract_num[i],
                'number': del_number[l],
                'start_date': del_start[l],
                'finish_date': del_end[l],
                'adres': del_adres[l],
                'condition_payment': del_condition_payment[l],
            }
            delivery_table.append(db_line)

        for l in range(len(graph_number)):
            db_line = {
                'contract_number': contract_num[i],
                'number': graph_number[l],
                'start_date': graph_satrt[l],
                'finish_date': graph_end[l],
                'payment_type': graph_payment_type[l],
                'condition_payment': graph_condition_payment[l],
            }
            graph_table.append(db_line)

        if del_doc_names:
            for l in range(len(del_doc_names)):
                db_line = {
                    'contract_number': contract_num[i],
                    'title': del_doc_names[l],
                }
                delivery_files_path.append(db_line)

        if graph_doc_names:
            for l in range(len(graph_doc_names)):
                db_line = {
                    'contract_number': contract_num[i],
                    'title': graph_doc_names[l],
                }
                graph_files_path.append(db_line)

        page_ans = _fetch_post(context, data, const.PAGE_LINK, form_preview)  # fake request

    # save data
    for row in single_table:
        context.emit(rule='store_lot_procurement', data=row)

    for row in lot_info_table:
        context.emit(rule='store_lot_info', data=row)

    for row in okgz_table:
        context.emit(rule='store_okgz_classes', data=row)

    for row in delivery_table:
        context.emit(rule='store_delivery_time', data=row)

    for row in delivery_files_path:
        context.emit(rule='store_delivery_files', data=row)

    for row in graph_table:
        context.emit(rule='store_payment_schedule', data=row)

    for row in graph_files_path:
        context.emit(rule='store_payment_files', data=row)


# get - запрос
def _initiate_session(context, data, url, additionalHeaders={}):
    attempt = data.pop('retry_attempt', 1)
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'accept': '*/*'}
        headers.update(additionalHeaders)
        result = context.http.get(url, headers=headers)
        print('print() Headers')
        print(headers)

        if not result.ok:
            err = (result.url, result.status_code)
            context.emit_warning("Fetch fail [%s]: HTTP %s" % err)
            if not context.params.get('emit_errors', False):
                return
        else:
            context.log.info("Fetched [%s]: %r to get session data",
                             result.status_code,
                             result.url)
            return result

    except RequestException as ce:
        retries = int(context.get('retry', 3))
        if retries >= attempt:
            context.log.warn("Retry: %s (error: %s)", url, ce)
            data['retry_attempt'] = attempt + 1
            context.recurse(data=data, delay=2 ** attempt)
        else:
            context.emit_warning("Fetch fail [%s]: %s" % (url, ce))


# post - запрос
def _fetch_post(context, data, url, formdata):
    attempt = data.pop('retry_attempt', 1)
    try:
        result = context.http.post(url, data=formdata)

        if not result.ok:
            err = (result.url, result.status_code)
            context.emit_warning("Fetch with post fail [%s]: HTTP %s" % err)
            if not context.params.get('emit_errors', False):
                return
        else:
            context.log.info("Fetched with post [%s]: %r",
                             result.status_code,
                             result.url)
            context.log.debug("Fetched with post [%s]: %r Post form data: %s",
                              result.status_code,
                              result.url,
                              str(formdata))
            return result

    except RequestException as ce:
        retries = int(context.get('retry', 3))
        if retries >= attempt:
            context.log.warn("Retry: %s (error: %s)", url, ce)
            data['retry_attempt'] = attempt + 1
            context.recurse(data=data, delay=2 ** attempt)
        else:
            context.emit_warning("Fetch fail [%s]: %s" % (url, ce))
