import datetime

MAIN_PAGE = 'https://budget.okmot.kg'

LINK_INCOMES = 'http://budget.okmot.kg/ru/incomes'
LINK_EXPENSES = 'http://budget.okmot.kg/ru/expenses'

VIEWSTATE_KEY = 'If-None-Match'

DISTRICT = "//span[@class='select2-results']/ul[@id='select2-country-k8-results']/li[@class='select2-results__option select2-results__option--highlighted']/text()"

QUERY_INN_MINJUST = "SELECT inn FROM kg_minjust WHERE inn <> ''"

MINJUST_HOST = "postgresgoszakup.postgres.database.azure.com"
MINJUST_DBNAME = 'goszakup_dev'
MINJUST_USER = 'readonly@postgresgoszakup'
MINJUST_PASSWORD = 'readonly'

