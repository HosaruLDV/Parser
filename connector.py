import json
import os

cwd = os.getcwd()
class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    def __init__(self, df):
        self.__data_file = os.path.join(cwd, df)
        self.__connect()
    # @property
    # def data_file(self):
    #     pass
    #
    # @data_file.setter
    # def data_file(self, value):
    #     # тут должен быть код для установки файла
    #     self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        try:
            fp = open(self.__data_file, 'r', encoding='utf-8')
        except FileNotFoundError:
            print(f'Саздание {self.__data_file}')
            fp = open(self.__data_file,'w', encoding='utf-8')
            data = []
            json.dump(data, fp)
        else:
            data = json.load(fp)
            print(data)
        finally:
            fp.close()


    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        fp = open(self.__data_file, 'r', encoding='utf-8')
        r_data = json.load(fp)
        r_data.append(data)
        fp.close()

        fp = open(self.__data_file,'w', encoding='utf-8')
        json.dump(r_data, fp)
        fp.close()

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        fp = open(self.__data_file,'r', encoding='utf-8')
        data = json.load(fp)
        fp.close()

        if not len(query): return data

        query_data = []

        for k in data[query.keys()]:
            if data[k] == query.values():
                query_data.append(data[k])

        return query_data

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not len(query): return

        fp = open(self.__data_file,'r', encoding='utf-8')
        data = json.load(fp)
        fp.close()
        cntr = 0

        for k in data:
            if k.get(list(query.keys())[0]) == list(query.values())[0]:
                del data[cntr]

            cntr += 1

        fp = open(self.__data_file,'w', encoding='utf-8')
        json.dump(data, fp)
        fp.close()

        return


if __name__ == '__main__':
    df = Connector('df.json')

    data_for_file = {'id': 1, 'title': 'tet'}

    df.insert(data_for_file)
    data_from_file = df.select(dict())
    assert data_from_file == [data_for_file]

    df.delete({'id':1})
    data_from_file = df.select(dict())
    assert data_from_file == []