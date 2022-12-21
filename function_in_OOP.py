import csv
import re

from prettytable import PrettyTable


class Vacancy:
    """
    Класс, осуществляющий редактирование подаваемого объеката "Вакансия"
    """
    order = ['index', 'name', 'description', 'key_skills', 'experience_id',
             'premium', 'employer_name', 'salary', 'area_name', 'published_at']

    experience_weight_dictionary = {
        'Нет опыта': 1,
        'От 1 года до 3 лет': 2,
        'От 3 до 6 лет': 3,
        'Более 6 лет': 4
    }

    ru_experience = {
        'noExperience': 'Нет опыта',
        'between1And3': 'От 1 года до 3 лет',
        'between3And6': 'От 3 до 6 лет',
        'moreThan6': 'Более 6 лет',
    }

    def __init__(self, vacancy):
        """
        Задать шаблон преобразования получаемого объекта
        :param vacancy: объект "Вакансия" с элементами по ключу
        """
        self.index = 0
        self.name = self.clearHTML(vacancy['name'])
        self.description = self.shorten_string(self.clearHTML(vacancy['description']))
        self.skills = vacancy['key_skills'].split('\n')
        self.key_skills = self.shorten_string(vacancy['key_skills'])
        self.skills_length = len(self.skills)
        self.experience_id = self.ru_experience[vacancy['experience_id']]
        self.premium = 'Да' if vacancy['premium'].lower() == 'true' else 'Нет'
        self.employer_name = vacancy['employer_name']
        self.salary_class = Salary(vacancy)
        self.salary = str(self.salary_class)
        self.area_name = vacancy['area_name']
        self.published = vacancy['published_at']
        self.published_at = '{0[2]}.{0[1]}.{0[0]}'.format(vacancy['published_at'][:10].split('-'))

    @staticmethod
    def shorten_string(string):
        """
        Возвращает строку с количеством символов не более 100
        :param string: строка
        :return: строка длиной до 100 символов
        """
        return string if len(string) <= 100 else string[:100] + '...'

    @staticmethod
    def clearHTML(string):
        """
        Очищает от html тегов
        :param string: строка с html тегами
        :return: очищенная от html тегов строка

        >>> Vacancy({'salary_from': '10', 'salary_to' : '100' , 'salary_gross' : 'Без вычета налогов', 'salary_currency' : 'RUR', 'name' : 'Программист', 'description' : 'Настоящий мегамозг', 'key_skills' : 'Усидчивость', 'experience_id' : 'moreThan6', 'premium' : 'True', 'employer_name' : 'Скб Контур', 'area_name' : 'Екб', 'published_at' : '2022-05-31T17:32:31+0300'}).clearHTML('ОБЯЗАННОСТИ:')
        'ОБЯЗАННОСТИ:'
        """
        result = re.sub(r'<.*?>', '', string)
        result = re.sub(r'\s+', ' ', result)
        return result.strip()

    @property
    def salary_average(self):
        """
        Возвращает присвоенную среднюю зарабртную плату объекта, являющемуся экземляром salary_class
        :return: призвоенная средняя заработная плата
        """
        return self.salary_class.salary_average

    @property
    def salary_currency(self):
        """
        Возвращает присвоенную валюту объекта, являющемуся экземляром salary_class
        :return: призвоенная средняя заработная плата

        >>> Vacancy({'salary_from': '10', 'salary_to' : '100' , 'salary_gross' : 'Без вычета налогов', 'salary_currency' : 'RUR', 'name' : 'Программист', 'description' : 'Настоящий мегамозг', 'key_skills' : 'Усидчивость', 'experience_id' : 'moreThan6', 'premium' : 'True', 'employer_name' : 'Скб Контур', 'area_name' : 'Екб', 'published_at' : '2022-05-31T17:32:31+0300'}).salary_currency
        'RUR'
        """
        return self.salary_class.salary_currency

    @property
    def salary_from(self):
        """
        Возвращает присвоенное числовое значение заработаной платы "ОТ"
        :return: заработаная плата "ОТ"
        """
        return self.salary_class.salary_from

    @property
    def salary_to(self):
        """
        Возвращает присвоенное числовое значение заработаной платы "ДО"
        :return: заработая плата "ДО"
        """
        return self.salary_class.salary_to

    @property
    def experience_weight(self):
        """
        Возвращает опыт работы
        :return: опыт работы
        """
        return self.experience_weight_dictionary[self.experience_id]

    def get_list(self):
        """
        Формирует лист со значениями объекта order класса Vacancy по ключу значения
        :return: лист со значениями объекта order класса Vacancy по ключу значения
        """
        return [getattr(self, key) for key in self.order]


