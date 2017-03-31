import os  # ,setacl, wget

import os
import logger
import operations_setacl as acl
import shutil
from operations_process_controller import RegController as regc, ReturnCode as rc

from enum import Enum

_logger = logger.Logger().get_logger('operations_io')


class RegValue(object):
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = os.path.normpath(value)

    @property
    def type_(self):
        return self._type

    @type_.setter
    def value_type(self, value):
        assert (value in self.Type or value is None)
        self._type = value

    def __init__(self, value=None, type_=None, data=None, path=None):
        self.path = path
        self.type_ = type_
        self.value = value
        self.data = data

    def __repr__(self):
        return "{}{}:{!s}[{!s}]{!s}".format(str(self.__class__), self.path, self.value,
                                            self.type_.value if self.type_ else '', self.data)


class IOOperatorBase(object):
    @classmethod
    def _normpath(cls, path):
        return os.path.normpath(path)

    @classmethod
    def find_parent(cls, path):
        raise NotImplementedError()

    @classmethod
    def list(cls, path):
        raise NotImplementedError()

    @classmethod
    def add_container(cls, path, force=False):
        raise NotImplementedError()

    @classmethod
    def add_object(cls, path, object, force=False):
        raise NotImplementedError()

    @classmethod
    def rem_container(cls, path, force=False):
        raise NotImplementedError()

    @classmethod
    def rem_object(cls, path, object, force=False):
        raise NotImplementedError()

    @classmethod
    def exists(cls, path):
        raise NotImplementedError()

    @classmethod
    def copy(cls, source, dest):
        raise NotImplementedError()

    @classmethod
    def lock(cls, path):
        raise NotImplementedError()

    @classmethod
    def unlock(cls, path):
        raise NotImplementedError()

    @classmethod
    def placeholder(cls, path, force=False):
        path = cls._normpath(str(path))
        if cls.rem_container(path, force) is True:
            if cls.add_container(path, force) is True:
                return True
        return False


class FilesystemOperator(IOOperatorBase):
    @classmethod
    def find_parent(cls, path):
        path = cls._normpath(str(path))
        name = True

        while name:
            path, name = os.path.split(path)

            if os.path.isdir(path):
                return path
        return None

    @classmethod
    def add_container(cls, path, force=False):
        def subexec(path):
            try:
                os.makedirs(path)
                return os.path.isdir(path)
            except:
                return False  # todo finnaly

        path = cls._normpath(str(path))

        if os.path.isdir(path):
            _logger.warning('{} Directory exists, skipping.'.format(path))
            return True
        if not subexec(path):
            if force:
                parent = cls.find_parent(path)
                if parent:
                    acl1 = acl.Templates.file_unlock(parent)
                    acl1.execute()
                    subexec(path)

        if os.path.isdir(path):
            _logger.info('"{}" has been successfully created.'.format(path))
            return True
        _logger.info('"{}" Directory not created.'.format(path))
        return False

    @classmethod
    def _rem(cls, path, force=False, op_func=None, exists_func=None):
        def subexec(path):
            try:
                op_func(path)
                return not exists_func(path)
            except:  # todo finnaly
                return False

        path = cls._normpath(str(path))

        if not exists_func(path):
            _logger.warning('{} Directory not found, skipping.'.format(path))
            return True
        if not subexec(path):
            if force:
                acl1 = acl.Templates.file_unlock(path)
                acl1.execute()
                if not subexec(path):
                    parent = cls.find_parent(path)
                    if parent:
                        acl2 = acl.Templates.file_unlock(parent)
                        acl2.execute()
                        subexec(path)

        if not exists_func(path):
            _logger.info('"{}" has been successfully removed.'.format(path))
            return True
        _logger.info('"{}" Directory not removed.'.format(path))
        return False

    @classmethod
    def rem_container(cls, path, force=False):
        return cls._rem(path=path, force=force, op_func=shutil.rmtree, exists_func=os.path.isdir)

    @classmethod
    def rem_object(cls, path, object, force=False):
        return cls._rem(path=path, force=force, op_func=os.remove, exists_func=os.path.isfile)

    @classmethod
    def exists(cls, path):
        return os.path.exists(path)

    @classmethod
    def lock(cls, path, recursive=False):
        path = cls._normpath(str(path))
        acl1 = acl.Templates.file_lock(path, recursive)
        acl1.execute()

    @classmethod
    def unlock(cls, path, recursive=True):
        path = cls._normpath(str(path))
        acl1 = acl.Templates.file_unlock(path, recursive)
        acl1.execute()


