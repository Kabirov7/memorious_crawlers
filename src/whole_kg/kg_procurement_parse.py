import whole_kg.kg_procurement_const as const
import whole_kg.kg_procurement_helpers as h
from whole_kg.date_converter import Converter as converter


def extract(context, data):
    print('it is data',data)
    tender = data['tender']
    tender['pages'] = h.rehash_response_dict(tender['pages'], context)
    tender_page = tender['pages']['tender']
    tender_data = {'number': tender['number'],
                   'status': tender['status'],
                   'url': const.TENDER_LINK + tender['number'],
                   'procurement_object': _tender_gen_info(tender_page, 'Наименование закупки'),
                   'procuring_entity': _tender_gen_info(tender_page, 'Закупающая организация'),
                   'procurement_format': _tender_gen_info(tender_page, 'Формат закупок'),
                   'procurement_method': _tender_gen_info(tender_page, 'Метод закупок'),
                   'number_of_ads_for_contract': _tender_gen_info(tender_page, 'Номер объявления, опубликованного на портале, по которому был заключен договор'),
                   'guarantee_provision': _tender_get_guarantee(tender_page, 'Гарантийное обеспечение конкурсной заявки'),
                   'actual_address': _tender_gen_info(tender_page, 'Фактический адрес'),
                   'finance_source': _tender_gen_info(tender_page, 'Источники Финансирования'),
                   'cancel_reason': _tender_get_cancel_reason(tender_page),
                   'phone_number': _tender_gen_info(tender_page, 'Рабочий телефон'),
                   'planned_sum_int': h.to_int(_tender_gen_info(tender_page, 'Планируемая сумма')),
                   'publication_date': converter.convert(_tender_gen_info(tender_page, 'Дата публикации')),
                   'currency': _tender_gen_info(tender_page, 'Валюта конкурсной заявки'),
                   'due_date': converter.convert(_tender_gen_info(tender_page, 'Срок подачи конкурсных заявок'))}
    try:
        tender_data['ate_code'] = tender['address']['ateCode']
        tender_data['country_name'] = tender['address']['countryName']
        tender_data['region'] = tender['address']['region']
        tender_data['sub_region'] = tender['address']['subRegion']
        tender_data['district'] = tender['address']['district']
        tender_data['sub_district'] = tender['address']['subDistrict']
        tender_data['sub_sub_district'] = tender['address']['subSubDistrict']
        tender_data['locality'] = tender['address']['locality']
        tender_data['street_address'] = tender['address']['streetAddress']
    except KeyError as ke:
        context.log.info(ke)

    lots = []
    sublots = []
    for i, lot_page in enumerate(tender['pages']['lots']):
        lot = {'tender_number': tender['number'],
               'tender_url': const.TENDER_LINK + tender['number'],
               'lot_number': _lot_gen_info(tender_page, i + 1, 1),
               'lot_name': _lot_gen_info(tender_page, i + 1, 2),
               'lot_sum': _lot_gen_info(tender_page, i + 1, 3),
               'lot_sum_int': h.to_int(_lot_gen_info(tender_page, i + 1, 3)),
               'lot_location': _lot_gen_info(tender_page, i + 1, 4),
               'lot_plan': h.gettext(lot_page.html.xpath(
                   "//p//span[@class = 'extendtext']/text()")),
               'lot_class': h.gettext(lot_page.html.xpath(
                   "//p/span[@class='italic']/text()"))
               }
        lots.append(lot)
        context.log.debug('****************\n lot class: %s' % lot['lot_class'])
        for j in range(_count_sublots(tender['pages']['lots'][i])):
            sublot = {'tender_number': tender['number'],
                      'tender_url': const.TENDER_LINK + tender['number'],
                      'lot_number': _lot_gen_info(tender_page, i + 1, 1),
                      'sublot_number': str(j),
                      'sublot_class': _sublot_gen_info(tender['pages']['lots'][i], j + 1, 1),
                      'sublot_unit': _sublot_gen_info(tender['pages']['lots'][i], j + 1, 2),
                      'sublot_amount': _sublot_gen_info(tender['pages']['lots'][i], j + 1, 3),
                      'sublot_specs': _sublot_gen_info(tender['pages']['lots'][i], j + 1, 4)}
            sublots.append(sublot)


    #сколько таблиц будет, +1 самая главная
    tender_data['lots'] = lots
    tender_data['sublots'] = sublots
    tender_data['participants'] = []
    tender_data['lot_participation'] = []

    try:
        if tender['pages']['participants'] is not None:
            participants = tender['pages']['participants'].html.xpath(
                "//tbody[@id = 'submissions_data']/tr/td[@role='gridcell'][2]/text()")
            for participant in participants:
                participant = participant.strip()
                context.log.debug('participants: %s' % participant)
                bidder = {'name': participant,
                          'inn': _get_inn(participant, tender['pages']['applications'])}
                tender_data['participants'].append(bidder)
                lots = tender['pages']['participants'].html.xpath(
                    "//td[@role='gridcell'][contains(text(), '" + participant + "')]/..//td/table/tr/td[1]/text()")
                prices = tender['pages']['participants'].html.xpath(
                    "//td[@role='gridcell'][contains(text(), '" + participant + "')]/..//td/table/tr/td[3]/text()")
                for lot, price in zip(lots, prices):
                    lot = lot.split(' :')[0]
                    # TODO: make price one int column
                    price = price.strip()
                    #это то что меня интересует!!!
                    lot_participation = {'tender_number': tender['number'],
                                         'lot_number': lot,
                                         'participant_inn': bidder['inn'],
                                         'participant_name': participant,
                                         'proposed_price': price,
                                         'proposed_price_int': h.to_int(price),
                                         'results': ''
                                         }
                    print("IT IS lot_participation....", lot_participation)
                    if tender['status'] == 'complete' and tender['pages']['winners'] is not None:
                        lot_participation['results'] = _infer_lot_result(tender['pages']['winners'], lot, participant)
                    context.log.debug(lot_participation)
                    tender_data['lot_participation'].append(lot_participation)
        if tender['pages']['winners'] is not None:
            tender_data['eval_pub_date'] = h.get_evaluation_publish_date(tender['pages']['winners'])
            context.log.debug('\n' + '*' * 15 + '\n' + str(tender_data['eval_pub_date']) + '\n' + '*' * 15)
    except KeyError as ke:
        context.log.info(ke)
    context.emit(data=tender_data)


