# !/usr/bin/env python
# *- coding: utf-8 -*-
import sqlalchemy

class Banco:
    def __init__(self, config):
        self.config = config


    def connect(self):
        self.engine = sqlalchemy.create_engine(
            'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(**self.config)
        )
        pass

    def disconnect(self):
        pass

    def insert_query(self):
        pass

    def update_query(self):
        pass

    def remove_query(self):
        pass

    def get_data(self):
        pass
