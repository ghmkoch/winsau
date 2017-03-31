from task import TaskManager, TaskType

from operations_process_controller import WMIController, RegController
from operations_io import RegOperator

import os


def get_sid(username):
    return [i['SID'] for i in WMIController.useraccount_list() if i['Name'] == username][0]


def get_homepath(username):
    return next(
        RegOperator.list(
            r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\{}'.format(get_sid(username)),
            'ProfileImagePath'
        ))['data']


def get_regpath(username):
    return os.path.join('HKEY_USERS', get_sid(username))


def regload_profile(username):
    regpath = get_regpath(username)
    if RegOperator.exists(regpath):
        return regpath
    RegController.load(
        regpath,
        os.path.join(get_homepath(username), 'NTUSER.DAT')
    )
    return regpath


def regunload_profile(username):
    regpath = get_regpath(username)
    if not RegOperator.exists(regpath):
        return
    RegController.unload(regpath)


TaskManager.create_single_task(
    func=staticmethod(get_sid),
    name='user_get_sid',
    description='Get user sid (username)',
    task_type=TaskType.FRAMEWORK,
)
TaskManager.create_single_task(
    func=staticmethod(get_homepath),
    name='user_get_homepath',
    description='Get user homepath (username)',
    task_type=TaskType.FRAMEWORK,
)
TaskManager.create_single_task(
    func=staticmethod(get_regpath),
    name='user_get_regpath',
    description='Get user reg path (username)',
    task_type=TaskType.FRAMEWORK,
)
TaskManager.create_single_task(
    func=staticmethod(regload_profile),
    name='user_regload_profile',
    description='Load user profile into registry if not yet loaded (username)',
    task_type=TaskType.FRAMEWORK,
)
TaskManager.create_single_task(
    func=staticmethod(regunload_profile),
    name='user_regunload_profile',
    description='Unoad user profile into registry if not yet unloaded (username)',
    task_type=TaskType.FRAMEWORK,
)
