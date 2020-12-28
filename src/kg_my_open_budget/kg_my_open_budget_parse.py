import kg_my_open_budget.kg_my_open_budget_const as const
import kg_my_open_budget.kg_my_open_budget_helpers as helper
from lxml import html


def extract_budget_revenue(context, data):

    page_html = html.fromstring(data['page_text'])

    name_list = page_html.xpath(const.X_PATH_TABLE_DATA_NAME_LIST)

    parent_list = page_html.xpath(const.X_PATH_TABLE_DATA_PARENTS_LIST)
    for i in range(len(parent_list)):
        parent_list[i] = parent_list[i].lstrip()

    if name_list:
        parent = ''
        for index in range(len(name_list)):

            name = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1).lstrip()
            if name in parent_list:
                parent = name
                db_line = {'region_name':               data['region_name'],
                           'district_name':             data['district_name'],
                           'rural_municipality_name':   data['rural_municipality_name'],
                           'date_month':                data['date_month'],
                           'name':                      helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1),
                           'republic_budget':           helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_2),
                           'local_budget_district':     helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_3),
                           'local_budget_city':         helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_4),
                           'local_budget_rural':        helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_5),
                           'region_link':               data['region_link'],
                           'district_link':             data['district_link'],
                           'report_link':               data['report_link']
                           }

                print(data['region_name'] + ' - ' + data['district_name'] + ': ' + db_line['name'][:60] + '...')

                #test = {'revenue': db_line}
                #context.emit(rule='pass', data=test)
                context.emit(rule='store_budget_revenue_totals', data=db_line)

            else:
                db_line = {'region_name':               data['region_name'],
                           'district_name':             data['district_name'],
                           'rural_municipality_name':   data['rural_municipality_name'],
                           'date_month':                data['date_month'],
                           'parent':                    parent,
                           'name':                      helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1),
                           'republic_budget':           helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_2),
                           'local_budget_district':     helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_3),
                           'local_budget_city':         helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_4),
                           'local_budget_rural':        helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_5),
                           'region_link':               data['region_link'],
                           'district_link':             data['district_link'],
                           'report_link':               data['report_link']
                           }

                print(data['region_name'] + ' - ' + data['district_name'] + ': ' + db_line['name'][:60] + '...')

                #test = {'revenue_total': db_line}
                #context.emit(rule='pass', data=test)
                context.emit(rule='store_budget_revenue_main', data=db_line)


def extract_income_department_details(context, data):

    page_html = html.fromstring(data['page_text'])

    name_list = page_html.xpath(const.X_PATH_TABLE_DATA_NAME_LIST)

    parent_list = page_html.xpath(const.X_PATH_TABLE_DATA_PARENTS_LIST)
    for i in range(len(parent_list)):
        parent_list[i] = parent_list[i].lstrip()

    if name_list:

        for index in range(len(name_list)):

            name = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1).lstrip()
            if name not in parent_list:

                income = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_2)
                if income == '':
                    income = '0'

                db_line = {'department_name':           data['department_name'],
                           'department_detail_name':    data['department_detail_name'],
                           'date_month':                data['date_month'],
                           'name':                      helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1),
                           'income':                    income,
                           'department_link':           data['department_link'],
                           'report_link':               data['report_link']
                           }

                print(data['department_name'] + ' - ' + data['department_detail_name'] + ' - ' + ': ' + db_line['name'][:60] + '...')

                #test = {'revenue': db_line}
                #context.emit(rule='pass', data=test)
                context.emit(rule='store_income_departments', data=db_line)


def extract_income_inn_details(context, data):

    page_html = html.fromstring(data['page_text'])

    name_list = page_html.xpath(const.X_PATH_TABLE_DATA_INN_NAME_LIST)

    parent_list = page_html.xpath(const.X_PATH_TABLE_DATA_INN_PARENTS_LIST)
    for i in range(len(parent_list)):
        parent_list[i] = parent_list[i].lstrip()

    if name_list:

        for index in range(len(name_list)):

            name = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_3).lstrip()
            if name not in parent_list:

                #forman sum
                pay_sum = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_5)
                if pay_sum == '':
                    pay_sum = '0'

                #format date
                payment_date = helper.get_date(helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_2).lstrip())

                db_line = {'inn':               data['inn'],
                           'inn_minjust':       data['inn_minjust'],
                           'page_link':         data['page_link'],
                           'inn_taxpayer_name': data['inn_taxpayer_name'],
                           'document_number':   helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1).lstrip(),
                           'payment_date':      payment_date,
                           'taxpayer_name':     helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_3_TITLE).lstrip(),
                           'purpose':           helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_4_TITLE).lstrip(),
                           'pay_sum':           pay_sum
                            }

                print(data['inn'] + ' - ' + data['inn_taxpayer_name'] + ': ' + db_line['pay_sum'])

                context.emit(rule='store_income_inn_details', data=db_line)


