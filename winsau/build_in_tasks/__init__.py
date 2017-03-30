from task import TaskManager, TaskParameter, TaskType
import operations_io as op_io
import operations_process_controller as op_pc
import operations_setacl as op_setacl
import aegis

def create_single_tasks():
    # operations_io.FilesystemOperator
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.find_parent,
        name='dir_parent',
        description='Find a working Directory parent (path)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.add_container,
        name='mk_dir',
        description='Create a Directory (path, [op]forced)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.rem_container,
        name='rm_dir',
        description='Remove a Directory (path, [op]forced)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.rem_object,
        name='rm',
        description='Remove a File (working_path, filename, [op]forced)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.exists,
        name='fs_exists',
        description='Check if File or Directory exists (path)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.lock,
        name='fs_lock',
        description='Lock ACL for File or Directory (path, recursive)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.unlock,
        name='fs_unlock',
        description='Unlock ACL for File or Directory (path, recursive)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.add_container,
        name='dir_placeholder',
        description='Create or replace with an empty Directory (path, [op]forced)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.FilesystemOperator.list,
        name='dir_list',
        description='List Directory (path)',
        task_type=TaskType.SYSTEM,
    )

    # operations_io.RegOperator
    TaskManager.create_single_task(
        func=op_io.RegOperator.find_parent,
        name='reg_parent',
        description='Find a working Key parent (path)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.RegOperator.add_object,
        name='reg_add',
        description='Add registry Key or Value (path, [op]value, [op]regtype(reg_binary|reg_dword|'
                    'reg_dword_little_endian|reg_dword_big_endian|reg_expand_sz|reg_link|reg_multi_sz|'
                    'reg_none|reg_qword|reg_qword_little_endian|reg_sz), [op]data, [op]forced)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.RegOperator.rem_container,
        name='reg_rem',
        description='Remove a Key or Value (path, [op]value, [op]forced)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.RegOperator.exists,
        name='reg_exists',
        description='Check if Key or Value exists (path, [op]value)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.RegOperator.lock,
        name='reg_lock',
        description='Lock ACL for Key (path, recursive)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.RegOperator.unlock,
        name='reg_unlock',
        description='Unlock ACL for Key (path, recursive)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.RegOperator.add_container,
        name='reg_placeholder',
        description='Create or replace with an empty Key (path, [op]forced)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_io.RegOperator.list,
        name='reg_list',
        description='List key (path)',
        task_type=TaskType.SYSTEM,
    )

    #
    #

    # operations_process_controller.WUSAController
    TaskManager.create_single_task(
        func=op_pc.WUSAController.wusa_install,
        name='wusa_install',
        description='Install update (path)',
        task_type=TaskType.SYSTEM,
    )

    # operations_process_controller.WMIController
    TaskManager.create_single_task(
        func=op_pc.WMIController.diskdrive_list,
        name='wmic_diskdrive_list',
        description='List physical disk drive',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.process_list,
        name='wmic_process_list',
        description='List process',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.product_list,
        name='wmic_product_list',
        description='List installation packages',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.nic_list,
        name='wmic_nic_list',
        description='List network interface',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.computersystem_list,
        name='wmic_computersystem_list',
        description='List computer system',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.partition_list,
        name='wmic_partition_list',
        description='List partitions',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.bios_list,
        name='wmic_bios_list',
        description='List BIOS information',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.qfe_list,
        name='wmic_qfe_list',
        description='List Quick Fix Engineering (Patches) information',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.useraccount_list,
        name='wmic_useraccount_list',
        description='List user account information',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.netlogin_list,
        name='wmic_netlogin_list',
        description='List login information',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.startup_list,
        name='wmic_startup_list',
        description='List commands that run automatically at startup',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.share_list,
        name='wmic_share_list',
        description='List of shared resources',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.process_terminate,
        name='wmic_process_terminate',
        description='Terminate a process '
                    '([op]handle_count, [op]name, [op]priority, [op]process_id, [op]thread_count, '
                    '[op]working_set_size)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.WMIController.process_delete,
        name='wmic_process_delete',
        description='Delete a process '
                    '([op]handle_count, [op]name, [op]priority, [op]process_id, [op]thread_count, '
                    '[op]working_set_size)',
        task_type=TaskType.SYSTEM,
    )

    # operations_process_controller.RegController
    TaskManager.create_single_task(
        func=op_pc.RegController.load,
        name='llreg_load',
        description='Load registry resource (key, source)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.RegController.unload,
        name='llreg_unload',
        description='Unload registry resource (key)',
        task_type=TaskType.SYSTEM,
    )

    # operations_process_controller.NetController
    TaskManager.create_single_task(
        func=op_pc.NetController.stop,
        name='net_stop',
        description='Stop service (service)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.NetController.start,
        name='net_start',
        description='Start service (service)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.NetController.user_add,
        name='net_user_add',
        description='Add user (username, change_password)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.NetController.user_delete,
        name='net_user_delete',
        description='Delete user (username)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.NetController.localgroup_user_add,
        name='net_localgroup_user_add',
        description='Add user to group (username, group)',
        task_type=TaskType.SYSTEM,
    )
    # operations_process_controller.SCController
    TaskManager.create_single_task(
        func=op_pc.SCController.query,
        name='sc_query',
        description='Query service ([op]service)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.SCController.config,
        name='sc_config',
        description='Configure service (service, start_mode(auto|disabled))',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.SCController.delete,
        name='sc_delete',
        description='Delete service (service)',
        task_type=TaskType.SYSTEM,
    )

    # operations_process_controller.SchtasksController
    TaskManager.create_single_task(
        func=op_pc.SchtasksController.exists,
        name='schtasks_exists',
        description='Check if task exists (path)',
        task_type=TaskType.SYSTEM,
    )
    TaskManager.create_single_task(
        func=op_pc.SchtasksController.disable,
        name='schtasks_disable',
        description='Disable task (path)',
        task_type=TaskType.SYSTEM,
    )

    # operations_process_controller.TaskkillController
    TaskManager.create_single_task(
        func=op_pc.TaskkillController.taskkill,
        name='taskkill',
        description='Kill process (process)',
        task_type=TaskType.SYSTEM,
    )

    # operations_process_controller.AttribController
    TaskManager.create_single_task(
        func=op_pc.AttribController.attrib,
        name='attrib',
        description='Changes file attributes (path, [op]read_only, [op]hidden, [op]system, [op]recursive)',
        task_type=TaskType.SYSTEM,
    )
    # operations_process_controller.NetstatController
    TaskManager.create_single_task(
        func=op_pc.NetstatController.netstat,
        name='netstat',
        description='Displays protocol statistics and current TCP/IP network connections',
        task_type=TaskType.SYSTEM,
    )