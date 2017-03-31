from csv_dictreader_extended import DictReaderExtended
import logger
import os
import subprocess

from enum import Enum

_logger = logger.Logger().get_logger('operations_process_controller')


class ControllerException(Exception):
    pass


class ReturnCode(int):
    iter_skip = False

    def __iter__(self):
        if self.iter_skip:
            return tuple().__iter__()
        raise TypeError()


class ControllerBase(object):
    _BIN = None
    _SUCCESS_CODES = (0,)

    @classmethod
    def _execute(cls, parameters, filter=None):
        cmd = ' '.join((cls._BIN, parameters))
        _logger.debug('{} Exec:{}'.format(cls.__class__.__name__, cmd))
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        ret = ReturnCode(p.returncode)
        if ret in cls._SUCCESS_CODES:
            res = out
        else:
            res = ret
        if filter:
            return filter(res)
        else:
            return res

    @classmethod
    def _exec_filter_csv(cls, value):
        if isinstance(value, ReturnCode):
            return value
        else:
            return DictReaderExtended(cls, value.strip().split("\n"))

    @classmethod
    def _exec_filter_nostr(cls, value):
        if isinstance(value, ReturnCode):
            return value
        else:
            return True

    @classmethod
    def _exec_filter_bool(cls, value):
        if isinstance(value, ReturnCode):
            return False
        else:
            return True


class WUSAController(ControllerBase):
    _BIN = 'wusa'
    _SUCCESS_CODES = (0, 1, 2359302, 3010)

    @classmethod
    def wusa_install(cls, path):
        path = os.path.normpath(path)
        params = '"{}" /quiet /norestart'.format(path)
        return cls._execute(params, cls._exec_filter_nostr)

    @classmethod
    def wusa_uninstall(cls, kbnumber):
        params = '/kb:{} /norestart /quiet /uninstall /quiet /norestart'.format(str(kbnumber))
        return cls._execute(params, cls._exec_filter_nostr)


# /kb:$kbnumber /norestart /quiet /uninstall

class WMIController(ControllerBase):
    _BIN = 'wmic'

    @classmethod
    def diskdrive_list(cls):
        params = 'diskdrive list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def process_list(cls):
        params = 'process list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def product_list(cls):
        params = 'product list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def nic_list(cls):
        params = 'nic list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def computersystem_list(cls):
        params = 'computersystem list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def partition_list(cls):
        params = 'partition list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def bios_list(cls):
        params = 'bios list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def qfe_list(cls):
        # QFE - Quick Fix Engineering. List all installed Microsoft hotfixes/patches
        params = 'qfe list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def useraccount_list(cls):
        # USERACCOUNT - User account management
        params = 'useraccount list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def netlogin_list(cls):
        # NETLOGIN - Network login information (of a particular user) management
        params = 'netlogin list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def startup_list(cls):
        params = 'startup list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def share_list(cls):
        params = 'share list full /format:csv'
        return cls._execute(params, cls._exec_filter_csv)

    @classmethod
    def process_terminate(cls, handle_count=None, name=None, priority=None, process_id=None, thread_count=None,
                          working_set_size=None):
        assert handle_count or name or priority or process_id or thread_count or working_set_size
        query = list()
        if handle_count: query.append('HandleCount="{}"'.format(handle_count))
        if name: query.append('Name="{}"'.format(name))
        if priority: query.append('Priority="{}"'.format(priority))
        if process_id: query.append('ProcessId="{}"'.format(process_id))
        if thread_count: query.append('ThreadCount="{}"'.format(thread_count))
        if working_set_size: query.append('WorkingSetSize="{}"'.format(working_set_size))
        params = 'process where ({}) call terminate'.format(" and ".join(query))
        ret = cls._execute(params, False)
        return ret if isinstance(ret, ReturnCode) else True

    @classmethod
    def process_delete(cls, handle_count=None, name=None, priority=None, process_id=None, thread_count=None,
                       working_set_size=None):
        assert handle_count or name or priority or process_id or thread_count or working_set_size
        query = list()
        if handle_count: query.append('HandleCount="{}"'.format(handle_count))
        if name: query.append('Name="{}"'.format(name))
        if priority: query.append('Priority="{}"'.format(priority))
        if process_id: query.append('ProcessId="{}"'.format(process_id))
        if thread_count: query.append('ThreadCount="{}"'.format(thread_count))
        if working_set_size: query.append('WorkingSetSize="{}"'.format(working_set_size))
        params = 'process where ({}) delete'.format(" and ".join(query))
        ret = cls._execute(params, False)
        return ret if isinstance(ret, ReturnCode) else True

    @classmethod
    def product_uninstall(cls, caption=None, identifying_number=None, name=None, vendor=None, version=None):
        assert caption or identifying_number or name or vendor or version
        query = list()
        if caption: query.append('Caption="{}"'.format(caption))
        if identifying_number: query.append('IdentifyingNumber="{}"'.format(identifying_number))
        if name: query.append('Name="{}"'.format(name))
        if vendor: query.append('Vendor="{}"'.format(vendor))
        if version: query.append('Version="{}"'.format(version))
        params = 'product where ({}) uninstall'.format(" and ".join(query))
        ret = cls._execute(params, False)
        return ret if isinstance(ret, ReturnCode) else True

    @classmethod
    def share_delete(cls, description=None, name=None, path=None):
        assert description or name or path
        query = list()
        if description: query.append('Description="{}"'.format(description))
        if name: query.append('Name="{}"'.format(name))
        if path: query.append('Path="{}"'.format(path))
        params = 'share where ({}) delete'.format(" and ".join(query))
        ret = cls._execute(params, False)
        return ret if isinstance(ret, ReturnCode) else True