def extract_expenses_functions_details(context, data):

    page_html = html.fromstring(data['page_text'])

    name_list = page_html.xpath(const.X_PATH_TABLE_DATA_NAME_LIST)

    try:
        parent_list = page_html.xpath(const.X_PATH_TABLE_DATA_PARENTS_LIST)
        for i in range(len(parent_list)):
            parent_list[i] = parent_list[i].lstrip()

    except:
        print('ERROR!!!!!!!!!!\nERROR!!!!!!!!!\n' + data['report_link'] + ' --- ' + data['date_month'])

    if name_list:
        parent = ''
        for index in range(len(name_list)):

            republic_budget_sum = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_2)
            if republic_budget_sum == '':
                republic_budget_sum = '0'

            local_budget_sum = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_3)
            if local_budget_sum == '':
                local_budget_sum = '0'

            name = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1_STRONG).lstrip()
            if name:

                parent = name
                db_line = {'name':                              name,
                           'republic_budget_sum':               republic_budget_sum,
                           'local_budget_sum':                  local_budget_sum,
                           'function_name':                     data['function_name'],
                           'function_link':                     data['function_link'],
                           'function_details_link_level_one':   data['function_details_link_level_one'],
                           'function_details_name_level_one':   data['function_details_name_level_one'],
                           'function_details_name_level_two':   data['function_details_name_level_two'],
                           'report_link':                       data['report_link'],
                           'date_month':                        data['date_month']
                           }

                print(data['function_name'] + ' - ' + data['function_details_name_level_one'] + ' - ' + ': ' + db_line['name'][:60] + '...')

                #test = {'revenue': db_line}
                #context.emit(rule='pass', data=test)
                context.emit(rule='store_expenses_functions_details_totals', data=db_line)

            else:
                name = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1).lstrip()
                db_line = {'name': name,
                           'republic_budget_sum': republic_budget_sum,
                           'local_budget_sum': local_budget_sum,
                           'parent': parent,
                           'function_name': data['function_name'],
                           'function_link': data['function_link'],
                           'function_details_link_level_one': data['function_details_link_level_one'],
                           'function_details_name_level_one': data['function_details_name_level_one'],
                           'function_details_name_level_two': data['function_details_name_level_two'],
                           'report_link': data['report_link'],
                           'date_month': data['date_month']
                           }

                print(data['function_name'] + ' - ' + data['function_details_name_level_one'] + ' - ' + ': ' + db_line['name'][
                                                                                                        :60] + '...')

                # test = {'revenue': db_line}
                # context.emit(rule='pass', data=test)
                context.emit(rule='store_expenses_functions_details', data=db_line)


def extract_expenses_departments_details(context, data):

    page_html = html.fromstring(data['page_text'])

    name_list = page_html.xpath(const.X_PATH_TABLE_DATA_NAME_LIST)

    parent_list = page_html.xpath(const.X_PATH_TABLE_DATA_PARENTS_LIST)
    for i in range(len(parent_list)):
        parent_list[i] = parent_list[i].lstrip()

    if name_list:
        parent = ''
        for index in range(len(name_list)):

            budget_sum = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_2)
            if budget_sum == '':
                budget_sum = '0'

            special_sum = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_3)
            if special_sum == '':
                special_sum = '0'

            name = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1_STRONG).lstrip()
            if name:
                parent = name

                db_line = {'department_name':           data['department_name'],
                           'department_detail_name':    data['department_detail_name'],
                           'date_month':                data['date_month'],
                           'name':                      name,
                           'budget_sum':                budget_sum,
                           'special_sum':               special_sum,
                           'department_link':           data['department_link'],
                           'report_link':               data['report_link']
                           }

                print(data['department_name'] + ' - ' + data['department_detail_name'] + ' - ' + ': ' + db_line['name'][:60] + '...')

                #test = {'revenue': db_line}
                #context.emit(rule='pass', data=test)
                context.emit(rule='store_expenses_departments_details_totals', data=db_line)

            else:
                name = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1).lstrip()
                db_line = {'department_name':           data['department_name'],
                           'department_detail_name':    data['department_detail_name'],
                           'date_month':                data['date_month'],
                           'name':                      name,
                           'parent':                    parent,
                           'budget_sum':                budget_sum,
                           'special_sum':               special_sum,
                           'department_link':           data['department_link'],
                           'report_link':               data['report_link']
                           }

                print(data['department_name'] + ' - ' + data['department_detail_name'] + ' - ' + ': ' + db_line['name'][:60] + '...')

                #test = {'revenue': db_line}
                #context.emit(rule='pass', data=test)o
                context.emit(rule='store_expenses_departments_details', data=db_line)


def extract_expenses_inn_details(context, data):

    page_html = html.fromstring(data['page_text'])

    name_list = page_html.xpath(const.X_PATH_TABLE_DATA_INN_NAME_LIST)

    parent_list = page_html.xpath(const.X_PATH_TABLE_DATA_INN_PARENTS_LIST)
    for i in range(len(parent_list)):
        parent_list[i] = parent_list[i].lstrip()

    if name_list:

        for index in range(len(name_list)):

            name = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_3).lstrip()
            if name not in parent_list:

                #forman sum
                pay_sum = helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_5)
                if pay_sum == '':
                    pay_sum = '0'

                #format date
                payment_date = helper.get_date(helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_2).lstrip())

                db_line = {'inn':               data['inn'],
                           'inn_minjust':       data['inn_minjust'],
                           'page_link':         data['page_link'],
                           'inn_taxpayer_name': data['inn_taxpayer_name'],
                           'document_number':   helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_1).lstrip(),
                           'payment_date':      payment_date,
                           'taxpayer_name':     helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_3).lstrip(),
                           'purpose':           helper.get_row_item(page_html, index + 1, const.X_PATH_TABLE_DATA_COLUMN_4_TITLE).lstrip(),
                           'pay_sum':           pay_sum
                            }

                print(data['inn'] + ' - ' + data['inn_taxpayer_name'] + ': ' + db_line['pay_sum'])

                context.emit(rule='store_expenses_inn_details', data=db_line)