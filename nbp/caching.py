# -*- coding: utf-8 -*-
import os
from os.path import join as pathjoin, exists, basename


def mkdir_p(*path):
    try:
        os.makedirs(pathjoin(*path))
    except OSError, exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


class Cache(object):
    def __init__(self, dir_path, file_name):
        self.dir_path = dir_path
        self.file_name = file_name

    @property
    def file_path(self):
        return pathjoin(self.dir_path, self.file_name)

    def dir_exists(self):
        return exists(self.dir_path)

    def file_exists(self):
        return exists(self.file_path)

    def create_dir(self):
        mkdir_p(self.dir_path)

    def save(self, data):
        with open(self.file_path, "w") as f:
            f.write(data.read())

    def open(self):
        return open(self.file_path, "r")


def get_cache(cache_file_path):
    file_path = cache_file_path
    file_name = basename(file_path)
    dir_path = file_path.replace(file_name, '')
    return Cache(dir_path, file_name)
