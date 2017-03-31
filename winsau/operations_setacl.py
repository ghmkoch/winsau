#
# SetACL.exe simple wrapper for python
# Copyright (c) 2017 Martin Saavedra
# Binary file needed and can be downloaded from https://helgeklein.com/download/
# Distributed under MIT License
#

import logger
import os
import subprocess
from collections import defaultdict
from enum import Enum
# from config import config

_logger = logger.Logger().get_logger('operations_setacl')
# bin_path = config.get('setacl', 'bin_path', True) #todo
BIN_PATH = 'SetACL64.exe'


class WNTrustee(Enum):
    NULL_AUTHORITY = 'S-1-0'
    NOBODY = 'S-1-0-0'
    WORLD_AUTHORITY = 'S-1-1'
    EVERYONE = 'S-1-1-0'
    UNTRUSTED_MANDATORY_LEVEL = 'S-1-16-0'
    HIGH_MANDATORY_LEVEL = 'S-1-16-12288'
    SYSTEM_MANDATORY_LEVEL = 'S-1-16-16384'
    PROTECTED_PROCESS_MANDATORY_LEVEL = 'S-1-16-20480'
    SECURE_PROCESS_MANDATORY_LEVEL = 'S-1-16-28672'
    LOW_MANDATORY_LEVEL = 'S-1-16-4096'
    MEDIUM_MANDATORY_LEVEL = 'S-1-16-8192'
    MEDIUM_PLUS_MANDATORY_LEVEL = 'S-1-16-8448'
    LOCAL_AUTHORITY = 'S-1-2'
    LOCAL = 'S-1-2-0'
    CONSOLE_LOGON = 'S-1-2-1'
    CREATOR_AUTHORITY = 'S-1-3'
    CREATOR_OWNER = 'S-1-3-0'
    CREATOR_GROUP = 'S-1-3-1'
    CREATOR_OWNER_SERVER = 'S-1-3-2'
    CREATOR_GROUP_SERVER = 'S-1-3-3'
    OWNER_RIGHTS = 'S-1-3-4'
    NONUNIQUE_AUTHORITY = 'S-1-4'
    NT_AUTHORITY = 'S-1-5'
    DIALUP = 'S-1-5-1'
    PRINCIPAL_SELF = 'S-1-5-10'
    AUTHENTICATED_USERS = 'S-1-5-11'
    RESTRICTED_CODE = 'S-1-5-12'
    TERMINAL_SERVER_USERS = 'S-1-5-13'
    REMOTE_INTERACTIVE_LOGON = 'S-1-5-14'
    THIS_ORGANIZATION_GROUP = 'S-1-5-15'
    THIS_ORGANIZATION_ACCOUNT = 'S-1-5-17'
    LOCAL_SYSTEM = 'S-1-5-18'
    NT_AUTHORITY_LOCAL_SERVICE = 'S-1-5-19'
    NETWORK = 'S-1-5-2'
    NT_AUTHORITY_NETWORK_SERVICE = 'S-1-5-20'
    ENTERPRISE_READONLY_DOMAIN_CONTROLLERS = 'S-1-5-21-498'
    ADMINISTRATOR = 'S-1-5-21-500'
    GUEST = 'S-1-5-21-501'
    KRBTGT = 'S-1-5-21-502'
    DOMAIN_ADMINS = 'S-1-5-21-512'
    DOMAIN_USERS = 'S-1-5-21-513'
    DOMAIN_GUESTS = 'S-1-5-21-514'
    DOMAIN_COMPUTERS = 'S-1-5-21-515'
    DOMAIN_CONTROLLERS = 'S-1-5-21-516'
    CERT_PUBLISHERS = 'S-1-5-21-517'
    SCHEMA_ADMINS = 'S-1-5-21-518'
    ENTERPRISE_ADMINS = 'S-1-5-21-519'
    GROUP_POLICY_CREATOR_OWNERS = 'S-1-5-21-520'
    READONLY_DOMAIN_CONTROLLERS = 'S-1-5-21-521'
    CLONEABLE_DOMAIN_CONTROLLERS = 'S-1-5-21-522'
    RAS_AND_IAS_SERVERS = 'S-1-5-21-553'
    ALLOWED_RODC_PASSWORD_REPLICATION_GROUP = 'S-1-5-21-571'
    DENIED_RODC_PASSWORD_REPLICATION_GROUP = 'S-1-5-21-572'
    BATCH = 'S-1-5-3'
    ADMINISTRATORS = 'S-1-5-32-544'
    USERS = 'S-1-5-32-545'
    GUESTS = 'S-1-5-32-546'
    POWER_USERS = 'S-1-5-32-547'
    ACCOUNT_OPERATORS = 'S-1-5-32-548'
    SERVER_OPERATORS = 'S-1-5-32-549'
    PRINT_OPERATORS = 'S-1-5-32-550'
    BACKUP_OPERATORS = 'S-1-5-32-551'
    REPLICATORS = 'S-1-5-32-552'
    BUILTIN_PREWINDOWS__COMPATIBLE_ACCESS = 'S-1-5-32-554'
    BUILTIN_REMOTE_DESKTOP_USERS = 'S-1-5-32-555'
    BUILTIN_NETWORK_CONFIGURATION_OPERATORS = 'S-1-5-32-556'
    BUILTIN_INCOMING_FOREST_TRUST_BUILDERS = 'S-1-5-32-557'
    BUILTIN_PERFORMANCE_MONITOR_USERS = 'S-1-5-32-558'
    BUILTIN_PERFORMANCE_LOG_USERS = 'S-1-5-32-559'
    BUILTIN_WINDOWS_AUTHORIZATION_ACCESS_GROUP = 'S-1-5-32-560'
    BUILTIN_TERMINAL_SERVER_LICENSE_SERVERS = 'S-1-5-32-561'
    BUILTIN_DISTRIBUTED_COM_USERS = 'S-1-5-32-562'
    BUILTIN_CRYPTOGRAPHIC_OPERATORS = 'S-1-5-32-569'
    BUILTIN_EVENT_LOG_READERS = 'S-1-5-32-573'
    BUILTIN_CERTIFICATE_SERVICE_DCOM_ACCESS = 'S-1-5-32-574'
    BUILTIN_RDS_REMOTE_ACCESS_SERVERS = 'S-1-5-32-575'
    BUILTIN_RDS_ENDPOINT_SERVERS = 'S-1-5-32-576'
    BUILTIN_RDS_MANAGEMENT_SERVERS = 'S-1-5-32-577'
    BUILTIN_HYPERV_ADMINISTRATORS = 'S-1-5-32-578'
    BUILTIN_ACCESS_CONTROL_ASSISTANCE_OPERATORS = 'S-1-5-32-579'
    BUILTIN_REMOTE_MANAGEMENT_USERS = 'S-1-5-32-580'
    INTERACTIVE = 'S-1-5-4'
    SERVICE = 'S-1-5-6'
    NTLM_AUTHENTICATION = 'S-1-5-64-10'
    SCHANNEL_AUTHENTICATION = 'S-1-5-64-14'
    DIGEST_AUTHENTICATION = 'S-1-5-64-21'
    ANONYMOUS = 'S-1-5-7'
    PROXY = 'S-1-5-8'
    NT_SERVICE = 'S-1-5-80'
    ALL_SERVICES = 'S-1-5-80-0'
    NT_VIRTUAL_MACHINE_VIRTUAL_MACHINES = 'S-1-5-83-0'
    ENTERPRISE_DOMAIN_CONTROLLERS = 'S-1-5-9'


