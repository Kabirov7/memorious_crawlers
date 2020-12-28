import json
import time
import psycopg2

from requests.exceptions import RequestException

import whole_kg.kg_procurement_const as const
import whole_kg.kg_procurement_helpers as h


def fetch_links(context, data):
    response_get = _initiate_session(context, data, const.LIST_URL)

    offset = data.get('offset', const.DEFAULT_OFFSET)
    table_val = h.get_table_val(response_get)
    view_state = h.get_viewstate(response_get)
    form = {
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': table_val,
        'javax.faces.partial.execute': table_val,
        'javax.faces.partial.render': table_val,
        'javax.faces.behavior.event': 'page',
        'javax.faces.partial.event': 'page',
        table_val + '_pagination': 'true',
        table_val + '_first': offset,
        table_val + '_rows': const.ROWS_NUMBER,
        table_val + '_skipChildren': 'true',
        table_val + '_encodeFeature': 'true',
        table_val.split(':')[0]: table_val.split(':')[0],
        table_val + '_selection': '',
        table_val[:-6] + '_activeIndex': '0',
        'javax.faces.ViewState': view_state
    }
    context.log.debug('\n' + '*' * 15 + '\n main page form' + '\n' + '*' * 15)
    context.log.debug(form)

    response_post = _fetch_post(context, data, const.LIST_URL, form)

    _emit_links(context, data, response_post)

    # If number of retrieved links matches the number of links requested, it probably means there are more links to retrieve.
    # TO DO Fix HTML to get the first result
    # I subtract 1 as a temporary fix to get the first result
    if h.number_of_links(response_post) == const.ROWS_NUMBER - 1:
        data = {'offset': offset + const.ROWS_NUMBER - 1}
        context.recurse(data=data)

def fetch_links_from_db(context, data):
    try:
        db_params = const.DB_PARAMS
        connection = psycopg2.connect(user=db_params['user'],
                                      password=db_params['password'],
                                      host=db_params['host'],
                                      port=db_params['port'],
                                      database=db_params['database'])

        cursor = connection.cursor()
        sql_command = 'SELECT ' + const.TENDER_NUMBERS_COLUMN_NAME + ' FROM ' + const.TENDER_NUMBERS_TABLE_NAME
        cursor.execute(sql_command)

        while True:
            tender_numbers = cursor.fetchmany(const.TENDER_NUMBERS)
            if tender_numbers:
                context.log.info(f'tenders: {len(tender_numbers)}')
                for tender_number in tender_numbers:
                    data = {'tender_number': tender_number[0]}
                    context.emit(rule='tender_number', data=data)
            else:
                break

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def fetch_tender(context, data):
    tender_address = _load_tender_address(context, data)
    tender_info = _load_tender_info(context, data)
    if tender_info['status'] == 'complete':
        tender_winners = _load_tender_winners(context, data)
    else:
        tender_winners = None
    _emit_tender(context, data, tender_info, tender_winners, tender_address)


def _load_tender_winners(context, data):
    # New session for cookies and viewstate
    main_page = _initiate_session(context, data, const.MAIN_URL)


    # Search for tender by number
    form = {h.get_another_form_for_search_field(main_page): h.get_another_form_for_search_field(main_page),
            const.SEARCH_FIELD_KEY: data['tender_number'],
            h.get_form_for_search_field(main_page): 'Найти',
            const.VIEWSTATE_KEY: h.get_viewstate(main_page)}

    search_page = _fetch_post(context, data, const.HOME_URL, form)


    # Go to tender results and return them
    form = {h.get_result_form_j_idt(search_page).split(':')[0]: h.get_result_form_j_idt(search_page).split(':')[0],
            h.get_result_form_j_idt(search_page) + ':table_rppDD': '10',
            h.get_result_form_j_idt(search_page) + ':table_selection': '',
            h.get_result_form_j_idt(search_page) + '_activeIndex': '0',
            h.get_result_form_j_idt(search_page) + ':table:0:evaluation_findings': h.get_result_form_j_idt(
                search_page) + ':table:0:evaluation_findings',
            const.VIEWSTATE_KEY: h.get_viewstate(search_page)}
    print('IT IS 108line FORM__',  form)


    context.log.debug('\n' + '*' * 15 + '\n tender winners form' + '\n' + '*' * 15 + '\n')
    context.log.debug(form)
    results_page = _fetch_post(context, data, const.LIST_URL, form)
    print('ITIS 120line RESULTS_PAGE___', results_page)
    return results_page