def _tender_gen_info(tender_page, label):
    result = tender_page.html.xpath(
        "//span[@class='label'][contains(text(),'%s')]/following-sibling::span//text()" % label)
    return h.gettext(result)


def _tender_get_cancel_reason(tender_page):
    result = tender_page.html.xpath("//span[contains(text(), 'Отмена Конкурса')]/following::span[1]/table/tbody//tr/td[@class='contentC']//text()")
    result += tender_page.html.xpath("//tbody/tr/td[contains(text(), 'Причина отмены')]//text()")
    return h.compose_text(result)


def _tender_get_guarantee(tender_page, label):
    result = tender_page.html.xpath("//span[@class='label'][contains(text(),'%s')]/following-sibling::span//text()" % label)
    return h.compose_text(result)


def _lot_gen_info(tender_page, tr, td):
    result = tender_page.html.xpath(
        "//tbody[contains(@id, 'lotsTable')][contains(@id, '_data')]/tr[%s]/td[%s]/span[2]/text()" % (str(tr), str(td)))
    return h.gettext(result)


def _sublot_gen_info(lot, tr, td):
    expr = "//th[contains(text(), 'Класс ОКГЗ')]/../../../tbody/tr[{}]/td[{}]/text()"
    result = lot.html.xpath(expr.format(str(tr), str(td)))
    return h.gettext(result)

def _count_sublots(lot):
    return len(lot.html.xpath("//th[contains(text(), 'Класс ОКГЗ')]/../../../tbody/tr"))


def _get_inn(participant, post_responses):
    for response in post_responses:
        result = response.html.xpath(
            "//td[contains(@class, 'contentC')][contains(text(), '" + participant + "')]/../preceding-sibling::tr/td[contains(@class, 'contentC')]/text()")
        if result:
            return result[0].strip()
    return None


def _infer_lot_result(page, lot, name):
    result = page.html.xpath(
        "//td[@role='gridcell'][contains(text(), '" + lot + "')]/..//span[contains(@id, 'winners')][contains(text(), '" + name + "')]/following-sibling::span[@class='text-results']/text()")
    if result:
        result = result[0].strip()
    else:
        result = 'lost'
    return result