class ObjectType(Enum):
    FILE, REGISTRY = 'file', 'reg'


class _AbstractACLAction(object):
    _SIGN = None

    @property
    def SIGN(self):
        return self._SIGN

    def __setattr__(self, key, value):
        if key == 'SIGN': return
        return super.__setattr__(self, key, value)

    def compile(self):
        return


class What(Enum):
    DACL, SACL, OWNER, PRIMARY_GROUP = ('d', 's', 'o', 'g')


class Where(Enum):
    DACL, SACL, BOTH = ('dacl', 'sacl', 'dacl,sacl')


class FilePermission(Enum):
    READ, WRITE, LIST_FOLDER, READ_EXECUTE, CHANGE, FULL_ACCESS, TRAVERSE, LIST_DIR, READ_ATTRIBUTES, \
    READ_EXTENDED_ATTRIBUTES, ADD_FILE, ADD_SUBDIR, WRITE_ATTRIBUTES, WRITE_EXTENDED_ATTRIBUTES, DELETE_CHILD, DELETE, \
    READ_PERMISSIONS, WRITE_PERMISSIONS, WRITE_OWNER = (
        'read', 'write', 'list_folder', 'read_ex', 'change', 'full', 'traverse', 'list_dir', 'read_attr', 'read_ea',
        'add_file', 'add_subdir', 'write_attr', 'write_ea', 'del_child', 'delete', 'read_dacl', 'write_dacl',
        'write_owner')