def _load_tender_address(context, data):
    # New session for cookies and viewstate
    main_page = _initiate_session(context, data, const.MAIN_URL)


    # Search for tender by number
    form = {h.get_another_form_for_search_field(main_page): h.get_another_form_for_search_field(main_page),
            const.SEARCH_FIELD_KEY: data['tender_number'],
            h.get_form_for_search_field(main_page): 'Найти',
            const.VIEWSTATE_KEY: h.get_viewstate(main_page)}

    search_page = _fetch_post(context, data, const.HOME_URL, form)

    # form to download item's file
    # json_form = {
    #     table_val.split(':')[0]: table_val.split(':')[0],
    #     table_val + '_rppDD': 10,
    #     table_val + '_selection': '',
    #     table_val.split(':')[0]+':' + table_val.split(':')[1] + '_activeIndex': '0',
    #     'javax.faces.ViewState': h.get_viewstate(main_page),
    #     table_val + ':0:get_json': table_val + ':0:get_json'
    # }

    # form to download all items' files from page (there should be only one anyway)
    table_val = h.get_table_val(search_page)
    json_form = {
        table_val.split(':')[0]: table_val.split(':')[0],
        table_val + ':j_idt119': '',
        table_val.split(':')[0] + '_rppDD': 10,
        table_val.split(':')[0] + '_selection': '',
        table_val.split(':')[0] + ':' + table_val.split(':')[1] + '_activeIndex': '0',
        'javax.faces.ViewState': h.get_viewstate(search_page)
    }
    context.log.debug('\n' + '*' * 15 + '\n json form' + '\n' + '*' * 15)
    context.log.debug(json_form)
    json_response = _fetch_post(context, data, const.LIST_URL, json_form)
    address = extract_address(context, json_response.serialize())
    return address


def extract_address(context, data):
    context.log.debug('\n' + '*' * 15 + '\n' + data['content_hash'] + '\n' + '*' * 15)
    with context.load_file(data['content_hash']) as fh:
        datastore = json.load(fh)
        for tender in datastore:
            try:
                item = {}
                for party in tender['parties']:
                    if 'buyer' in party['roles'] or 'tenderer' in party['roles']:
                        item = party['address']
                item['id'] = tender['tender']['id']
                context.log.debug('tender address: {}'.format(item))
                return item
            except KeyError as ke:
                context.log.info(ke)
                item = {'id': tender['tender']['id']}
                context.log.info(item)
            except IndexError as ie:
                context.log.info(ie)
                item = {'id': tender['tender']['id']}
                context.log.info(item)


