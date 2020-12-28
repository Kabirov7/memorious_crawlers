DEFAULT_OFFSET = 0
ROWS_NUMBER = 1000
TENDER_NUMBERS = 100

MAIN_URL = 'http://zakupki.gov.kg/popp'
LIST_URL = 'http://zakupki.gov.kg/popp/view/order/list.xhtml'
HOME_URL = 'http://zakupki.gov.kg/popp/home.xhtml'
VIEW_URL = 'http://zakupki.gov.kg/popp/view/order/view.xhtml'
CONTEST_URL = 'http://zakupki.gov.kg/popp/view/contest.xhtml'

TENDER_LINK = 'http://zakupki.gov.kg/popp/view/order/view.xhtml?id='
VIEWSTATE_KEY = 'javax.faces.ViewState'

# LINKS_FORM = {
#     'javax.faces.partial.ajax': 'true',
#     'javax.faces.source': 'j_idt106:j_idt107:table',
#     'javax.faces.partial.execute': 'j_idt106:j_idt107:table',
#     'javax.faces.partial.render': 'j_idt106:j_idt107:table',
#     'javax.faces.behavior.event': 'page',
#     'javax.faces.partial.event': 'page',
#     'j_idt106:j_idt107:table_pagination': 'true',
#     'j_idt106:j_idt107:table_first': '',
#     'j_idt106:j_idt107:table_rows': ROWS_NUMBER,
#     'j_idt106:j_idt107:table_skipChildren': 'true',
#     'j_idt106:j_idt107:table_encodeFeature': 'true',
#     'j_idt106': 'j_idt106',
#     'j_idt106:j_idt107:table_selection': '',
#     'j_idt106:j_idt107_activeIndex': '0',
#     'javax.faces.ViewState': ''
# }
# LINKS_OFFSET_KEY = 'j_idt106:j_idt107:table_first'
# LINKS_ROWS_NUMBER_KEY = 'j_idt106:j_idt107:table_rows'

TENDER_NUMBERS_PATH = "//tr[@role='row']/@data-rk"

SEARCH_FIELD_KEY = 'tv1:search-field'

# TENDER_NUMBERS_TABLE_NAME = env.get('TENDER_NUMBERS_TABLE_NAME')
# TENDER_NUMBERS_COLUMN_NAME = env.get('TENDER_NUMBERS_COLUMN_NAME')
# DB_PARAMS = {
#     user: env.get('USER'),
#     password: env.get('PASSWORD'),
#     host: env.get('HOST'),
#     port: env.get('PORT'),
#     database: env.get('DATABASE')
# }

# SEARCH_FORM = {
#     'tv1:j_idt68': 'tv1:j_idt68',
#     SEARCH_FIELD_KEY: '',
#     'tv1:j_idt71': 'Найти',
# }

# RESULTS_FORM = {
#     'j_idt104': 'j_idt104',
#     'j_idt104:j_idt105:table_rppDD': '10',
#     'j_idt104:j_idt105:table_selection': '',
#     'j_idt104:j_idt105_activeIndex': '0',
#     'j_idt104:j_idt105:table:0:evaluation_findings': 'j_idt104:j_idt105:table:0:evaluation_findings'
# }

# PRODUCTS_ROW_EXPANSION_KEY = 'j_idt71:lotsTable_expandedRowIndex'
#
# PRODUCT_LOTS_FORM = {
#     'javax.faces.source': 'j_idt71:lotsTable',
#     'javax.faces.partial.execute': 'j_idt71:lotsTable',
#     'javax.faces.partial.render': 'j_idt71:lotsTable',
#     'j_idt71:lotsTable': 'j_idt71:lotsTable',
#     'j_idt71:lotsTable_rowExpansion': 'true',
#     PRODUCTS_ROW_EXPANSION_KEY: '0',
#     'j_idt71:lotsTable_encodeFeature': 'true',
#     'j_idt71:lotsTable_skipChildren': 'true'
# }

# SERVICES_ROW_EXPANSION_KEY = 'j_idt71:lotsTable2_expandedRowIndex'
#
# SERVICE_LOTS_FORM = {
#     'javax.faces.source': 'j_idt71:lotsTable2',
#     'javax.faces.partial.execute': 'j_idt71:lotsTable2',
#     'javax.faces.partial.render': 'j_idt71:lotsTable2',
#     'j_idt71:lotsTable2': 'j_idt71:lotsTable2',
#     'j_idt71:lotsTable2_rowExpansion': 'true',
#     SERVICES_ROW_EXPANSION_KEY: '0',
#     'j_idt69': 'j_idt69',
#     'j_idt71:lotsTable2_encodeFeature': 'true',
#     'j_idt71:lotsTable2_skipChildren': 'true'
# }
#
# LOTS_FORM = {
#     'javax.faces.partial.ajax': 'true',
#     'j_idt69': 'j_idt69',
#     'j_idt71:tender-doc-explanation-table_rppDD': '10',
#     'j_idt71:tender-doc-explanation-table_selection': '',
#     'j_idt71_activeIndex': '0',
# }

# PARTICIPANTS_FORM = {
# #     'j_idt69': 'j_idt69',
# #     'j_idt71:tender-doc-explanation-table_rppDD': '10',
# #     'j_idt71:tender-doc-explanation-table_selection': '',
# #     'j_idt71_activeIndex': '0',
# #     'j_idt71:contest': 'j_idt71:contest'
# # }