class RobocopyController(ControllerBase):
    _BIN = 'robocopy'
    _SUCCESS_CODES = (0, 1)

    class OptionGeneric(Enum):
        SUBDIRS = 'S'
        EMPTY_SUBDIRS = 'E'
        EXCLUDE_JUNCTIONS = 'XJ'

    class OptionAttributeAdd(Enum):
        READ_ONLY = 'R'
        ARCHIVE = 'E'
        SYSTEM = 'S'
        HIDDEN = 'H'
        COMPRESSED = 'C'
        NOT_CONTENT_INDEXED = 'N'
        ENCRYPTED = 'E'
        TEMPORARY = 'T'
        OFFLINE = 'O'

    class OptionAttributeRemove(Enum):
        READ_ONLY = 'R'
        ARCHIVE = 'E'
        SYSTEM = 'S'
        HIDDEN = 'H'
        COMPRESSED = 'C'
        NOT_CONTENT_INDEXED = 'N'
        ENCRYPTED = 'E'
        TEMPORARY = 'T'
        OFFLINE = 'O'

    @classmethod
    def robocopy(cls, source, dest, options=()):
        options_generic = set([i for i in options if isinstance(i, cls.OptionGeneric)])
        option_attribute_add = set([i for i in options if isinstance(i, cls.OptionAttributeAdd)])
        option_attribute_remove = set([i for i in options if isinstance(i, cls.OptionAttributeRemove)])
        subparams = list()

        # Sorting
        order_option_generic = {v: i for i, v in enumerate(
            [cls.OptionGeneric.SUBDIRS, cls.OptionGeneric.EMPTY_SUBDIRS, cls.OptionGeneric.EXCLUDE_JUNCTIONS])}
        sorted_options_generic = sorted(list(options_generic), key=lambda d: order_option_generic[d])

        for i in sorted_options_generic or (): subparams += ['/{}'.format(i.value)]
        if option_attribute_add: subparams += ['/A+:{}'.format(''.join([i.value for i in option_attribute_add]))]
        if option_attribute_remove: subparams += ['/A-:{}'.format(''.join([i.value for i in option_attribute_remove]))]
        params = '{options}"{source}" "{dest}"'.format(
            options=' '.join(subparams + [' ']) if subparams else '',
            source=os.path.normpath(source),
            dest=os.path.normpath(dest),
        )
        return cls._execute(params, cls._exec_filter_nostr)