class RegistryPermission(Enum):
    READ, FULL_ACCESS, QUERY_VALUE, SET_VALUE, CREATE_SUBKEY, ENUM_SUBKEYS, NOTIFY, CREATE_LINK, DELETE, \
    WRITE_PERMISSIONS, WRITE_OWNER, READ_ACCESS = (
        'read', 'full', 'query_val', 'set_val', 'create_subkey', 'enum_subkeys', 'notify', 'create_link', 'delete',
        'write_dacl', 'write_owner', 'read_access')


class FileRecursion(Enum):
    NO = 'no'
    CONT = 'cont'
    OBJ = 'obj'
    CONT_OBJ = 'cont_obj'


class RegistryRecursion(Enum):
    NO = 'no'
    YES = 'yes'


class Inheritance(Enum):
    SUBOBJECTS, SUBCONTAINERS, NO_PROPAGATION, INHERIT_ONLY = ('so', 'sc', 'np', 'io')


class ModeDACL(Enum):
    SET, GRANT, DENY, REVOKE = ('set', 'grant', 'deny', 'revoke')


class ModeSACL(Enum):
    AUDIT_SUCCESS, AUDIT_FAILURE, REVOKE = ('aud_succ', 'aud_fail', 'revoke')


class TrusteeAction(Enum):
    REMOVE = 'remtrst'
    REPLACE = 'repltrst'
    COPY = 'cpytrst'


class DomainAction(Enum):
    REMOVE = 'remdom'
    REPLACE = 'repltrst'
    COPY = 'cpytrst'


class Protection(Enum):
    NO_CHANGE = 'nc'
    NO_PROTECTED = 'np'
    PROTECTED_COPY = 'pc'
    PROTECTED_NO_COPY = 'p_nc'


class ActionACE(_AbstractACLAction):
    _SIGN = 'ace'

    def __init__(self, trustee, permissions, inheritance=None, mode=None, where=None):
        self.trustee = trustee
        self.permissions = permissions
        self.inheritance = inheritance
        self.mode = mode
        self.where = where

    def compile(self):
        for i in self.permissions:
            if not ((i in FilePermission) or (i in RegistryPermission)): raise TypeError()
        if self.inheritance:
            for i in self.inheritance:
                if i not in Inheritance: raise TypeError()
        if self.mode:
            if not ((self.mode in ModeDACL) or (self.mode in ModeSACL)): raise TypeError()
        if self.where:
            if self.where not in Where: raise TypeError()
        c_trustee = ('n:{}'.format(self.trustee.value if self.trustee in WNTrustee else self.trustee),)
        c_permissions = ('p:{}'.format(','.join([i.value for i in self.permissions])),)
        c_inheritance = ('i:{}'.format(','.join([i.value for i in self.inheritance])),) if self.inheritance else ()
        c_mode = ('m:{}'.format(self.mode.value),) if self.mode else ()
        c_where = ('w:{}'.format(self.where.value),) if self.where else ()
        c_layer0 = ';'.join(c_trustee + c_permissions + c_inheritance + c_mode + c_where)
        c_layer1 = '-ace "{}"'.format(c_layer0)
        return c_layer1