class RegOperator(IOOperatorBase):
    @classmethod
    def find_parent(cls, path):
        path = cls._normpath(str(path))
        name = True

        while name:
            path, name = os.path.split(path)

            if cls.exists(path):
                return path
        return None

    @classmethod
    def list(cls, path, value=None):
        query1 = regc.query(path, value)
        if not isinstance(query1, rc):
            return query1
        else:
            return False

    @classmethod
    def _add(cls, path, value=None, regtype=None, data=None, force=False):
        def subexec(path, value, regtype, data):
            try:
                if not isinstance(regc.add(path, value, regtype, data), rc):
                    if cls.exists(path, value):
                        return True
            finally:
                return False

        path = cls._normpath(str(path))
        value = value if value else ''

        if not subexec(path, value, regtype, data):
            if force:
                acl1 = acl.Templates.reg_unlock(path)
                acl1.execute()
                if not subexec(path, value, regtype, data):
                    parent = cls.find_parent(path)
                    if parent:
                        acl2 = acl.Templates.reg_unlock(parent)
                        acl2.execute()
                        subexec(path, value, regtype, data)

        if cls.exists(path, value):
            _logger.info('"{} {}" has been successfully added.'.format(path, value))
            return True
        _logger.info('"{} {}" was not added.'.format(path, value))
        return False

    @classmethod
    def add_container(cls, path, force=False):
        return cls._add(path=path, force=force)

    @classmethod
    def add_object(cls, path, value=None, regtype=None, data=None, force=False):
        return cls._add(path=path, value=value, regtype=regtype, data=data, force=force)

    @classmethod
    def _rem(cls, path, object=None, force=False):
        def subexec(path, object):
            try:
                regc.delete(path, object)
                return not cls.exists(path, object)
            except:
                return False

        path = cls._normpath(str(path))
        if not cls.exists(path, object):
            _logger.warning('{} Registry not found, skipping.'.format(path))
            return True
        if not subexec(path, object):
            if force:
                acl1 = acl.Templates.reg_unlock(path)
                acl1.execute()
                if not subexec(path, object):
                    parent = cls.find_parent(path)
                    if parent:
                        acl2 = acl.Templates.file_unlock(parent)
                        acl2.execute()
                        subexec(path, object)

        if not cls.exists(path, object):
            _logger.info('"{}" has been successfully removed.'.format(path))
            return True
        _logger.info('"{}" Registry not removed.'.format(path))
        return False

    @classmethod
    def rem_container(cls, path, force=False):
        return cls._rem(path, None, force)

    @classmethod
    def rem_object(cls, path, object, force=False):
        return cls._rem(path, object, force)

    @classmethod
    def exists(cls, path, value=None):
        res = not isinstance(regc.query(path, value), rc)
        if not (res or value):
            dirname, basename = os.path.split(path)
            query1 = regc.query(dirname, value)
            if not isinstance(query1, rc):
                for i in query1:
                    if i['key'].lower() == basename.lower():
                        return True
        return res

    @classmethod
    def lock(cls, path):
        path = cls._normpath(str(path))
        acl1 = acl.Templates.reg_lock(path)
        acl1.execute()

    @classmethod
    def unlock(cls, path):
        path = cls._normpath(str(path))
        acl1 = acl.Templates.reg_unlock(path)
        acl1.execute()
