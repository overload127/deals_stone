import csv
import collections
from datetime import datetime

from django.db.models import Sum
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Gem, Customer, Deal, clear_all_table_models


CUSTOMER = 0
GEM = 1
TOTAL = 2
QUANTITY = 3
DATE = 4
DEFAULT_FIELDS = ['customer', 'item', 'total', 'quantity', 'date']


class DealLoadCSV(APIView):
    """
    Загрузка сделок из файла
    """
    parser_classes = (MultiPartParser,)

    def post(self, request, format='csv'):
        """
        Получает файл и загружает его в бд
        """
        context = dict()

        # Отчистка БД
        clear_all_table_models()

        # Проверка наличия файла
        if 'deals' not in request.FILES:
            deskription = 'does not file transfer in field "deals"'
            context['status'] = f'Error, Desc: {deskription} - ' \
                'в процессе обработки файла произошла ошибка.'

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        # декодирование данных
        file_csv = request.FILES['deals']
        decoded_file_csv = file_csv.read().decode('utf-8').splitlines()

        # Проверка на наличие всех необходимых полей
        data_deals = csv.reader(decoded_file_csv)
        fieldnames = next(data_deals)
        for field in DEFAULT_FIELDS:
            if field not in fieldnames:
                deskription = f'does not exist field "{field}" in file'
                context['status'] = f'Error, Desc: {deskription} - ' \
                    'в процессе обработки файла произошла ошибка.'

                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        # Загрузка данных в БД
        bad_status = fill_base(decoded_file_csv)

        # Если случилась ошибка то сообщим об этом
        if bad_status:
            deskription = bad_status
            context['status'] = f'Error, Desc: {deskription} - ' \
                'в процессе обработки файла произошла ошибка.'

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        context['status'] = 'OK - файл был обработан без ошибок'
        return Response(context, status=status.HTTP_200_OK)


def fill_base(decoded_file_csv):
    """
    Заполнение БД подготовленными данными
    """
    customers = dict()
    gems = dict()
    deals = list()
    errors = list()

    data_deals = csv.DictReader(decoded_file_csv)

    find_error = False
    for numline, row in enumerate(data_deals, 1):
        # Нужна проверка всех данных тут что бы
        # определить проблеммы до внесения данных в БД
        error = check_cell_correct(row)

        if error:
            find_error = True
            errors.append(str(numline))

        elif not find_error:
            try:
                gem = row[DEFAULT_FIELDS[GEM]]
                if gem not in gems:
                    gems[gem] = Gem(title=gem)

                name = row[DEFAULT_FIELDS[CUSTOMER]]
                if name not in customers:
                    customers[name] = Customer(name=name)

            except Exception:
                # Тут неплохо бы добавить логирование
                find_error = True
                errors.append(str(numline))

    # Есть ошибки? - Выходим
    if errors:
        deskription = ' '.join(errors)
        return f'line [{deskription}] is bad'

    Gem.objects.bulk_create(gems.values())
    Customer.objects.bulk_create(customers.values())

    for gem in Gem.objects.all().values('title', 'id'):
        gems[gem['title']] = gem['id']

    for customer in Customer.objects.all().values('name', 'id'):
        customers[customer['name']] = customer['id']

    data_deals = csv.reader(decoded_file_csv)
    next(data_deals)
    for numline, row in enumerate(data_deals, 1):
        try:
            deals.append(Deal(
                client_id=customers[row[CUSTOMER]],
                gem_id=gems[row[GEM]],
                total=row[TOTAL],
                quantity=row[QUANTITY],
                date=datetime.strptime(row[DATE], '%Y-%m-%d %H:%M:%S.%f')
            ))
        except Exception:
            # Тут неплохо бы добавить логирование
            find_error = True
            errors.append(str(numline))

    # Есть ошибки? - отчистка БД и выходим
    if errors:
        clear_all_table_models()
        deskription = ' '.join(errors)
        return f'line [{deskription}] is bad'

    Deal.objects.bulk_create(deals)

    return None


def check_cell_correct(row):
    """
    Проверяет полученые данные на корректность
    """
    try:
        if (row[DEFAULT_FIELDS[CUSTOMER]] is None or
           len(row[DEFAULT_FIELDS[CUSTOMER]]) < 1):
            return True

        if (row[DEFAULT_FIELDS[GEM]] is None or
           len(row[DEFAULT_FIELDS[GEM]]) < 1):
            return True

        if (row[DEFAULT_FIELDS[TOTAL]] is None or
           len(row[DEFAULT_FIELDS[TOTAL]]) < 1 or
           int(row[DEFAULT_FIELDS[TOTAL]]) < 0):
            return True

        if (row[DEFAULT_FIELDS[QUANTITY]] is None or
           len(row[DEFAULT_FIELDS[QUANTITY]]) < 1 or
           int(row[DEFAULT_FIELDS[QUANTITY]]) < 0):
            return True

        if (row[DEFAULT_FIELDS[DATE]] is None or
           len(row[DEFAULT_FIELDS[DATE]]) < 1 or
           not datetime.strptime(row[DEFAULT_FIELDS[DATE]],
                             '%Y-%m-%d %H:%M:%S.%f')):
            return True

    except Exception:
        return True

    return False


class DealTop(APIView):
    """
    Возвращает топ Х пользователей по цене
    """
    parser_classes = (MultiPartParser,)

    def get(self, request, count=5):
        """
        Возвращает топ Х пользователей по цене
        """
        context = dict()

        # Проверка корректности запроса
        if count <= 0:
            context['response'] = list()
            return Response(context, status=status.HTTP_200_OK)

        customers = list(Customer.objects.annotate(
            total_amount=Sum('deals__total')).order_by(
                '-total_amount').values(
                    'id', 'name', 'total_amount')[:count])

        id_customers = list()
        for customer in customers:
            id_customers.append(customer['id'])

        gems = list(Deal.objects.filter(
            client__id__in=id_customers).values(
                'client__id', 'gem__title').distinct())

        all_gems = list()
        gem_of_customer = dict()
        for gem in gems:
            all_gems.append(gem['gem__title'])
            if gem['client__id'] not in gem_of_customer:
                gem_of_customer[gem['client__id']] = list()
            gem_of_customer[gem['client__id']].append(gem['gem__title'])

        count_gem = collections.Counter(all_gems)

        list_users = []
        for customer in customers:
            customer_info = dict()
            customer_info['username'] = customer['name']
            customer_info['spent_money'] = customer['total_amount']

            clear_gems = list()

            for gem in gem_of_customer[customer['id']]:
                if count_gem[gem] > 1:
                    clear_gems.append(gem)

            customer_info['gems'] = clear_gems
            list_users.append(customer_info)

        context['response'] = list_users
        return Response(context, status=status.HTTP_200_OK)
