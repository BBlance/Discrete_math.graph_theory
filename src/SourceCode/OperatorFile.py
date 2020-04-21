import json
import os
import csv
import re

from PyQt5.QtCore import QPoint


class OperatorData(object):

    def save_Graph(self, filename, data):
        print(data)
        try:
            if not os.path.exists(filename):
                with open(filename, 'w', encoding='utf-8') as f:
                    for vertices, dicts in data.items():
                        f.write(str(vertices) + '\t')
                        for coordinates, vert in dicts.items():
                            f.write(str(coordinates) + '\t' + str(vert) + '\n')
                    print('写入成功')
            else:
                with open(filename, 'a', encoding='utf-8') as f:
                    for vertices, dicts in data.items():
                        f.write(str(vertices) + '\t')
                        for coordinates, vert in dicts.items():
                            f.write(str(coordinates) + '\t' + str(vert) + '\n')
                    print('写入成功')
        except Exception as e:
            print('写入错误 ==>', e)

        return filename

    def save_Json(self, filename, item):  # 将字典对象保存为Json

        # 将字典对象转化为可写入文本的字符串
        item = json.dumps(item)

        try:
            if not os.path.exists(filename):

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(item + ',\n')
                    print("写入成功")
            else:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(item + ',\n')
                    print('写入成功')
        except Exception as e:
            print('写入错误 ==>', e)

        return filename

    def save_Csv(self, keyword_list, filename, item):  # 将字典对象保存为csv
        ''':arg
        保存csv的方法
        :param keyword_list:保存文件的字段(表头)
        :param filename:: 保存文件的路径
        :param item: 要保存的字典对象
        :return:
        '''

        try:

            #  首次打开文件时，首行写入表头
            if not os.path.exists(filename):
                #  newline='' 去处空白行
                with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                    #  写字典的方法
                    writer = csv.DictWriter(csv_file, fieldnames=keyword_list)
                    #  写表头方法
                    writer.writeheader()
            # 追加内容
            #  newline='' 去处空白行，不加会出现空白行
            with open(filename, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=keyword_list)
                #  按行写入数据
                writer.writerow(item)
                print("写入成功")
        except Exception as e:
            print('写入错误 ==>', e)
            #  记录错误数据
            with open('error.txt', 'w') as f:
                f.write(json.dumps(item) + ',\n')

        return filename

    def open_Graph(self, filename):
        data = {}
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                vertices = int(line.split('\t')[0])
                coordinates = tuple(int(x) for x in line.split('\t')[1].strip(')').strip('(').split(','))
                connectionTo = line.split('\t')[2].strip('[').strip(']').split(',')
                for i in range(len(connectionTo)):
                    connectionTo[i] = connectionTo[i].replace(" ", '')
                connectionTo=[int(x) for x in connectionTo if x != '']


                data[vertices] = {coordinates: connectionTo}

        return data

    def open_Json(self, filename):

        with open(filename, 'r', encoding='UTF-8') as f:
            load_dict = json.load(f)
            print('加载文件完成')
        return load_dict

    def open_Csv(self, filename):
        load_dict = {}
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            fieldnames = next(reader)
            csv_reader = csv.DictReader(f, fieldnames=fieldnames)
            for row in csv_reader:
                for key, value in row.items():
                    load_dict[key] = value
        return load_dict

if __name__ == '__main__':
    g = OperatorData()


