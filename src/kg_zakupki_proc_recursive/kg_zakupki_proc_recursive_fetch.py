import kg_zakupki_proc.kg_zakupki_proc_const as const
from requests import RequestException
import kg_zakupki_proc.kg_zakupki_proc_helpers as helpers
from time import sleep
from pprint import pprint
from datetime import datetime
import random


def get_count_contracts(context, data):
	# seed_page = _initiate_session(context, data, const.SEED_LINK)
	#
	# contract_number_form = seed_page.html.xpath(const.CONTRACT_NUMBER_FORM)
	# table_val = helpers.get_table_val(seed_page)
	# view_state = helpers.get_viewstate(seed_page)
	#
	# request_form = {
	# 	'javax.faces.partial.ajax': 'true',
	# 	'javax.faces.source': table_val,
	# 	'javax.faces.partial.execute': table_val,
	# 	'javax.faces.partial.render': table_val,
	# 	'javax.faces.behavior.event': 'page',
	# 	'javax.faces.partial.event': 'page',
	# 	table_val + '_pagination': 'true',
	# 	table_val + '_first': 0,
	# 	table_val + '_rows': 100000,
	# 	table_val + '_skipChildren': 'true',
	# 	table_val + '_encodeFeature': 'true',
	# 	table_val.split(':')[0]: table_val.split(':')[0],
	# 	table_val + '_selection': '',
	# 	contract_number_form: '',
	# 	'form:supplier_input': '',
	# 	'form:supplier_hinput': '',
	# 	'form:dateFrom_input': '',
	# 	'form:dateTo_input': '',
	# 	table_val + '_rppDD': 10,
	# 	'javax.faces.ViewState': view_state
	# }
	#
	#
	# response = _fetch_post(context, data, const.SEED_LINK, request_form)
	#
	# count_contracts = len(response.html.xpath(const.X_PATH_CONTRACT_NUMBER))
	count_contracts = 1000

	data = {
		"count_contracts": count_contracts,
		"first": 0,
		"step": 10
	}

	context.emit(rule='get_fifty_contracts', data=data)