class Salary:
    """
    Взаимодействие с заработной платой
    """
    en_ru_valuta = {
        'AZN': 'Манаты',
        'BYR': 'Белорусские рубли',
        'EUR': 'Евро',
        'GEL': 'Грузинский лари',
        'KGS': 'Киргизский сом',
        'KZT': 'Тенге',
        'RUR': 'Рубли',
        'UAH': 'Гривны',
        'USD': 'Доллары',
        'UZS': 'Узбекский сум'
    }

    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, vacancy):
        """
        Задает шаблон преобразования экземпляров о финансах получаемого объекта "Вакансия"
        :param vacancy: объект "Вакансия" с элементами по ключу
        """
        self.salary_from = int(float(vacancy['salary_from']))
        self.salary_to = int(float(vacancy['salary_to']))
        self.salary_gross = 'Без вычета налогов' if vacancy['salary_gross'].lower() == 'true' else 'С вычетом налогов'
        self.salary_currency = vacancy['salary_currency']
        self.salary_average = Salary.currency_to_rub[self.salary_currency] * (self.salary_from + self.salary_to) / 2

    def __str__(self):
        """
        Объединение и преобразование в строковое значение экземлеров о финансах в один элемент
        :return: Строка вида: {зарплата от} - {зарплата до} {валөта на русском} {информация о налогах}
        """
        return '{0:,} - {1:,} ({2}) ({3})'\
            .format(self.salary_from, self.salary_to,
                    Salary.en_ru_valuta[self.salary_currency], self.salary_gross).replace(',', ' ')


