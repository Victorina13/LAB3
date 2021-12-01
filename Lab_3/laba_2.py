import re
import json
import argparse
from tqdm import tqdm


class Node:
    """Объект класса Node обрабатывает запись о пользователе.
    :parameter
    node:dict
    """
    node: dict

    def __init__(self, _node):
        self.node = _node.copy()

    def check_telephone(self) -> bool:
        """Выполняет проверку на валидность поля telephone
        Returns
        -------
        True, если номер телефона валидный, иначе False """

        pattern = "^\\+7-\\(\\d{3}\\)-\\d{3}(-\\d{2}){2}"
        if re.match(pattern, self.node["telephone"]):
            return True
        return False

    def check_weight(self) -> bool:
        """Выполняет проверку на валидность поля weight
        Returns
        -------
        True, если вес валидный,иначе False """

        pattern = "^([1-9]|[1-9][0-9]|1[0-9][1-9]|2[0-5][0-9])$"
        if re.match(pattern, str(self.node["weight"])):
            return True
        return False

    def check_inn(self) -> bool:
        """Выполняет проверку на валидность поля inn
        Returns
        -------
        True, если ИНН валидный,иначе False """

        pattern = "^[0-9]{12}$"
        if re.match(pattern, self.node["inn"]):
            return True
        return False

    def check_passport_series(self) -> bool:
        """Выполняет проверку на валидность поля passport_series
        Returns
                -------
                True, если серия паспорта валидная,иначе False"""
        pattern = "\\d{2} \\d{2}"
        if re.match(pattern, self.node["passport_series"]):
            return True
        return False

    def check_university(self) -> bool:
        """Выполняет проверку на валидность поля university
        Returns
        -------
        True, если название университета валидное,иначе False"""

        pattern = "^.*(?:СПбГУ|МФТИ|МГУ|МГТУ|им\\.|[Уу]нивер|[Аа]кадем|[Ии]нстит|[Нн]ационал).*$"
        if re.match(pattern, self.node["university"]):
            return True
        return False

    def check_work_experience(self) -> bool:
        """Выполняет проверку на валидность поля work_experience
        Returns
        -------
        True, если стаж работы валидный,иначе False"""

        pattern = "^([1-9]|[1-6][0-9])$"
        if re.match(pattern, str(self.node["work_experience"])):
            return True
        return False

    def check_academic_degree(self) -> bool:
        """Выполняет проверку на валидность поля academic_degree
        Returns
        -------
        True, если ученая степень валидная,иначе False"""

        pattern = "Доктор наук|Магистр|Кандидат наук|Специалист|Бакалавр"
        if re.match(pattern, self.node["academic_degree"]):
            return True
        return False

    def check_worldview(self) -> bool:
        """Выполняет проверку на валидность поля worldview
        Returns
        -------
        True, если мировоззрение валидное,иначе False"""

        pattern = "^.+(?:изм|ство|ам)$"
        if re.match(pattern, self.node["worldview"]):
            return True
        return False

    def check_address(self) -> bool:
        """Выполняет проверку на валидность поля address
         Returns
         -------
        True, если адрес валидный,иначе False"""

        pattern = "^[\\wа-яА-Я\\s\\.\\d-]* \\d+$"
        if re.match(pattern, self.node["address"]):
            return True
        return False


class Validator:
    """Объект класса Validator проверяет записи файла на валидность.
       Attributes
       ----------
       data : list
       Список записей """
    data: list

    def __init__(self, _data):
        self.data = []
        tmp = json.load(open(_data, encoding="windows-1251"))
        for i in tmp:
            self.data.append(Node(i.copy()))

    def parse(self, index) -> dict:
        """Выполняет валидацию записи по ее ключу."""
        res = {
            "telephone": self.data[index].check_telephone(),
            "weight": self.data[index].check_weight(),
            "inn": self.data[index].check_inn(),
            "passport_series": self.data[index].check_passport_series(),
            "university": self.data[index].check_university(),
            "work_experience": self.data[index].check_work_experience(),
            "academic_degree": self.data[index].check_academic_degree(),
            "worldview": self.data[index].check_worldview(),
            "address": self.data[index].check_address()
        }
        return res.copy()

    def count_incorrect_nodes(self) -> int:
        """Считает число некорректных записей"""
        count_incorrect = 0
        for i in tqdm(range(len(self.data)),
                      desc="Подсчёт некорректных записей",
                      ncols=100):
            if (False in self.parse(i).values()):
                count_incorrect += 1
        return count_incorrect

    def count_correct_nodes(self) -> int:
        """Считает число корректных записей"""
        count_correct = 0
        for i in tqdm(range(len(self.data)),
                      desc="Подсчёт корректных записей",
                      ncols=100):
            if not (False in self.parse(i).values()):
                count_correct += 1
        return count_correct

    def res_file(self, output_name):
        """Записывает корректные записи в файл."""
        tmp = []
        for i in range(len(self.data)):
            if not (False in self.parse(i).values()):
                tmp.append(self.data[i].node.copy())
        json.dump(tmp, open(output_name, "w", encoding="windows-1251"),
                  ensure_ascii=False, sort_keys=False, indent=4)

    def count_arg(self):
        """Считает число некорректных полей
        Returns
        -------
        res
        Список с количеством некорректных данных"""
        res = []
        count_telephone = 0
        count_weight = 0
        count_inn = 0
        count_passport = 0
        count_university = 0
        count_work_experience = 0
        count_academic_degree = 0
        count_worldview = 0
        count_address = 0
        for i in range(len(self.data)):
            if not self.data[i].check_telephone():
                count_telephone += 1
            if not self.data[i].check_weight():
                count_weight += 1
            if not self.data[i].check_inn():
                count_inn += 1
            if not self.data[i].check_passport_series():
                count_passport += 1
            if not self.data[i].check_university():
                count_university += 1
            if not self.data[i].check_work_experience():
                count_work_experience += 1
            if not self.data[i].check_academic_degree():
                count_academic_degree += 1
            if not self.data[i].check_worldview():
                count_worldview += 1
            if not self.data[i].check_address():
                count_address += 1

        res.append(count_telephone)
        res.append(count_weight)
        res.append(count_inn)
        res.append(count_passport)
        res.append(count_university)
        res.append(count_work_experience)
        res.append(count_academic_degree)
        res.append(count_worldview)
        res.append(count_address)
        return res


parser = argparse.ArgumentParser()
parser.add_argument("-input", type=str, default="38.txt")
parser.add_argument("-output", type=str, default="result.txt")
args = parser.parse_args()
input_path = args.input
output_path = args.output


val = Validator(input_path)
valid = val.count_correct_nodes()
invalid = val.count_incorrect_nodes()
print("Всего корректных записей в файле: ", valid)
print("Всего некорректных записей в файле: ", invalid)
val.res_file(output_path)
res = val.count_arg()
print("Количество некорректных записей 'telephone':", res[0])
print("Количество некорректных записей 'weight':", res[1])
print("Количество некорректных записей 'inn':", res[2])
print("Количество некорректных записей 'passport_series':", res[3])
print("Количество некорректных записей 'university':", res[4])
print("Количество некорректных записей 'work_experience':", res[5])
print("Количество некорректных записей 'academic_degree':", res[6])
print("Количество некорректных записей 'worldview':", res[7])
print("Количество некорректных записей 'address':", res[8])
