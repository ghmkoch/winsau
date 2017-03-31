import io
import os
import logger
from operations_process_controller import PowerShellController

_logger = logger.Logger().get_logger('operations_static')


def add_host(ipa, ipb):
    fpath = os.path.join(os.environ['systemroot'], 'system32', 'drivers', 'etc', 'hosts')
    with open(fpath, "a+") as f:
        content = f.read()
        if ipb in content:
            return
        f.seek(0, io.SEEK_END)
        f.write("\n{} {}".format(ipa, ipb))

def ps_uninstall_updates(updates):
    ps0 = \
        r"""$computername = $env:computername;$kbnumbers={kbnumbers};$x=0;$hotfixes = get-wmiobject -computername $computername -class win32_quickfixengineering | select hotfixid;foreach ($kbnumber in $kbnumbers) {{$kbid = \"kb\"+$kbnumber;if ($hotfixes -match $kbid) {{$x=1;\" - uninstall kb$kbnumber\";start-process wusa.exe \"/kb:$kbnumber /norestart /quiet /uninstall\" -nonewwindow -wait;}}}}if ($x -eq 0) {{\" - no updates required to be uninstalled\";}}"""
    ps0 = ps0.format(kbnumbers=','.join([str(i) for i in updates]))
    return PowerShellController.command(ps0)

def ps_hide_updates(updates):
    ps0 = \
        r"""$kbnumbers={kbnumbers};$x=0;try {{$updatesession = new-object -comobject microsoft.update.session;$updatesearcher = $updatesession.createupdatesearcher();$updatesearcher.includepotentiallysupersededupdates = $true;$searchresult = $updatesearcher.search(\"isinstalled=0\");foreach ($kbnumber in $kbnumbers) {{[boolean]$kblisted = $false;foreach ($update in $searchresult.updates) {{foreach ($kbarticleid in $update.kbarticleids) {{if ($kbarticleid -eq $kbnumber) {{$kblisted = $true;if ($update.ishidden -eq $false) {{$x=1;\" - hide kb$kbnumber\";$update.ishidden = $true   ;  }}}}}}}}}}}}catch {{}}if ($x -eq 0) {{\" - no updates required to be hidden\";}}$objautoupdatesettings = (new-object -comobject \"microsoft.update.autoupdate\").settings;$objsysinfo = new-object -comobject \"microsoft.update.systeminfo\";if ($objSysInfo.RebootRequired) {{\" - a reboot is required to complete some operations\";}}"""
    ps0 = ps0.format(kbnumbers=','.join([str(i) for i in updates]))
    return PowerShellController.command(ps0)