class RegController(ControllerBase):
    _BIN = 'reg'

    class RegType(Enum):
        BINARY = "reg_binary"
        DWORD = "reg_dword"
        DWORD_LITTLE_ENDIAN = "reg_dword_little_endian"
        DWORD_BIG_ENDIAN = "reg_dword_big_endian"
        EXPAND_SZ = "reg_expand_sz"
        LINK = "reg_link"
        MULTI_SZ = "reg_multi_sz"
        NONE = "reg_none"
        QWORD = "reg_qword"
        QWORD_LITTLE_ENDIAN = "reg_qword_little_endian"
        SZ = "reg_sz"

    @classmethod
    def _exec_filter_reg_query(cls, value):
        if isinstance(value, ReturnCode):
            return value
        else:
            has_values = True if [True for i in value.split("\n") if i.startswith('    ')] else False
            csv_template = '"{object}","{key}","{value}","{type}","{data}"'
            csv_data = ['"object","key","value","type","data"']
            for i, line in enumerate(value.split("\n")):
                if has_values and i is 1:
                    # print 'skypping parent'
                    continue
                if not line.strip():
                    continue

                if line.startswith('    '):  # its a value
                    row_items = line.strip().split("    ")
                    for i in range((3 - len(row_items))):
                        row_items.append([])
                    vvalue, vtype, vdata = row_items
                    csv_data.append(
                        csv_template.format(object='value', key='', value=vvalue, type=vtype.lower(), data=vdata))
                else:  # its a key
                    csv_data.append(
                        csv_template.format(object='key', key=os.path.split(line.strip())[1], value='', type='',
                                            data=''))

            return DictReaderExtended(cls, csv_data)

    @classmethod
    def add(cls, key, value=None, regtype=None, data=None):
        subparams = list()
        if value: subparams.append('/v "{}"'.format(value))
        if regtype: subparams.append(
            '/t {}'.format(regtype.value if isinstance(regtype, cls.RegType) else str(regtype)))
        if data: subparams.append('/d "{}"'.format(data))
        subparams.append('/f')
        params = 'add "{}" {}'.format(os.path.normpath(key), ' '.join(subparams))
        return cls._execute(params, cls._exec_filter_nostr)

    @classmethod
    def delete(cls, key, value=None):
        subparams = list()
        if value: subparams.append('/v "{}"'.format(value))
        subparams.append('/f')
        params = 'delete "{}" {}'.format(os.path.normpath(key), ' '.join(subparams))
        return cls._execute(params, cls._exec_filter_nostr)

    @classmethod
    def query(cls, key, value=None):
        subparams = list()
        if value: subparams.append('/v "{}"'.format(value))
        params = 'query "{}" {}'.format(os.path.normpath(key), ' '.join(subparams))
        # cls._execute(params, cls._exec_filter_reg_query_fetch if value else cls._exec_filter_reg_query)
        return cls._execute(params, cls._exec_filter_reg_query)

    @classmethod
    def load(cls, key, source):
        params = 'load "{}" "{}"'.format(key, os.path.normpath(source))
        return cls._execute(params, cls._exec_filter_bool)

    @classmethod
    def unload(cls, key):
        params = 'unload "{}"'.format(key)
        return cls._execute(params, cls._exec_filter_bool)


class RDController(ControllerBase):
    _BIN = 'rd'

    @classmethod
    def rd(cls, path):
        params = r'/s /q "{}"'.format(os.path.normpath(path))
        return cls._execute(params, cls._exec_filter_nostr)


class NetController(ControllerBase):
    _BIN = 'net'

    @classmethod
    def stop(cls, service):
        params = 'stop "{}"'.format(service)
        return cls._execute(params, cls._exec_filter_nostr)

    @classmethod
    def start(cls, service):
        params = 'start "{}"'.format(service)
        return cls._execute(params, cls._exec_filter_nostr)

    @classmethod
    def user_add(cls, username, change_password=False):
        subparams = ''
        if change_password: subparams += ' /logonpasswordchg:yes'
        params = 'user "{}" /add{}'.format(username, subparams)
        return cls._execute(params, cls._exec_filter_nostr)

    @classmethod
    def user_delete(cls, username):
        params = 'user "{}" /delete'.format(username)
        return cls._execute(params, cls._exec_filter_nostr)

    @classmethod
    def localgroup_user_add(cls, username, group):
        params = 'localgroup {} {} /add'.format(group, username)
        return cls._execute(params, cls._exec_filter_nostr)