def _load_tender_info(context, data):
    # Get main tender page, cookies and viewstate

    url = const.TENDER_LINK + data['tender_number']
    tender_page = _initiate_session(context, data, url)

    # Create form for post requets depending on tender type (products or services)

    tender_type = h.determine_tender_type(tender_page)
    context.log.debug('Tender type: %s' % tender_type)
    form_type_specific = {}
    row_expansion_key = ''

    if tender_type == 'products':
        # form_type_specific = const.PRODUCT_LOTS_FORM
        lots_table_value = h.get_form_for_lots_table(tender_page)  # j_idt71:lotsTable
        row_expansion_key = lots_table_value + '_expandedRowIndex'
        context.log.debug('products form: %s' % lots_table_value)
    else:
        # form_type_specific = const.SERVICE_LOTS_FORM
        lots_table_value = h.get_form_for_lots_table(tender_page)  # j_idt71:lotsTable2
        row_expansion_key = lots_table_value + '_expandedRowIndex'
        context.log.debug('service form: %s' % lots_table_value)

    form = {
        'javax.faces.source': lots_table_value,
        'javax.faces.partial.execute': lots_table_value,
        'javax.faces.partial.render': lots_table_value,
        lots_table_value: lots_table_value,
        lots_table_value + '_rowExpansion': 'true',
        row_expansion_key: '',
        lots_table_value + '_encodeFeature': 'true',
        lots_table_value + '_skipChildren': 'true',
        'javax.faces.partial.ajax': 'true',
        h.get_another_form_for_lots_table(tender_page): h.get_another_form_for_lots_table(tender_page),  # j_idt69
        lots_table_value.split(':')[0] + ':tender-doc-explanation-table_rppDD': '10',
        lots_table_value.split(':')[0] + ':tender-doc-explanation-table_selection': '',
        lots_table_value.split(':')[0] + '_activeIndex': '0',
        const.VIEWSTATE_KEY: h.get_viewstate(tender_page)
    }
    # form = const.LOTS_FORM
    # form.update(form_type_specific)

    # Get page for each lot

    lot_pages = []

    for i in range(h.count_lots(tender_page)):
        form[row_expansion_key] = str(i)
        lot_page = _fetch_post(context, data, const.VIEW_URL + '?cid=1', form)
        lot_pages.append(lot_page)

        context.log.debug('\n' + '*' * 15 + '\n tender info form' + '\n' + '*' * 15 + '\n')
        context.log.debug(form)

    participants_page = None
    application_pages = None

    # Check if the tender is over and protocol has been created.
    if h.check_protocol(tender_page) > 0:
        # Get participants page

        # form = const.PARTICIPANTS_FORM
        j_idt = h.get_participants_form_jidt(tender_page)
        j_idt_other = h.get_other_participants_form_jidt(tender_page)
        context.log.debug('participants form1: %s' % j_idt)
        context.log.debug('participants form2: %s' % j_idt_other)
        form = {
            j_idt_other: j_idt_other,
            j_idt + ':tender-doc-explanation-table_rppDD': '10',
            j_idt + ':tender-doc-explanation-table_selection': '',
            j_idt + '_activeIndex': '0',
            j_idt + ":contest": j_idt + ":contest",
            const.VIEWSTATE_KEY: h.get_viewstate(tender_page)
        }
        context.log.debug('\n' + '*' * 15 + '\n tender participants form' + '\n' + '*' * 15 + '\n')
        context.log.debug(form)
        participants_page = _fetch_post(context, data, const.VIEW_URL + '?cid=1', form)

        # Get applications pages
        if h.check_cancellation(tender_page):
            status = 'cancelled'
        else:
            application_pages = []
            submissions = h.get_participants_submissions_jidt(participants_page)
            # for i in range(h.count_participants(participants_page)):
            #     form = {
            #         'submissions:%s:j_idt177' % str(i): 'submissions:%s:j_idt177' % str(i),
            #         'submissions:%s:j_idt177:j_idt178' % str(i): 'Просмотр конкурсной заявки',
            #         const.VIEWSTATE_KEY: h.get_viewstate(participants_page)
            #     }
            for s in submissions:  # s = submissions:0:j_idt177:j_idt178
                form = {
                    s.replace(':' + s.split(':')[3], ''): s.replace(':' + s.split(':')[3], ''),  # 'submissions:0:j_idt177': 'submissions:0:j_idt177' <- 'submissions:0:j_idt177:j_idt178': 'submissions:0:j_idt177:j_idt178'
                    s: 'Просмотр конкурсной заявки',
                    const.VIEWSTATE_KEY: h.get_viewstate(participants_page)
                }
                context.log.debug('\n' + '*' * 15 + '\n submissions form' + '\n' + '*' * 15 + '\n')
                context.log.debug(form)
                application_page = _fetch_post(context, data, const.CONTEST_URL + '?cid=1', form)
                application_pages.append(application_page)
            status = 'complete'
    else:
        if h.check_cancellation(tender_page):
            status = 'cancelled'
        else:
            status = 'new'

    pages = {
        'tender': tender_page,
        'lots': lot_pages,
        'participants': participants_page,
        'applications': application_pages,
    }
    return {
        'pages': pages,
        'status': status,
        'type': tender_type
    }


def _emit_tender(context, data, tender_info, tender_winners, tender_address):
    tender = tender_info
    tender['number'] = data['tender_number']
    tender['address'] = tender_address
    tender['pages']['winners'] = tender_winners
    tender['pages'] = h.serialize_response_dict(tender['pages'])
    context.log.info(f'\ntender number: {tender["number"]}\n'
                     f'tender address: {tender["address"]}')
    data = {'tender': tender}

    context.emit(rule='tender_pages', data=data)


def _initiate_session(context, data, url):
    time.sleep(0.1)  # delay to avoid error 403
    attempt = data.pop('retry_attempt', 1)
    try:
        context.http.reset()
        result = context.http.get(url, lazy=True)

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


def _fetch_post(context, data, url, formdata):
    time.sleep(0.3)  # delay to avoid error 403
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


def _emit_links(context, data, result):
    # result = result.replace(b'<![CDATA[', b'')
    tender_numbers = result.html.xpath(const.TENDER_NUMBERS_PATH)
    if tender_numbers:
        context.log.info(f'tenders: {len(tender_numbers)}')
        for tender_number in tender_numbers:
            data = {'tender_number': tender_number}
            context.emit(rule='tender_number', data=data)
