from task import TaskManager, TaskParameter, TaskType, task, step


@task('aegis', '')
class AegisTask(object):
    ph_step0_data = (
        r"HKEY_LOCAL_MACHINE\software\policies\microsoft\office\15.0\osm",
        r"HKEY_LOCAL_MACHINE\software\policies\microsoft\office\16.0\osm",
        r"hkey_local_machine\software\microsoft\wcmsvc\wifinetworkmanager",
        r"hkey_local_machine\software\microsoft\windows\currentversion\windowsupdate\auto update",
        r"hkey_local_machine\software\microsoft\windows defender\spynet",
        r"hkey_local_machine\software\policies\microsoft\sqmclient\windows",
        r"hkey_local_machine\software\policies\microsoft\windows\datacollection",
        r"hkey_local_machine\software\policies\microsoft\windows\gwx",
        r"hkey_local_machine\software\policies\microsoft\windows\scripteddiagnosticsprovider\policy",
        r"hkey_local_machine\software\policies\microsoft\windows\skydrive",
        r"hkey_local_machine\software\policies\microsoft\windows\windowsupdate",
        r"hkey_local_machine\system\currentcontrolset\control\wmi\autologger\autoLogger-diagtrack-listener",
    )

    def __init__(self, step0_data=ph_step0_data):
        self.step0_data = step0_data

    @step('0', 'take ownership of keys')
    def step_0(self):
        for i in self.step0_data:
            if TaskManager.reg_exists(i): TaskManager.reg_unlock(i)