class ActionTrustee(_AbstractACLAction):
    _SIGN = 'trustee'

    def __init__(self, trustee1, trustee_action, trustee2=None, what=None):
        self.trustee1 = trustee1
        self.trustee2 = trustee2
        self.trustee_action = trustee_action
        self.what = what

    def compile(self):
        if self.what:
            for i in self.what:
                if i not in What: raise TypeError()
        if self.trustee_action not in TrusteeAction: raise TypeError()

        c_trustee1 = ('n1:{}'.format(self.trustee1.value if self.trustee1 in WNTrustee else self.trustee1),)
        c_trustee2 = (
            'n2:{}'.format(
                self.trustee2.value if self.trustee2 in WNTrustee else self.trustee2),) if self.trustee2 else ()
        c_trustee_action = ('ta:{}'.format(self.trustee_action.value),)
        c_permissions = ('w:{}'.format(','.join([i.value for i in self.what])),) if self.what else ()

        c_layer0 = ';'.join(c_trustee1 + c_trustee2 + c_trustee_action + c_permissions)
        c_layer1 = '-trst "{}"'.format(c_layer0)
        return c_layer1


class ActionDomain(_AbstractACLAction):
    _SIGN = 'domain'

    def __init__(self, trustee1, domain_action, trustee2=None, what=None):
        self.trustee1 = trustee1
        self.trustee2 = trustee2
        self.domain_action = domain_action
        self.what = what

    def compile(self):
        if self.what:
            for i in self.what:
                if i not in What: raise TypeError()
        if self.domain_action not in DomainAction: raise TypeError()

        c_trustee1 = ('n1:{}'.format(self.trustee1.value if self.trustee1 in WNTrustee else self.trustee1),)
        c_trustee2 = (
            'n2:{}'.format(
                self.trustee2.value if self.trustee2 in WNTrustee else self.trustee2
            ),
        ) if self.trustee2 else ()
        c_trustee_action = ('da:{}'.format(self.domain_action.value),)
        c_permissions = ('w:{}'.format(','.join([i.value for i in self.what])),) if self.what else ()

        c_layer0 = ';'.join(c_trustee1 + c_trustee2 + c_trustee_action + c_permissions)
        c_layer1 = '-dom "{}"'.format(c_layer0)
        return c_layer1


class ActionSetOwner(_AbstractACLAction):
    _SIGN = 'setowner'

    def __init__(self, trustee):
        self.trustee = trustee

    def compile(self):
        c_layer0 = 'n:{}'.format(self.trustee.value if self.trustee in WNTrustee else self.trustee)
        c_layer1 = '-ownr "{}"'.format(c_layer0)
        return c_layer1


class ActionPrimaryGroup(_AbstractACLAction):
    _SIGN = 'setgroup'

    def __init__(self, trustee):
        self.trustee = trustee

    def compile(self):
        c_layer0 = 'n:{}'.format(self.trustee.value if self.trustee in WNTrustee else self.trustee)
        c_layer1 = '-grp "{}"'.format(c_layer0)
        return c_layer1


class ActionSetProtectionFlags(_AbstractACLAction):
    _SIGN = 'setprot'

    def __init__(self, dacl, sacl):
        self.dacl = dacl
        self.sacl = sacl

    def compile(self):
        if self.dacl not in Protection: raise TypeError()
        if self.sacl not in Protection: raise TypeError()
        c_dacl = ('dacl:{}'.format(self.dacl.value),)
        c_sacl = ('sacl:{}'.format(self.sacl.value),)
        c_layer0 = ";".join((c_dacl + c_sacl))
        c_layer1 = '-op "{}"'.format(c_layer0)
        return c_layer1


