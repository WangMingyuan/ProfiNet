# -*- coding: utf-8 -*-

"""
Author: YJ
Email: yj1516268@outlook.com
Created Date: 2018-07-16 15:46:24

"""

import toml
import snap7
from snap7 import util


class PLC:
    """Read Data : Real, Integer, Bool"""
    def __init__(self):
        """
        Connect to snap7-server

        """
        toml_path = "./resource/conf/conf.toml"
        self.conf = conf = toml.load(toml_path)

        # db num
        self.db = conf['conf'].get('db_num', 50)

        # start & end num
        self.real_start = real_start = conf['Real']['offset'][0]
        self.real_end = real_end = conf['Real']['offset'][-1]

        self.int_start = int_start = conf['Integer']['offset'][0]
        self.int_end = int_end = conf['Integer']['offset'][-1]

        self.bool_start = bool_start = conf['Bool']['offset'][0]
        self.bool_end = bool_end = conf['Bool']['offset'][-1]

        # data size
        self.real_size = real_end - real_start + 4
        self.int_size = int_end - int_start + 2
        self.bool_size = bool_end - bool_start + 0.1

        # create client
        self.client = snap7.client.Client()
        self.client.connect(
            conf['conf'].get('host', "10.7.93.84"),
            conf['conf'].get('rack', 0),
            conf['conf'].get('slot', 2),
            conf['conf'].get('port', 102),
        )

    def read_Real(self):
        """
        Read Real type Data from snap7-server

        :param start: 开始的下标
        :param size: 每一组数据的大小
        """
        data = self.client.db_read(self.db, self.real_start, self.real_size)

        real_list = []
        for index in range(self.real_start, self.real_end + 1, 4):
            real_data = util.get_real(data, index)
            real_list.append(real_data)

        print("real_list = {}\n".format(real_list))

    def read_Integer(self):
        """
        Read Integer type Data from snap7-server

        :param start: 开始的下标
        :param size: 每一组数据的大小
        """
        data = self.client.db_read(self.db, self.int_start, self.int_size)

        int_list = []
        for index in range(self.int_start, self.int_end + 1, 2):
            int_data = util.get_int(data, index)
            int_list.append(int_data)

        print("int_list = {}\n".format(int_list))

    def read_Bool(self):
        """
        Read Bool type Data from snap7-server

        :param start: 开始的下标
        :param size: 每一组数据的大小
        """
        data = self.client.db_read(self.db, self.bool_start, self.bool_size)

        bool_list = []
        for be in range(self.bool_start, self.bool_end + 1):
            for bl in range(0, 8):
                bool_data = util.get_bool(data, byte_index=be, bool_index=bl)
                bool_list.append(bool_data)

        print("bool_list = {}".format(bool_list))


if __name__ == "__main__":
    plc = PLC()
