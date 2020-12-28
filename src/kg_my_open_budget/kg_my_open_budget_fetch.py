from requests import RequestException
import json
import kg_my_open_budget.kg_my_open_budget_const as const
import kg_my_open_budget.kg_my_open_budget_helpers as h
from datetime import datetime, timedelta
import calendar

import psycopg2


def initialize(context, data):
    _initiate_session(context, data, const.LINK_INCOMES)

    context.emit(rule='fetch_links')


def fetch_links(context, data):
    response_page_income = _initiate_session(context, data, const.LINK_INCOMES)
    page_html_income = response_page_income.html


    dep_income = page_html_income.xpath("//div[@class='container budget']//div[@class='col-3'][1]//text()")

    all_departaments = []
    for i in range(10, len(dep_income)-2, 2):
        all_departaments.append(dep_income[i])



    response_page_expenses = _initiate_session(context, data, const.LINK_EXPENSES)
    page_html_expenses = response_page_expenses.html


    section = page_html_expenses.xpath("//div[@id='pills-function']//div[@class='col-2'][1]//text()")
    departmental_expenses = page_html_expenses.xpath("//div[@id='pills-department']//div[@class='col-2'][1]//text()")
    departmental_expenses_id = page_html_expenses.xpath("//div[@id='pills-department']//option//@value")

    departmental_exp_id = departmental_expenses_id[2:]

    response_page_income = _initiate_session(context, data, const.LINK_INCOMES)
    page_html_income = response_page_income.html

    disc = page_html_income.xpath("//div[@class='col-2'][1]//text()")

    all_regions = []
    for i in range(6, len(disc) - 3, 2):
        all_regions.append(disc[i])

    request_region = []
    for i in range(2, len(all_regions) + 2):
        if i <= 8:
            path = "4170" + str(i) + "000000000"
        elif i == 9:
            path = "417" + str(11) + "000000000"
        elif i == 10:
            path = "417" + str(21) + "000000000"
        request_region.append(path)


    expenses_by_func = []
    for i in range(6,len(section)-2, 2):
        expenses_by_func.append(section[i])



    departmetals = []
    for i in range(6, len(departmental_expenses)-2,2):
        departmetals.append(departmental_expenses[i])

    ###creating dates for reequest
    dates = []
    start_date = datetime(2013, 1, 1)
    while start_date <= datetime.today():
        days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
        start_date += timedelta(days=days_in_month)
        dates.append(start_date.date())

    conn_string = "host='{}' dbname='{}' user='{}' password='{}'"
    conn_string = conn_string.format(const.MINJUST_HOST,
                                     const.MINJUST_DBNAME,
                                     const.MINJUST_USER,
                                     const.MINJUST_PASSWORD)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    # execute our Query
    cursor.execute(const.QUERY_INN_MINJUST)

    # retrieve the records from the database
    records = cursor.fetchall()

    ##################Общие доходы##################
    total_income = []
    total_income_blue = []
    for income in range(len(all_regions)):
        page = _initiate_session(context, data, 'http://budget.okmot.kg/ru/incomes/get-regions/'+request_region[income]+'?_type=query')
        page_text = page.text
        page_list = eval(page_text)
        for i in range(len(page_list[0])):
            path_to = page_list[0][i]
            next_page = _initiate_session(context, data, 'http://budget.okmot.kg/ru/incomes/get-districts/'+path_to['code']+'?_type=query')
            next_page_text = next_page.text
            next_page_list = eval(next_page_text)
            for n in range(len(next_page_list[0])):
                for t in range(len(dates) - 1):
                    path_to_next_page = next_page_list[0][n]
                    last_page = _initiate_session(context, data, 'http://budget.okmot.kg/ru/get-incomes?countryCode='+request_region[income]+'&regionCode='+path_to['code']+'&districtCode='+path_to_next_page['code']+'&dateFrom='+str(dates[t])+'&dateTo='+str(dates[t+1]))
                    last_page_text = last_page.text
                    last_page_list = eval(last_page_text)
                    for l in range(len(last_page_list)):
                        path_to_last = last_page_list[l]
                        print('path_to_last',path_to_last)
                        print("next")
                        for path_to_last_item in path_to_last:
                            if len(path_to_last_item['code']) != 8:
                                dab_line = {
                                    'countryCode': request_region[income],
                                    'regionCode': path_to['code'],
                                    'districCode':path_to_next_page['code'],
                                    'code': path_to_last_item['code'],
                                    'region': all_regions[income],
                                    'rayon': path_to['name']['ru'],
                                    'distric': path_to_next_page['name']['ru'],
                                    'name': path_to_last_item['name'],
                                    'republic_budget_plan': path_to_last_item['rb_p'],
                                    'republic_budget_fact': path_to_last_item['rb'],
                                    'rayon_plan': path_to_last_item['rayon'],
                                    'rayon_fact': path_to_last_item['rayon_p'],
                                    'gorod_plan':path_to_last_item['gorod'],
                                    'gorod_fact': path_to_last_item['gorod_p'],
                                    'ail_plan': path_to_last_item['ao_p'],
                                    'ail_fact': path_to_last_item['ao'],
                                    'dataFrom':dates[t],
                                    'dataTo': dates[t+1],
                                }
                                total_income_blue.append(dab_line)
                            elif len(path_to_last_item['code']) == 8:
                                db_line = {
                                    'countryCode': request_region[income],
                                    'regionCode': path_to['code'],
                                    'districCode': path_to_next_page['code'],
                                    'code': path_to_last_item['code'],
                                    'region': all_regions[income],
                                    'rayon': path_to['name']['ru'],
                                    'distric': path_to_next_page['name']['ru'],
                                    'name': path_to_last_item['name'],
                                    'republic_budget_plan': path_to_last_item['rb_p'],
                                    'republic_budget_fact': path_to_last_item['rb'],
                                    'rayon_plan': path_to_last_item['rayon'],
                                    'rayon_fact': path_to_last_item['rayon_p'],
                                    'gorod_plan': path_to_last_item['gorod'],
                                    'gorod_fact': path_to_last_item['gorod_p'],
                                    'ail_plan': path_to_last_item['ao_p'],
                                    'ail_fact': path_to_last_item['ao'],
                                    'dataFrom': dates[t],
                                    'dataTo': dates[t + 1],
                                }
                                total_income.append(db_line)

    for index in range(len(total_income)):
        db_line = {'countryCode': total_income[index]['countryCode'],
                   'regionCode': total_income[index]['regionCode'],
                   'districCode': total_income[index]['districCode'],
                   'code': total_income[index]['code'],
                   'region': total_income[index]['region'],
                   'rayon': total_income[index]['rayon'],
                   'distric': total_income[index]['distric'],
                   'name': total_income[index]['name'],
                   'republic_budget_plan': total_income[index]['republic_budget_plan'],
                   'republic_budget_fact': total_income[index]['republic_budget_fact'],
                   'rayon_plan': total_income[index]['rayon_plan'],
                   'rayon_fact': total_income[index]['rayon_fact'],
                   'gorod_plan': total_income[index]['gorod_plan'],
                   'gorod_fact': total_income[index]['gorod_fact'],
                   'ail_plan': total_income[index]['ail_plan'],
                   'ail_fact': total_income[index]['ail_fact'],
                   'dataFrom': total_income[index]['dataFrom'],
                   'dataTo': total_income[index]['dataTo'],
                   }
        context.emit(rule='store_kg_budget_new_revenue', data=db_line)

    for index in range(len(total_income_blue)):
        db_line = {'countryCode': total_income_blue[index]['countryCode'],
                   'regionCode': total_income_blue[index]['regionCode'],
                   'districCode': total_income_blue[index]['districCode'],
                   'code': total_income_blue[index]['code'],
                   'region': total_income_blue[index]['region'],
                   'rayon': total_income_blue[index]['rayon'],
                   'distric': total_income_blue[index]['distric'],
                   'name': total_income_blue[index]['name'],
                   'republic_budget_plan': total_income_blue[index]['republic_budget_plan'],
                   'republic_budget_fact': total_income_blue[index]['republic_budget_fact'],
                   'rayon_plan': total_income_blue[index]['rayon_plan'],
                   'rayon_fact': total_income_blue[index]['rayon_fact'],
                   'gorod_plan': total_income_blue[index]['gorod_plan'],
                   'gorod_fact': total_income_blue[index]['gorod_fact'],
                   'ail_plan': total_income_blue[index]['ail_plan'],
                   'ail_fact': total_income_blue[index]['ail_fact'],
                   'dataFrom': total_income_blue[index]['dataFrom'],
                   'dataTo': total_income_blue[index]['dataTo'],
                   }
        context.emit(rule='store_kg_budget_new_revenue_totals', data=db_line)

    ##################Детальное поступление по плательщикам##################
    incomes_by_payers = []
    for inn in range(len(records)):
        try:
            page_inn = _initiate_session(context, data, 'http://budget.okmot.kg/ru/income/get-inn?inn=' + records[inn][0] + '&dateFrom=&dateTo=')
            page_inn_text = page_inn.text
            page_inn_list = eval(page_inn_text)
            for g in range(len(page_inn_list['response'])):
                db_line = {
                    'inn': records[inn][0],
                    'number': page_inn_list['response'][g]['number'],
                    'period': page_inn_list['response'][g]['date'],
                    'payer': page_inn_list['response'][g]['payer'],
                    'descr': page_inn_list['response'][g]['descr'],
                    'sum': page_inn_list['response'][g]['amount'],
                }
                incomes_by_payers.append(db_line)
        except:
            pass

    for index in range(len(incomes_by_payers)):
        dab_line = {'inn': incomes_by_payers[index]['inn'],
                   'number': incomes_by_payers[index]['number'],
                   'period': incomes_by_payers[index]['period'],
                   'payer': incomes_by_payers[index]['payer'],
                   'descr': incomes_by_payers[index]['descr'],
                   'sum': incomes_by_payers[index]['sum'],
                   }
        context.emit(rule='store_kg_budget_new_income_inn_details', data=dab_line)


    ##################Доходы от платных услуг##################
    for num in range(len(all_departaments)):
        page = _initiate_session(context, data,'http://budget.okmot.kg/ru/incomes/get-subdepartments/' + departmental_exp_id[num] + '?_type=query')
        page_text = page.text
        page_list = eval(page_text)
        if len(page_content_list) != []:
            for dep in range(len(page_list[0])):
                for t in range(len(dates) - 1):
                    try:
                        path_to = page_list[0][dep]
                        page_content = _initiate_session(context, data, 'http://budget.okmot.kg/ru/get-paid-service?department=' + departmental_exp_id[num] + '&subdepartment=' + path_to['code'] + '&dateFrom=' + str(dates[t]) + '&dateTo=' + str(dates[t + 1]))
                        page_content_text = page_content.text
                        page_content_list = eval(page_content_text)
                        if page_content_list != []:
                            for c in range(len(page_content_list)):
                                db_line = {
                                    'parent_code': departmental_exp_id[num],
                                    'code': page_content_list[c]['code'],
                                    'departament': all_departaments[num],
                                    'subordination': path_to['name'],
                                    'title': page_content_list[c]['name'],
                                    'sum_plan':page_content_list[c]['plan'],
                                    'sum_fact':page_content_list[c]['fact'],
                                    'dateFrom': dates[t],
                                    'dateTo': dates[t + 1],
                                    }
                                context.emit(rule='store_kg_budget_new_income_departments', data=db_line)
                    except:
                        pass


    ##################Расходы по функциям##################
    exp_by_func = []
    exp_by_func_blue = []
    for ex_func in range(1,11):
        if ex_func < 10 :
            page = _initiate_session(context, data, 'http://budget.okmot.kg/ru/expenses/get-functions2/70'+ str(ex_func) +'?_type=query')
        elif ex_func >= 10:
            page = _initiate_session(context, data, 'http://budget.okmot.kg/ru/expenses/get-functions2/7'+ str(ex_func) +'?_type=query')
        page_text = page.text
        page_list = eval(page_text)
        for i in range(len(page_list[0])):
            code = page_list[0][i]['code']
            page_list_name = page_list[0][i]['name']
            next_page = _initiate_session(context, data, 'http://budget.okmot.kg/ru/expenses/get-functions3/'+code+'?_type=query')
            next_page_text = next_page.text
            next_page_list = eval(next_page_text)
            for n in range(len(next_page_list[0])):
                for t in range(len(dates) - 1):
                    last_path = next_page_list[0][n]
                    last_page = _initiate_session(context, data, 'http://budget.okmot.kg/ru/expenses/get-functions?function1='+str(ex_func)+'&function2='+code+'&function3='+last_path['code']+'&dateFrom='+str(dates[t])+'&dateTo='+str(dates[t+1]))
                    last_page_text = last_page.text
                    last_page_list = eval(last_page_text)
                    if last_page_list != []:
                        for l in range(len(last_page_list)):
                            if len(last_page_list[l]['code']) != 8:
                                db_line = {
                                    'code': last_page_list[l]['code'],
                                    'section': expenses_by_func[ex_func],
                                    'group': page_list_name,
                                    'functions': last_path['name'],
                                    'name': last_page_list[l]['name'],
                                    'fact_rb': last_page_list[l]['fact_rb'],
                                    'plan_rb': last_page_list[l]['plan_rb'],
                                    'fact_mb': last_page_list[l]['fact_mb'],
                                    'plan_mb': last_page_list[l]['plan_mb'],
                                    'dateFrom': dates[t],
                                    'dateTo': dates[t + 1],
                                }
                                exp_by_func_blue.append(db_line)
                            elif len(last_page_list[l]['code']) == 8:
                                db_line = {
                                    'code': last_page_list[l]['code'],
                                    'section': expenses_by_func[ex_func],
                                    'group': page_list_name,
                                    'functions': last_path['name'],
                                    'name': last_page_list[l]['name'],
                                    'fact_rb': last_page_list[l]['fact_rb'],
                                    'plan_rb': last_page_list[l]['plan_rb'],
                                    'fact_mb': last_page_list[l]['fact_mb'],
                                    'plan_mb': last_page_list[l]['plan_mb'],
                                    'dateFrom': dates[t],
                                    'dateTo': dates[t + 1],
                                }
                                exp_by_func.append(db_line)

    for index in range(len(exp_by_func)):
        db_line = {
            'code': exp_by_func[index]['code'],
            'section': exp_by_func[index]['section'],
            'group': exp_by_func[index]['group'],
            'functions': exp_by_func[index]['name'],
            'name': exp_by_func[index]['name'],
            'fact_rb': exp_by_func[index]['fact_rb'],
            'plan_rb': exp_by_func[index]['plan_rb'],
            'fact_mb': exp_by_func[index]['fact_mb'],
            'plan_mb': exp_by_func[index]['plan_mb'],
            'dateFrom': exp_by_func_blue[index]['dateFrom'],
            'dateTo': exp_by_func_blue[index]['dateTo'],
        }
        context.emit(rule='store_kg_budget_new_expenses_functions_details', data=db_line)

    for index in range(len(exp_by_func_blue)):
        db_line = {
            'code': exp_by_func_blue[index]['code'],
            'section': exp_by_func_blue[index]['section'],
            'group': exp_by_func_blue[index]['group'],
            'functions': exp_by_func_blue[index]['name'],
            'name': exp_by_func_blue[index]['name'],
            'fact_rb': exp_by_func_blue[index]['fact_rb'],
            'plan_rb': exp_by_func_blue[index]['plan_rb'],
            'fact_mb': exp_by_func_blue[index]['fact_mb'],
            'plan_mb': exp_by_func_blue[index]['plan_mb'],
            'dateFrom': exp_by_func_blue[index]['dateFrom'],
            'dateTo': exp_by_func_blue[index]['dateTo'],
        }
        context.emit(rule='store_kg_budget_new_expenses_functions_details_totals', data=db_line)



    ##################Расходы по ведомствам##################
    exp_by_departaments = []
    exp_by_departaments_blue = []
    for ex_dep in range(len(departmental_exp_id)):
        page = _initiate_session(context, data, 'http://budget.okmot.kg/ru/expenses/get-subdepartments/'+departmental_exp_id[ex_dep]+'?_type=query')
        page_text = page.text
        page_list = eval(page_text)
        for i in range(len(page_list[0])):
            path_to = page_list[0][i]
            for t in range (len(dates)-1):
                itsaa = f'http://budget.okmot.kg/ru/expenses/get-expenses-by-department?department={ex_dep}&subdepartment={path_to["code"]}&dateFrom={dates[t]}&dateTo={dates[t+1]}'
                last_page = _initiate_session(context, data, itsaa)
                last_page_text = last_page.text
                last_page_list = eval(last_page_text)
                if last_page_list != []:
                    for l in range(len(last_page_list)):
                        if len(last_page_list[l]['code']) != 8:
                            db_line = {
                                'code': last_page_list[l]['code'],
                                'departamental': departmetals[ex_dep],
                                'group': path_to['name'],
                                'name': last_page_list[l]['name'],
                                'fact_rb': last_page_list[l]['fact_rb'],
                                'plan_rb': last_page_list[l]['plan_rb'],
                                'fact_sb': last_page_list[l]['fact_sb'],
                                'plan_sb': last_page_list[l]['plan_sb'],
                                'dateFrom': dates[t],
                                'dateTo': dates[t+1],
                            }
                            exp_by_departaments_blue.append(db_line)
                        elif len(last_page_list[l]['code']) == 8:
                            db_line = {
                                'code': last_page_list[l]['code'],
                                'departamental': departmetals[ex_dep],
                                'group': path_to['name'],
                                'name': last_page_list[l]['name'],
                                'fact_rb': last_page_list[l]['fact_rb'],
                                'plan_rb': last_page_list[l]['plan_rb'],
                                'fact_sb': last_page_list[l]['fact_sb'],
                                'plan_sb': last_page_list[l]['plan_sb'],
                                'dateFrom': dates[t],
                                'dateTo': dates[t + 1],
                            }
                            exp_by_departaments.append(db_line)

    for index in range(len(exp_by_departaments)):
        db_line = {'code':exp_by_departaments[index]['code'],
                   'departamental': exp_by_departaments[index]['departamental'],
                   'group': exp_by_departaments[index]['group'],
                   'fact_rb': exp_by_departaments[index]['fact_rb'],
                   'plan_rb': exp_by_departaments[index]['plan_rb'],
                   'fact_sb': exp_by_departaments[index]['fact_sb'],
                   'plan_sb': exp_by_departaments[index]['plan_sb'],
                   'dateFrom': exp_by_departaments[index]['dateFrom'],
                   'dateTo': exp_by_departaments[index]['dateTo'],
                   }
        context.emit(rule='store_kg_budget_new_expenses_departments', data=db_line)

    for index in range(len(exp_by_departaments_blue)):
        db_line = {'code':exp_by_departaments_blue[index]['code'],
                   'departamental': exp_by_departaments_blue[index]['departamental'],
                   'group': exp_by_departaments_blue[index]['group'],
                   'fact_rb': exp_by_departaments_blue[index]['fact_rb'],
                   'plan_rb': exp_by_departaments_blue[index]['plan_rb'],
                   'fact_sb': exp_by_departaments_blue[index]['fact_sb'],
                   'plan_sb': exp_by_departaments_blue[index]['plan_sb'],
                   'dateFrom': exp_by_departaments_blue[index]['dateFrom'],
                   'dateTo': exp_by_departaments_blue[index]['dateTo'],
                   }
        context.emit(rule='store_kg_budget_new_expenses_departments_totals', data=db_line)


    ##################Расходы по получателям##################
    expenses_by_payers = []
    for inn in range(len(records)):
        try:
            page_inn = _initiate_session(context, data, 'http://budget.okmot.kg/ru/expenses/get-inn?inn=' + records[inn][0] + '&dateFrom=&dateTo=')
            page_inn_text = page_inn.text
            page_inn_list = eval(page_inn_text)
            for g in range(len(page_inn_list['response'])):
                db_line = {
                    'number': page_inn_list['response'][g]['number'],
                    'period': page_inn_list['response'][g]['date'],
                    'payer': page_inn_list['response'][g]['number'],
                    'descr': page_inn_list['response'][g]['descr'],
                    'sum': page_inn_list['response'][g]['amount'],
                    'payer_inn': str(records[inn][0])}
                expenses_by_payers.append(db_line)
        except:
            pass

    for index in range(len(expenses_by_payers)):
        db_line = {'payer_inn': expenses_by_payers[index]['payer_inn'],
                   'number': expenses_by_payers[index]['number'],
                   'period': expenses_by_payers[index]['period'],
                   'payer': expenses_by_payers[index]['payer'],
                   'description': expenses_by_payers[index]['descr'],
                   'sum': expenses_by_payers[index]['sum'],
                   }
        context.emit(rule='store_kg_budget_new_expenses_inn_details', data=db_line)


def _initiate_session(context, data, url, cookies=None):
    attempt = data.pop('retry_attempt', 1)
    try:
        context.http.reset()

        if cookies:
            headers = {'Cookie': cookies}
            result = context.http.get(url, lazy=True, headers=headers)
        else:
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


def _fetch_post(context, data, url, formdata, cookies=None):
    attempt = data.pop('retry_attempt', 1)
    try:
        if cookies:
            headers = {'Cookie': cookies}
            result = context.http.post(url, data=formdata, headers=headers)
        else:
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