class ActionResetChildren(_AbstractACLAction):
    _SIGN = 'rstchldrn'

    def __init__(self, where):
        self.where = where

    def compile(self):
        if self.where not in Where: raise TypeError()
        c_layer0 = self.where.value
        c_layer1 = '-rst "{}"'.format(c_layer0)
        return c_layer1


class ActionClear(_AbstractACLAction):
    _SIGN = 'clear'

    def __init__(self, where):
        self.where = where

    def compile(self):
        if self.where not in Where: raise TypeError()
        c_layer0 = self.where.value
        c_layer1 = '-clr "{}"'.format(c_layer0)
        return c_layer1


class ActionDeleteOrphanedSIDs(_AbstractACLAction):
    _SIGN = 'delorphanedsids'

    def __init__(self, where):
        self.where = where

    def compile(self):
        if self.where not in Where: raise TypeError()
        c_layer0 = self.where.value
        c_layer1 = '-os "{}"'.format(c_layer0)
        return c_layer1


class SetACL(object):
    _MULTIPLE_ACTIONS_ORDER = ['restore', 'clear', 'trustee', 'domain', 'ace', 'setowner', 'setgroup', 'setprot',
                               'rstchldrn', 'list']
    _SINGLE_ACTIONS_ORDER = ['restore', 'clear', 'trustee', 'domain', 'setowner', 'ace', 'setgroup', 'setprot',
                             'rstchldrn', 'list']

    _COMMAND = '{bin} -on "{path}" -ot {object_type} {parameters}'

    def __init__(self, path, object_type, actions, preowner_action = None, recursion=None, combined=True):
        self.path = os.path.normpath(path)
        self.object_type = object_type
        self.actions = actions
        self.recursion = recursion
        self.combined = combined
        self.preowner_action = preowner_action

    def command(self, multi_line=False):
        if self.preowner_action:
            if not isinstance(self.preowner_action, ActionSetOwner): raise TypeError()
        for i in self.actions:
            if not isinstance(i, _AbstractACLAction): raise TypeError()

        if self.recursion:
            if self.recursion not in (RegistryRecursion if self.object_type is ObjectType.REGISTRY else FileRecursion):
                raise TypeError()

        if self.combined:
            grouped_actions = defaultdict(list)
            for i in self.actions: grouped_actions[i.SIGN].append(i)
            actions = grouped_actions.iteritems()
        else:
            actions = ((i.SIGN, (i,)) for i in self.actions)

        compiled_actions = list()
        order_switch = self._MULTIPLE_ACTIONS_ORDER if self.combined else self._SINGLE_ACTIONS_ORDER
        order = {v: i for i, v in enumerate(order_switch)}
        sorted_actions = sorted(actions, key=lambda d: order[d[0]])

        for action_type, action_list in sorted_actions:
            compiled_actions.append(
                '{multi_line_pad}-actn {action_type} {action_params}'.format(
                    multi_line_pad="\n    " if multi_line else '',
                    action_type=action_type,
                    action_params=' '.join(
                        ['{multi_line_pad}{action_params}'.format(
                            multi_line_pad="\n        " if multi_line and len(action_list) > 1 else '',
                            action_params=i.compile(),
                        ) for i in action_list])
                )
            )

        c_rec = ('{multi_line_pad}-rec {args}'.format(
            multi_line_pad="\n    " if multi_line else '',
            args=self.recursion.value
        ),) if self.recursion else ()

        if self.combined:
            c_actions = (' '.join(compiled_actions),)
            c_layer0 = ' '.join((c_actions + c_rec))
            c_layer1 = self._COMMAND.format(
                bin=BIN_PATH,
                path=self.path,
                object_type=self.object_type.value,
                parameters=c_layer0,
            )
            yield c_layer1
        else:
            for c_action in compiled_actions:
                c_layer0 = ' '.join(((c_action,) + c_rec))
                c_layer1 = self._COMMAND.format(
                    bin=BIN_PATH,
                    path=self.path,
                    object_type=self.object_type.value,
                    parameters=c_layer0,
                )
                yield c_layer1

    def execute(self):
        cmds = tuple(self.command())
        if self.preowner_action:
            preowner_acl = SetACL(self.path,self.object_type,(self.preowner_action,),recursion=self.recursion)
            preowner_acl.execute()

        for i, cmd in enumerate(cmds):
            _logger.debug('EXEC COMMAND "{}"'.format(cmd))
            try:
                subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                _logger.info('[{}/{}]"{}" ACL successfully changed.'
                    .format(
                    i + 1,
                    len(cmds),
                    self.path,

                )
                )
            except subprocess.CalledProcessError as e:
                raise SetACLException(SetACLReturnCodes(e.returncode))

        return


