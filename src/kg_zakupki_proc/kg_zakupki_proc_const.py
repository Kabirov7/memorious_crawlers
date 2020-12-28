MAIN_PAGE = 'http://zakupki.gov.kg/'
START_PAGE = 1

SEED_LINK = 'http://zakupki.gov.kg/popp/view/order/single_source_procurement.xhtml'

VIEWSTATE_KEY = 'javax.faces.ViewState'

DEFAULT_OFFSET = 0

CONTRACTS_IDS_FOR_REQUEST_FORM = "//tr/td[2]//@onclick"
CONTRACT_NUMBER_FORM = "string(//div[@class='col-2 report-head']/input/@name)"

X_PATH_CONTRACT_NUMBER = "//tr/td[2]/a/text()"
X_PATH_PROCURING_ORGANIZATION = "//tr/td[3]//text()"
X_PATH_PROVIDER = "//tr/td[4]//text()"
X_PATH_TYPE = "//tr/td[5]//text()"
X_PATH_DATE = "//tr/td[6]//text()"

LOT_INFO = "//span[@id='lot-info']//div[@class='col-4 report-head']//text()"

product_info = "//span[@id='product-info']//thead/tr/th/text()" ### len may be 6 or 8


#Contract details
OKGZ_CLASS = "//span[@id='product-info']//tbody/tr/td[1]//text()"# if len product_info is 6
OKGZ_UNIT = "//span[@id='product-info']//tbody/tr/td[2]//text()"# if len product_info is 6
OKGZ_COUNT = "//span[@id='product-info']//tbody/tr/td[3]//text()"# if len product_info is 6
OKGZ_PRICE_UNIT_ITEM = "//span[@id='product-info']//tbody/tr/td[4]//text()"# if len product_info is 6
OKGZ_PRICE_SUM = "//span[@id='product-info']//tbody/tr/td[5]//text()"# if len product_info is 6
OKGZ_SPECIFICATION_6 = "//span[@id='product-info']//tbody/tr/td[6]//text()"# if len product_info is 6

OKGZ_BRAND_8 = "//span[@id='product-info']//tbody/tr/td[6]//text()"
OKGZ_MADE_IN_8 = "//span[@id='product-info']//tbody/tr/td[7]//text()"
OKGZ_SPECIFICATION_8 = "//span[@id='product-info']//tbody/tr/td[8]//text()"


#Delivery times
schedule_info = "//span[@id='schedule-info']//thead[@id='table_head']/tr/th//text()" # only 6

DELIVERY_NUMBER = "//span[@id='schedule-info']//tbody/tr/td[1]//text()"
DELIVERY_START_DATE = "//span[@id='schedule-info']//tbody/tr/td[2]//text()"
DELIVERY_FINISH_DATE = "//span[@id='schedule-info']//tbody/tr/td[3]//text()"
DELIVERY_ADRES_AND_PLACE = "//span[@id='schedule-info']//tbody/tr/td[4]//text()"
DELIVERY_CONDITION_PAYMENT = "//span[@id='schedule-info']//tbody/tr/td[5]//text()"
DELIVERY_DOC_NAME = "//ol[@id='table:0:j_idt156_list']//a/text()"
DELIVERY_DOC_URL = "//ol[@id='table:0:j_idt156_list']//a/@href"

#payment schedule
GRAPHIC_NUMBER = "//span[@id='delivery-info']//tbody/tr/td[1]//text()"
GRAPHIC_START_DATE = "//span[@id='delivery-info']//tbody/tr/td[2]//text()"
GRAPHIC_FINISH_DATE = "//span[@id='delivery-info']//tbody/tr/td[3]//text()"
GRAPHIC_PAYMENT_TYPE = "//span[@id='delivery-info']//tbody/tr/td[4]//text()"
GRAPHIC_CONDITION_PAYMENT = "//span[@id='delivery-info']//tbody/tr/td[5]//text()"
GRAPHIC_DOC_NAME = "//ol[@id='tablePayment:0:j_idt172_list']//a/text()"
GRAPHIC_DOC_URL = "//ol[@id='tablePayment:0:j_idt172_list']//a/@href"