class DataSet:
    """
    Класс формирования таблицы
    """
    ru_en_keys_dictionary = {
        'Описание': 'description',
        'Навыки': 'skills_length',
        'Оклад': 'salary_average',
        'Дата публикации вакансии': 'published',
        'Опыт работы': 'experience_weight',
        'Премиум-вакансия': 'premium',
        'Идентификатор валюты оклада': 'salary_currency',
        'Название': 'name',
        'Название региона': 'area_name',
        'Компания': 'employer_name',
    }

    conditions_to_sort = {
        'Навыки': lambda vacancy, value: all([skill in vacancy.skills for skill in value.split(', ')]),
        'Оклад': lambda vacancy, value: vacancy.salary_from <= float(value) <= vacancy.salary_to,
        'Дата публикации вакансии': lambda vacancy, value: vacancy.published_at == value,
        'Опыт работы': lambda vacancy, value: vacancy.experience_id == value,
        'Премиум-вакансия': lambda vacancy, value: vacancy.premium == value,
        'Идентификатор валюты оклада': lambda vacancy, value: Salary.en_ru_valuta[vacancy.salary_currency] == value,
        'Название': lambda vacancy, value: vacancy.name == value,
        'Название региона': lambda vacancy, value: vacancy.area_name == value,
        'Компания': lambda vacancy, value: vacancy.employer_name == value
    }

    def __init__(self, file_name, filter_param, sort_param, sort_reverse, sort_range):
        """
        Задает шаблон преобразования экземпляров о финансах получаемого объекта "Вакансия"
        :param file_name: название файла
        :param filter_param: параметр фильтрации
        :param sort_param: параметр сортировки
        :param sort_reverse: параметр вывода таблицы в обратном порядке (да/нет)
        :param sort_range: промежуток вывода строк таблицы
        """
        self.file_name = file_name
        self.filter_param = filter_param
        self.sort_param = sort_param
        self.sort_reverse = sort_reverse
        self.sort_range = sort_range
        self.vacancies_objects = []

    def csv_reader(self):
        """
        Проверка файла на пустоту и наличие вакансий.
        При их наличи формируется словарь вакансий, где ключ - наименование столбца,
        экземпляр вакансии, стоящий в этом же столбце, - значение ключа
        :return: Словарь, у которого наименование столбца - ключ;
        экземпляр вакансии, стоящий в этом же столбце, - значение ключа
        """
        header = []
        with open(self.file_name, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    header = row
                    csv_header_length = len(row)
                elif '' not in row and len(row) == csv_header_length:
                    self.vacancies_objects.append(Vacancy(dict(zip(header, row))))

        if len(self.vacancies_objects) == 0:
            if len(header) == 0:
                print('Пустой файл')
            else:
                print('Нет данных')
            exit()

    def get_rows(self):
        """
        Получить список строк для вакансий в экзмпляре vacancies_objects
        :return: список строк для вакансий в экзмпляре vacancies_objects
        """
        return [vacancy.get_list() for vacancy in self.vacancies_objects]

    def filter_rows(self):
        """
        Фильтрцет строки по задаваемому параметру фильтрации
        :return: список отфильтрованных строк по задаваемому значению
        """
        if len(self.filter_param) == 0:
            return

        self.vacancies_objects \
            = list(filter(lambda vacancy: self.conditions_to_sort[self.filter_param[0]](vacancy, self.filter_param[1]),
                          self.vacancies_objects))

    def sort_rows(self):
        """
        Сортирует вакансии по задаваемым параметрам, а также реверсирует список вакансий
        :return: новый vacancies_objects, отсортированный по новым условиям
        """
        if self.sort_param != '':
            self.vacancies_objects\
                .sort(key=lambda a: getattr(a, DataSet.ru_en_keys_dictionary[self.sort_param]),
                      reverse=self.sort_reverse)
        elif self.sort_param == '' and self.sort_reverse:
            self.vacancies_objects.reverse()

    def get_range(self):
        """
        Формируется экземпляр vacancies_objects класса DataSet из вакансий определенного промежутка,
        вводимого пользователем
        :return: фрагмент таблицы
        """
        vacancies_temp = []
        length = len(self.sort_range)
        for index, vacancy in enumerate(self.vacancies_objects):
            if (length > 1 and self.sort_range[0] <= index < self.sort_range[1]) or \
                    (length == 1 and self.sort_range[0] <= index) or length == 0:
                vacancy.index = index + 1
                vacancies_temp.append(vacancy)
        self.vacancies_objects = vacancies_temp


class InputConnect:
    """
    Класс формирования вводимых значений
    """
    table_header = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Оклад',
                    'Название региона', 'Дата публикации вакансии']

    def __init__(self):
        """
        Задать шаблон преобазования вводимых значений
        """
        self.errors = []
        self.file_name = input('Введите название файла: ')
        self.filter_param = self.parse_filter_param(input('Введите параметр фильтрации: '))
        self.sort_param = self.parse_sort_param(input('Введите параметр сортировки: '))
        self.sort_reverse = self.parse_sort_reverse(input('Обратный порядок сортировки (Да / Нет): '))
        self.sort_range = self.parse_sort_range(input('Введите диапазон вывода: '))
        self.table_fields = self.parse_table_fields(input('Введите требуемые столбцы: '))

        if len(self.errors) != 0:
            print(self.errors[0])
            exit()

        data_set = DataSet(self.file_name, self.filter_param, self.sort_param, self.sort_reverse, self.sort_range)
        data_set.csv_reader()
        data_set.filter_rows()
        data_set.sort_rows()
        data_set.get_range()

        rows = data_set.get_rows()

        if len(rows) == 0:
            print('Ничего не найдено')
        else:
            table = PrettyTable(align='l', field_names=InputConnect.table_header, max_width=20, hrules=1)
            table.add_rows(rows)
            print(table.get_string(fields=self.table_fields))

    def parse_filter_param(self, filter_param):
        """
        Учитывание всех случаев параметра фильтра
        :param filter_param: параметр фильтрации таблицы
        :return: только те вакансии, которые имеют введенный параметр фильтрации
        """
        if filter_param == '':
            return []

        if ': ' not in filter_param:
            self.errors.append('Формат ввода некорректен')
            return []

        filter_param = filter_param.split(': ')

        if filter_param[0] not in list(DataSet.conditions_to_sort.keys()):
            self.errors.append('Параметр поиска некорректен')
            return []

        return filter_param

    def parse_sort_param(self, sort_param):
        """
        Проверяет входит ли сортируемый параметр в допустимый диапазон значений
        наименований столбцов и пустого значения строки
        :param sort_param: параметр, относительно которого будут сортироваться столбцы
        :return: отсортированная по задаваемым значениям поля таблица
        """
        if sort_param not in InputConnect.table_header + ['']:
            self.errors.append('Параметр сортировки некорректен')
        return sort_param

    def parse_sort_reverse(self, sort_reverse):
        """
        Анализирует вводимые запрос на вывод таблицы в обратном порядке
        :param sort_reverse: переменная, в которую подается запрос
        на вывод таблицы в нормальной последовательности/обратной
        :return: True/False
        """
        if sort_reverse not in ('', 'Да', 'Нет'):
            self.errors.append('Порядок сортировки задан некорректно')
        return True if sort_reverse == 'Да' else False

    def parse_sort_range(self, sort_range):
        """
        Относительно начального и конечного введенных значений диапозона вывода
        формируется лист нумерации строк от начального элемента до конечного - 1 элемента
        :param sort_range: диапазон вывода
        :return: лист нумерации строк от начального до конечного - 1 элементов
        """
        return [] if sort_range == '' else [int(limit) - 1 for limit in sort_range.split()]

    def parse_table_fields(self, table_fields):
        """
        Анализирует наименования выводимых колонок подаваемой таблицы и выводит таблицу целиком,
        если вводимые поля отсутсвуют, или создает новую таблицу с данными полями, если они были поданы
        :param table_fields: таблица с запрашиваемыми наименованиями столбцов
        :return: таблица целиком или талица с запрашиваемыми наименованиями колонок
        """
        return InputConnect.table_header if table_fields == '' else ['№'] + [a for a in table_fields.split(', ')
                                                                             if a in InputConnect.table_header]


if __name__ == '__main__':
    InputConnect()