class SetACLException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Return code {}[{}]:{}".format(
            self.value.value,
            self.value.name,
            self.value.description,
        )


class SetACLReturnCodes(Enum):
    RTN_OK = 0
    RTN_USAGE = 1
    RTN_ERR_GENERAL = 2
    RTN_ERR_PARAMS = 3
    RTN_ERR_OBJECT_NOT_SET = 4
    RTN_ERR_GETSECINFO = 5
    RTN_ERR_LOOKUP_SID = 6
    RTN_ERR_INV_DIR_PERMS = 7
    RTN_ERR_INV_PRN_PERMS = 8
    RTN_ERR_INV_REG_PERMS = 9
    RTN_ERR_INV_SVC_PERMS = 10
    RTN_ERR_INV_SHR_PERMS = 11
    RTN_ERR_EN_PRIV = 12
    RTN_ERR_DIS_PRIV = 13
    RTN_ERR_NO_NOTIFY = 14
    RTN_ERR_LIST_FAIL = 15
    RTN_ERR_FINDFILE = 16
    RTN_ERR_GET_SD_CONTROL = 17
    RTN_ERR_INTERNAL = 18
    RTN_ERR_SETENTRIESINACL = 19
    RTN_ERR_REG_PATH = 20
    RTN_ERR_REG_CONNECT = 21
    RTN_ERR_REG_OPEN = 22
    RTN_ERR_REG_ENUM = 23
    RTN_ERR_PREPARE = 24
    RTN_ERR_SETSECINFO = 25
    RTN_ERR_LIST_OPTIONS = 26
    RTN_ERR_CONVERT_SD = 27
    RTN_ERR_LIST_ACL = 28
    RTN_ERR_LOOP_ACL = 29
    RTN_ERR_DEL_ACE = 30
    RTN_ERR_COPY_ACL = 31
    RTN_ERR_ADD_ACE = 32
    RTN_ERR_NO_LOGFILE = 33
    RTN_ERR_OPEN_LOGFILE = 34
    RTN_ERR_READ_LOGFILE = 35
    RTN_ERR_WRITE_LOGFILE = 36
    RTN_ERR_OS_NOT_SUPPORTED = 37
    RTN_ERR_INVALID_SD = 38
    RTN_ERR_SET_SD_DACL = 39
    RTN_ERR_SET_SD_SACL = 40
    RTN_ERR_SET_SD_OWNER = 41
    RTN_ERR_SET_SD_GROUP = 42
    RTN_ERR_INV_DOMAIN = 43
    RTN_ERR_IGNORED = 44
    RTN_ERR_CREATE_SD = 45
    RTN_ERR_OUT_OF_MEMORY = 46
    RTN_ERR_NO_ACTN_SPECIFIED = 47
    RTN_ERR_INV_WMI_PERMS = 48
    RTN_WRN_RECURSION_IMPOSSIBLE = 49

    @property
    def description(self):
        code = self.value
        return {
            0: 'OK',
            1: 'Usage instructions were printed',
            2: 'General error',
            3: 'Parameter(s) incorrect',
            4: 'The object was not set',
            5: 'The call to GetNamedSecurityInfo () failed',
            6: 'The SID for a trustee could not be found',
            7: 'Directory permissions specified are invalid',
            8: 'Printer permissions specified are invalid',
            9: 'Registry permissions specified are invalid',
            10: 'Service permissions specified are invalid',
            11: 'Share permissions specified are invalid',
            12: 'A privilege could not be enabled',
            13: 'A privilege could not be disabled',
            14: 'No notification function was given',
            15: 'An error occurred in the list function',
            16: 'FindFile reported an error',
            17: 'GetSecurityDescriptorControl () failed',
            18: 'An internal program error occurred',
            19: 'SetEntriesInAcl () failed',
            20: 'A registry path is incorrect',
            21: 'Connect to a remote registry failed',
            22: 'Opening a registry key failed',
            23: 'Enumeration of registry keys failed',
            24: 'Preparation failed',
            25: 'The call to SetNamedSecurityInfo () failed',
            26: 'Incorrect list options specified',
            27: 'A SD could not be converted to/from string format',
            28: 'ACL listing failed',
            29: 'Looping through an ACL failed',
            30: 'Deleting an ACE failed',
            31: 'Copying an ACL failed',
            32: 'Adding an ACE failed',
            33: 'No backup/restore file was specified',
            34: 'The backup/restore file could not be opened',
            35: 'A read operation from the backup/restore file failed',
            36: 'A write operation from the backup/restore file failed',
            37: 'The operating system is not supported',
            38: 'The security descriptor is invalid',
            39: 'The call to SetSecurityDescriptorDacl () failed',
            40: 'The call to SetSecurityDescriptorSacl () failed',
            41: 'The call to SetSecurityDescriptorOwner () failed',
            42: 'The call to SetSecurityDescriptorGroup () failed',
            43: 'The domain specified is invalid',
            44: 'An error occurred, but it was ignored',
            45: 'The creation of an SD failed',
            46: 'Memory allocation failed',
            47: 'No action specified - nothing to do',
            48: 'WMI permissions specified are invalid',
            49: 'Recursion is not possible'}[code]