def get_fifty_contracts(context, data):
	def download_file(name, url, table_name, contract_num, num):
		names = []
		if url:
			for k in range(len(name)):
				file_expantion = name[k].split('.')[-1]
				file_name = name[k][:-(1 + len(file_expantion))].replace('-', '_').replace(' ', '_')
				file_name = f'{table_name}_{contract_num}_num{k}_{file_name}.{file_expantion}'

				response = _initiate_session(context, data, url[k])
				# with context.load_file(response.serialize()['content_hash']) as fh:
				# 	f = open(f'/stiGov/data/{file_name}',
				# 			 'wb+')  # TODO: CHANGE DIRICTORY TO SAVE FILES
				# 	f.write(fh.read())
				# 	f.close()
				names.append(file_name)
			return names
		else:
			return []

	seed_page = _initiate_session(context, {}, const.SEED_LINK)

	contract_number_form = seed_page.html.xpath(const.CONTRACT_NUMBER_FORM)
	table_val = helpers.get_table_val(seed_page)
	view_state = helpers.get_viewstate(seed_page)

	request_form = {
		'javax.faces.partial.ajax': 'true',
		'javax.faces.source': table_val,
		'javax.faces.partial.execute': table_val,
		'javax.faces.partial.render': table_val,
		'javax.faces.behavior.event': 'page',
		'javax.faces.partial.event': 'page',
		table_val + '_pagination': 'true',
		table_val + '_first': data["first"],
		table_val + '_rows': data["step"],
		table_val + '_skipChildren': 'true',
		table_val + '_encodeFeature': 'true',
		table_val.split(':')[0]: table_val.split(':')[0],
		table_val + '_selection': '',
		contract_number_form: '',
		'form:supplier_input': '',
		'form:supplier_hinput': '',
		'form:dateFrom_input': '',
		'form:dateTo_input': '',
		table_val + '_rppDD': data["step"],
		'javax.faces.ViewState': view_state
	}

	response = _fetch_post(context, {}, const.SEED_LINK, request_form)

	purchases = {
		'contracts_num': response.html.xpath(const.X_PATH_CONTRACT_NUMBER),
		'contracts_ids_for_request_form': response.html.xpath(const.CONTRACTS_IDS_FOR_REQUEST_FORM),
		'procuring_organization': response.html.xpath(const.X_PATH_PROCURING_ORGANIZATION),
		'provider': response.html.xpath(const.X_PATH_PROVIDER),
		'contract_type': response.html.xpath(const.X_PATH_TYPE),
		'date': response.html.xpath(const.X_PATH_DATE),
		'contract_number_form': contract_number_form,
		'table_val': table_val,
		'view_state': view_state
	}


	contracts_number = len(purchases['contracts_ids_for_request_form'])
	for i in range(contracts_number):  # for every contract
		okgz_classes_procurement = []
		delivery_time_procurement = []
		payment_schedule_procurement = []
		payment_files_procurement = []
		delivery_files_procurement = []

		try:
			date = datetime.strptime(purchases['date'][i], "%d.%m.%Y")
		except Exception as e:
			date = purchases['date'][i]
		try:
			general_info = {
				'contract_number': purchases['contracts_num'][i],
				'procuring': purchases['procuring_organization'][i],
				'provider': purchases['provider'][i],
				'type': purchases['contract_type'][i],
				'date': date
			}
		except Exception as e:
			general_info = {
				'contract_number': purchases['contracts_num'][i],
				'procuring': purchases['procuring_organization'][i],
				'provider': purchases['provider'][i],
				'type': purchases['contract_type'][i],
				'date': date
			}

		new_data = {
			"contracts_ids_for_request_form": purchases["contracts_ids_for_request_form"][i],
			"contract_number_form": purchases["contract_number_form"],
			"table_val": purchases["table_val"],
			"view_state": purchases["view_state"],
			"general_info": general_info,
			"iteration": i
		}

		print('new_data: => ',new_data["general_info"])

		new_data["contracts_ids_for_request_form"] = \
			new_data["contracts_ids_for_request_form"].split('{')[-1].split('}')[0].split("'")[1]

		form_preview = {
			new_data['table_val'].split(':')[0]: new_data['table_val'].split(':')[0],
			new_data['contract_number_form']: '',
			'form:supplier_input': '',
			'form:supplier_hinput': '',
			'form:dateFrom_input': '',
			'form:dateTo_input': '',
			new_data['table_val'] + '_rppDD': '',
			new_data['table_val'] + '_selection': int(new_data["general_info"]["contract_number"].split("-")[-1]),
			'javax.faces.ViewState': new_data['view_state'],
			new_data["contracts_ids_for_request_form"]: new_data["contracts_ids_for_request_form"],
		}
		sleep(0.3)
		contract_response = _fetch_post(context, {}, const.SEED_LINK, form_preview)

		lot_info = contract_response.html.xpath(const.LOT_INFO)

		if lot_info:
			print("norm_status", contract_response.response)
		else:
			sleep(random.uniform(1, 2))
			contract_response = _fetch_post(context, {}, const.SEED_LINK, form_preview)
			lot_info = contract_response.html.xpath(const.LOT_INFO)

			print("nenorm_status", contract_response.response)

		lot_num = lot_info[3].replace('\n', '').replace('\t', '')

		lot_line = {
			'contract_number': new_data["general_info"]["contract_number"],
			"type": lot_info[0].replace('\n', '').replace('\t', ''),
			"provider": lot_info[1].replace('\n', '').replace('\t', ''),
			"lot_num": str(lot_num),
			"date_singing": datetime.strptime(lot_info[4].replace('\n', '').replace('\t', ''), "%Y-%m-%d"),
			"choose_case": lot_info[5].replace('\n', '').replace('\t', ''),
		}
		new_data["general_info"]["lot_num"] = lot_num

		print("lot_line => ", lot_line)


		okgz_info = contract_response.html.xpath("//span[@id='product-info']//thead/tr/th/text()")
		okgz_class = contract_response.html.xpath(const.OKGZ_CLASS)
		okgz_unit = contract_response.html.xpath(const.OKGZ_UNIT)
		okgz_count = contract_response.html.xpath(const.OKGZ_COUNT)
		okgz_price_unit_item = contract_response.html.xpath(const.OKGZ_PRICE_UNIT_ITEM)
		okgz_price_sum = contract_response.html.xpath(const.OKGZ_PRICE_SUM)

		if len(okgz_info) == 8:
			okgz_brand = contract_response.html.xpath(const.OKGZ_BRAND_8) if contract_response.html.xpath(
				const.OKGZ_BRAND_8) else [""] * len(okgz_info)
			okgz_made_in = contract_response.html.xpath(const.OKGZ_MADE_IN_8) if contract_response.html.xpath(
				const.OKGZ_MADE_IN_8) else [""] * len(okgz_info)
			okgz_specification = contract_response.html.xpath(const.OKGZ_SPECIFICATION_8) if contract_response.html.xpath(
				const.OKGZ_SPECIFICATION_8) else [""] * len(okgz_info)
		elif len(okgz_info) == 6:
			okgz_specification = contract_response.html.xpath(const.OKGZ_SPECIFICATION_6) if contract_response.html.xpath(
				const.OKGZ_SPECIFICATION_6) else [""] * len(okgz_info)
			okgz_brand = [''] * len(okgz_class)
			okgz_made_in = [''] * len(okgz_class)

		del_number = contract_response.html.xpath(const.DELIVERY_NUMBER)
		del_start = contract_response.html.xpath(const.DELIVERY_START_DATE)
		del_end = contract_response.html.xpath(const.DELIVERY_FINISH_DATE)
		del_adres = contract_response.html.xpath(const.DELIVERY_ADRES_AND_PLACE)
		del_condition_payment = contract_response.html.xpath(const.DELIVERY_CONDITION_PAYMENT)
		del_doc_name = contract_response.html.xpath(const.DELIVERY_DOC_NAME)
		del_doc_url = contract_response.html.xpath(const.DELIVERY_DOC_URL)

		del_doc_names = download_file(del_doc_name, del_doc_url, 'delivery', new_data["general_info"]["contract_number"],
									  del_number)

		graph_number = contract_response.html.xpath(const.GRAPHIC_NUMBER)
		graph_satrt = contract_response.html.xpath(const.GRAPHIC_START_DATE)
		graph_end = contract_response.html.xpath(const.GRAPHIC_FINISH_DATE)
		graph_payment_type = contract_response.html.xpath(const.GRAPHIC_PAYMENT_TYPE)
		graph_condition_payment = contract_response.html.xpath(const.GRAPHIC_CONDITION_PAYMENT)
		graph_doc_name = contract_response.html.xpath(const.GRAPHIC_DOC_NAME)
		graph_doc_url = contract_response.html.xpath(const.GRAPHIC_DOC_URL)

		graph_doc_names = download_file(graph_doc_name, graph_doc_url, 'payment', new_data["general_info"]["contract_number"],
										graph_number)

		for l in range(len(okgz_class)):
			okgz_line = {
				'contract_number': new_data["general_info"]["contract_number"],
				'lot_num': lot_num,
				'okgz_class': okgz_class[l],
				'okgz_unit': okgz_unit[l],
				'okgz_count': okgz_count[l],
				'okgz_price_unit_item': float(okgz_price_unit_item[l].replace("\xa0", "").replace(",", ".")),
				'okgz_price_sum': float(okgz_price_sum[l].replace("\xa0", "").replace(",", ".")),
				'okgz_specification': okgz_specification[l],
				"okgz_made_in": okgz_made_in[l],
				"okgz_brand": okgz_brand[l],
			}
			okgz_classes_procurement.append(okgz_line)

		for l in range(len(del_number)):
			delivery_line = {
				'contract_number': new_data["general_info"]["contract_number"],
				'lot_num': lot_num,
				'number': del_number[l],
				'start_date': datetime.strptime(del_start[l], "%d.%m.%Y"),
				'finish_date': datetime.strptime(del_end[l], "%d.%m.%Y"),
				'adres': del_adres[l],
				'condition_payment': del_condition_payment[l],
			}
			delivery_time_procurement.append(delivery_line)

		for l in range(len(graph_number)):
			graph_line = {
				'contract_number': new_data["general_info"]["contract_number"],
				'lot_num': lot_num,
				'number': graph_number[l],
				'start_date': datetime.strptime(graph_satrt[l], "%d.%m.%Y"),
				'finish_date': datetime.strptime(graph_end[l], "%d.%m.%Y"),
				'payment_type': graph_payment_type[l],
				'condition_payment': graph_condition_payment[l],
			}
			payment_schedule_procurement.append(graph_line)

		if del_doc_names:
			for l in range(len(del_doc_names)):
				db_line = {
					'contract_number': new_data["general_info"]["contract_number"],
					'title': del_doc_names[l],
				}
				delivery_files_procurement.append(db_line)

		if graph_doc_names:
			for l in range(len(graph_doc_names)):
				db_line = {
					'contract_number': new_data["general_info"]["contract_number"],
					'title': graph_doc_names[l],
				}
				payment_files_procurement.append(db_line)

		contract_data = {
			"lot_procurement": new_data["general_info"],
			"lot_info_procurement": lot_line,
			"okgz_classes_procurement": okgz_classes_procurement,
			"delivery_time_procurement": delivery_time_procurement,
			"payment_schedule_procurement": payment_schedule_procurement,
			"payment_files_procurement": payment_files_procurement,
			"delivery_files_procurement": delivery_files_procurement
		}

		context.emit(data=contract_data)

	# response = _fetch_post(context, data, const.SEED_LINK, form_preview)  # fake request

	data["first"] += 10
	print("data => ",data)
	if data['first'] <= data["count_contracts"]:
		context.recurse(data=data)

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