class SCController(ControllerBase):
    _BIN = 'sc'

    class StartMode(Enum):
        AUTO = 'auto'
        DISABLED = 'disabled'

    @classmethod
    def _exec_filter_sc_query(cls, value):
        if isinstance(value, ReturnCode):
            return value
        else:
            csv_data = [
                '"service_name","display_name","type","type_label","state","state_label","config","win32_exit_code","service_exit_code","checkpoint","wait_hint"']
            for i in value.split("\r\n\r\n"):
                row = [''] * 11

                if i.find('SERVICE_NAME') > -1:
                    row[0] = i.split('SERVICE_NAME')[1].split(':')[1].split("\n")[0].strip()
                if i.find('DISPLAY_NAME') > -1:
                    row[1] = i.split('DISPLAY_NAME')[1].split(':')[1].split("\n")[0].strip()
                if i.find('TYPE') > -1:
                    row[2] = i.split('TYPE')[1].split(':')[1].split("\n")[0].strip().split('  ')[0].strip()
                    row[3] = i.split('TYPE')[1].split(':')[1].split("\n")[0].strip().split('  ')[1].strip()
                if i.find('STATE') > -1:
                    row[4] = i.split('STATE')[1].split(':')[1].split("\n")[0].strip().split('  ')[0].strip()
                    row[5] = i.split('STATE')[1].split(':')[1].split("\n")[0].strip().split('  ')[1].strip()
                if i.find('WIN32_EXIT_CODE') > -1:
                    row[7] = i.split('WIN32_EXIT_CODE')[1].split(':')[1].split("\n")[0].strip().split('  ')[0].strip()
                if i.find('SERVICE_EXIT_CODE') > -1:
                    row[8] = i.split('SERVICE_EXIT_CODE')[1].split(':')[1].split("\n")[0].strip().split('  ')[0].strip()
                if i.find('CHECKPOINT') > -1:
                    row[9] = i.split('CHECKPOINT')[1].split(':')[1].split("\n")[0].strip()
                if i.find('WAIT_HINT') > -1:
                    row[10] = i.split('WAIT_HINT')[1].split(':')[1].split("\n")[0].strip()
                row[6] = (
                    [';'.join([k.strip() for k in j.strip(" \r\n()").split(',')]) for j in i.strip().split("\n") if
                     j.find(':') is -1] or [' ', ])[0]

                csv_data.append(','.join(['"{}"'.format(j) for j in row]))

            return DictReaderExtended(cls, csv_data)

    @classmethod
    def query(cls, service=None):
        subquery = ' "{}"'.format(service) if service else ''
        params = 'query{}'.format(subquery)
        return cls._execute(params, cls._exec_filter_sc_query)

    @classmethod
    def config(cls, service, start_mode):
        params = 'config "{}" start= {}'.format(service, cls.StartMode(start_mode).value)
        return cls._execute(params, cls._exec_filter_nostr)

    @classmethod
    def delete(cls, service):
        params = 'delete "{}"'.format(service)
        return cls._execute(params, cls._exec_filter_nostr)


class SchtasksController(ControllerBase):
    _BIN = 'schtasks'

    @classmethod
    def exists(cls, path):
        params = '/query /tn "{}"'.format(os.path.normpath(path))
        return cls._execute(params, cls._exec_filter_bool)

    @classmethod
    def disable(cls, path):
        params = '/change /disable /tn "{}"'.format(os.path.normpath(path))
        return cls._execute(params, cls._exec_filter_nostr)


class TaskkillController(ControllerBase):
    _BIN = 'taskkill'

    @classmethod
    def taskkill(cls, process):
        params = '/f /im "{}" /t'.format(process)
        return cls._execute(params, cls._exec_filter_nostr)


class AttribController(ControllerBase):
    _BIN = 'attrib'

    @classmethod
    def attrib(cls, path, read_only=None, hidden=None, system=None, recursive=False):
        subparams = list()
        if not read_only is None: subparams.append('+r' if read_only else '-r')
        if not system is None: subparams.append('+s' if system else '-s')
        if not hidden is None: subparams.append('+h' if hidden else '-h')
        if recursive: subparams.append('/s /d')

        params = '{} "{}"'.format(' '.join(subparams), os.path.normpath(path))
        return cls._execute(params, cls._exec_filter_nostr)


class NetstatController(ControllerBase):
    _BIN = 'netstat'

    @classmethod
    def _exec_filter_netstat(cls, value):
        if isinstance(value, ReturnCode):
            return value
        else:
            csv_data = ['"proto","local_address","foreign_address","state","pid"']
            for line in value.split("\n")[4:-1]:
                row = [''] * 5
                items = line.split()
                if len(items) > 3:
                    row[0] = items[0]
                    row[1] = items[1]
                    row[2] = items[2]
                    row[4] = items[-1]
                    if len(items) == 5:
                        row[3] = items[3]
                csv_data.append(','.join(['"{}"'.format(j) for j in row]))
            return DictReaderExtended(cls, csv_data)
            # return value

    @classmethod
    def netstat(cls):
        params = '-ano'
        return cls._execute(params, cls._exec_filter_netstat)


class PowerShellController(ControllerBase):
    _BIN = 'powershell'

    @classmethod
    def command(cls, command):
        params = '-executionpolicy bypass -command "{}"'.format(os.path.normpath(command))
        return cls._execute(params, cls._exec_filter_bool)