class Templates(object):
    @staticmethod
    def file_ownership(path, trustee):
        return SetACL(
            path=path,
            object_type=ObjectType.FILE,
            actions=(
                ActionClear(Where.BOTH),
                ActionSetOwner(trustee),
                ActionSetProtectionFlags(
                    dacl=Protection.NO_PROTECTED,
                    sacl=Protection.NO_CHANGE),
            ),
            recursion=FileRecursion.CONT_OBJ,
            combined=True,
        )

    @staticmethod
    def file_unlock(path, recursive = True):
        return SetACL(
            path=path,
            object_type=ObjectType.FILE,
            actions=(
                ActionClear(Where.BOTH),
                ActionSetOwner(WNTrustee.EVERYONE),
                ActionACE(WNTrustee.EVERYONE, (FilePermission.FULL_ACCESS,), where=Where.DACL),
                ActionSetProtectionFlags(
                    dacl=Protection.PROTECTED_NO_COPY,
                    sacl=Protection.NO_CHANGE),
            ),
            preowner_action=ActionSetOwner(WNTrustee.ADMINISTRATORS),
            recursion=FileRecursion.CONT_OBJ if recursive else FileRecursion.NO,
            combined=True,
        )
    @staticmethod
    def file_lock(path, recursive = False):
        return SetACL(
            path=path,
            object_type=ObjectType.FILE,
            actions=(
                ActionClear(Where.BOTH),
                ActionACE(WNTrustee.EVERYONE, (FilePermission.READ,), where=Where.DACL),
                ActionSetProtectionFlags(
                    dacl=Protection.PROTECTED_NO_COPY,
                    sacl=Protection.NO_CHANGE),
            ),
            preowner_action=ActionSetOwner(WNTrustee.ADMINISTRATORS),
            recursion=FileRecursion.CONT_OBJ if recursive else FileRecursion.NO,
            combined=True,
        )

    @staticmethod
    def file_user_profile(path, trustee):
        return SetACL(
            path=path,
            object_type=ObjectType.FILE,
            actions=(
                ActionClear(Where.BOTH),
                ActionACE(WNTrustee.LOCAL_SYSTEM, (FilePermission.FULL_ACCESS,), where=Where.DACL),
                ActionACE(WNTrustee.ADMINISTRATORS, (FilePermission.FULL_ACCESS,), where=Where.DACL),
                ActionACE(trustee, (FilePermission.FULL_ACCESS,), where=Where.DACL),
                ActionSetOwner(WNTrustee.LOCAL_SYSTEM),
                ActionSetProtectionFlags(
                    dacl=Protection.PROTECTED_NO_COPY,
                    sacl=Protection.NO_CHANGE),
            ),
            preowner_action=(ActionSetOwner(WNTrustee.ADMINISTRATORS)),
            recursion=FileRecursion.CONT_OBJ,
            combined=True,
        )

    @staticmethod
    def reg_user_profile(path, trustee):
        return SetACL(
            path=path,
            object_type=ObjectType.REGISTRY,
            actions=(
                ActionClear(Where.BOTH),
                ActionACE(WNTrustee.RESTRICTED_CODE, (RegistryPermission.READ,), where=Where.DACL),
                ActionACE(WNTrustee.ADMINISTRATORS, (RegistryPermission.FULL_ACCESS,), where=Where.DACL),
                ActionACE(WNTrustee.LOCAL_SYSTEM, (RegistryPermission.FULL_ACCESS,), where=Where.DACL),
                ActionACE(trustee, (RegistryPermission.FULL_ACCESS,), where=Where.DACL),
                ActionSetOwner(WNTrustee.ADMINISTRATORS),
            ),
            preowner_action=(ActionSetOwner(WNTrustee.ADMINISTRATORS)),
            recursion=RegistryRecursion.YES,
            combined=False,
        )

    @staticmethod
    def reg_lock(path):
        """
        Access only for Administrators (Read + Set), and Everyone (Read) - not inherited.
        """
        return SetACL(
            path=path,
            object_type=ObjectType.REGISTRY,
            actions=(
                ActionClear(Where.BOTH),
                ActionACE(WNTrustee.ADMINISTRATORS,
                          (RegistryPermission.QUERY_VALUE,
                           RegistryPermission.ENUM_SUBKEYS,
                           RegistryPermission.NOTIFY,
                           RegistryPermission.WRITE_PERMISSIONS,
                           RegistryPermission.WRITE_OWNER,
                           RegistryPermission.READ_ACCESS,
                           )),
                ActionACE(WNTrustee.EVERYONE,
                          (RegistryPermission.QUERY_VALUE,
                           RegistryPermission.ENUM_SUBKEYS,
                           RegistryPermission.NOTIFY,
                           RegistryPermission.READ_ACCESS,
                           )),
                ActionSetProtectionFlags(
                    dacl=Protection.PROTECTED_NO_COPY,
                    sacl=Protection.NO_CHANGE),
                ActionSetOwner(WNTrustee.ADMINISTRATORS),
            ),
            preowner_action=(ActionSetOwner(WNTrustee.ADMINISTRATORS)),
            combined=False,
        )

    @staticmethod
    def reg_unlock(path):
        """
        Set Inheritance on - clear non-inherited ACEs
        """
        return SetACL(
            path=path,
            object_type=ObjectType.REGISTRY,
            actions=(
                ActionClear(Where.BOTH),
                ActionACE(WNTrustee.EVERYONE, (RegistryPermission.FULL_ACCESS,), where=Where.DACL),
                ActionSetProtectionFlags(
                    #dacl=Protection.NO_PROTECTED,
                    dacl=Protection.PROTECTED_NO_COPY,
                    sacl=Protection.NO_CHANGE),
            ),
            preowner_action=(ActionSetOwner(WNTrustee.ADMINISTRATORS)),
            combined=True,
        )
