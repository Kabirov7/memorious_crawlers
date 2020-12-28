import datetime


class Converter:
    @staticmethod
    def convert(date):  # 22 февраля 2019 09:00
        date_array = str(date).split()
        try:
            month = date_array[1]
            date_array[1] = _encode_month(month)
            result = _compose_date([date_array[2], date_array[1], date_array[0], date_array[3]])
            return datetime.datetime.strptime(result, "%Y-%m-%d %H:%M")
        except IndexError as ie:
            print(ie)

    @staticmethod
    def convert_date_with_dots(date):  # 22.02.2019 09:30
        date_array = str(date).split()
        try:
            split_date = date_array[0].split('.')
            year = split_date[2]
            month = split_date[1]
            day = split_date[0]
            time = date_array[1]
            result = _compose_date([year, month, day, time])
            return datetime.datetime.strptime(result, "%Y-%m-%d %H:%M")
        except IndexError as ie:
            print(ie)


def _encode_month(month):
    months = {'января': 1,
              'февраля': 2,
              'марта': 3,
              'апреля': 4,
              'мая': 5,
              'июня': 6,
              'июля': 7,
              'августа': 8,
              'сентября': 9,
              'октября': 10,
              'ноября': 11,
              'декабря': 12,
              }
    return months[month]


def _compose_date(date_array):
    return '%s-%s-%s %s' % (date_array[0], date_array[1], date_array[2], date_array[3])
