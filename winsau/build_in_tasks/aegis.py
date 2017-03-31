from task import TaskManager, TaskParameter, TaskType, task, step
import os


@task('aegisv1.18', 'aegis v1.18 by https://voat.co/u/thepower')
class AegisTask(object):
    @property
    def user_regpath(self):
        if not self._user_regpath:
            self._user_regpath = TaskManager.user_regload_profile(self._username)
        return self._user_regpath

    def __init__(self, username):
        self._username = username
        self._user_regpath = None

    @step('0', 'take ownership of keys')
    def step_0(self):
        data = (
            r"hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\office\15.0\osm",
            r"hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\office\16.0\osm",
            r"hkey_local_machine\software\($|Wow6432Node\)microsoft\wcmsvc\wifinetworkmanager",
            r"hkey_local_machine\software\($|Wow6432Node\)microsoft\windows\currentversion\windowsupdate\auto update",
            r"hkey_local_machine\software\($|Wow6432Node\)microsoft\windows defender\spynet",
            r"hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\sqmclient\windows",
            r"hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\datacollection",
            r"hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\gwx",
            r"hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\scripteddiagnosticsprovider\policy",
            r"hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\skydrive",
            r"hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\windowsupdate",
            r"hkey_local_machine\system\currentcontrolset\control\wmi\autologger\autoLogger-diagtrack-listener"
        )
        for i in TaskManager.str_unpack(data):
            if TaskManager.reg_exists(i):
                TaskManager.reg_unlock(i)

    @step('1', 'block bad hosts')
    def step_1(self):
        data = (
            "0.r.msn.com", "a.ads1.msn.com", "a.ads2.msn.com", "a.rad.msn.com", "ac3.msn.com", "act-3-blu.mesh.com",
            "activesync.glbdns2.microsoft.com", "ad.doubleclick.net", "ads.eu.msn.com", "ads.msn.com",
            "ads.msn.com.nsatc.net", "ads1.msads.net", "ads1.msn.com", "ads2.msn.com", "ads2.msn.com.c.footprint.net",
            "adsmockarc.azurewebsites.net", "adsyndication.msn.com", "aidps.atdmt.com", "aidps.msn.com.nsatc.net",
            "aka-cdn-ns.adtech.de", "analytics.live.com", "analytics.microsoft.com", "analytics.msn.com",
            "analytics.msnbc.msn.com", "analytics.r.msn.com", "appexmapsappupdate.blob.core.windows.net",
            "arc2.msn.com", "arc3.msn.com", "arc9.msn.com", "atlas.c10r.facebook.com", "b.ads1.msn.com",
            "b.rad.msn.com", "bat.bing.com", "bingads.microsoft.com", "bl3302.storage.skyprod.akadns.net",
            "blu.mobileads.msn.com", "bn1-2cd.wns.windows.com", "bn1cd.wns.windows.com",
            "bn1wns2011508.wns.windows.com", "bn2wns1.wns.windows.com", "bn2wns1b.wns.windows.com",
            "bs.eyeblaster.akadns.net", "bs.serving-sys.com", "c.atdmt.com", "c.atdmt.com.nsatc.net", "c.bing.com",
            "c.microsoft.com", "c.msn.com", "c.msn.com.nsatc.net", "c.ninemsn.com.au", "c.no.msn.com",
            "c1.microsoft.com", "cdn.atdmt.com", "cdn.content.prod.cms.msn.com", "cds26.ams9.msecn.net",
            "choice.microsoft.com", "choice.microsoft.com.nsatc.net", "cmsresources.windowsphone.com",
            "col.mobileads.msn.com", "compatexchange.cloudapp.net", "content.windows.microsoft.com",
            "corp.sts.microsoft.com", "corpext.msitadfs.glbdns2.microsoft.com", "cs1.wpc.v0cdn.net",
            "dart.l.doubleclick.net", "db3aqu.atdmt.com", "dc.services.visualstudio.com", "dev.virtualearth.net",
            "df.telemetry.microsoft.com", "diagnostics.support.microsoft.akadns.net",
            "diagnostics.support.microsoft.com", "digg.analytics.live.com", "directory.services.live.com.akadns.net",
            "displaycatalog.md.mp.microsoft.com", "dl.delivery.mp.microsoft.com", "dmd.metaservices.microsoft.com",
            "#dns.msftncsi.com", "download-ssl.msgamestudios.com", "ecn.dev.virtualearth.net", "en-us.appex-rf.msn.com",
            "fe2.update.microsoft.com.akadns.net", "fe3.delivery.dsp.mp.microsoft.com.nsatc.net",
            "fe3.delivery.mp.microsoft.com", "feedback.microsoft-hohm.com", "feedback.search.microsoft.com",
            "feedback.windows.com", "fesweb1.ch1d.binginternal.com",
            "ff4a487e56259f4bd5831e9e30470e83.azr.msnetworkanalytics.testanalytics.net", "flex.msn.com",
            "flex.msn.com.nsatc.net", "g.msn.com", "g.msn.com.nsatc.net", "geo-prod.do.dsp.mp.microsoft.com",
            "global.msads.net.c.footprint.net", "h1.msn.com", "h2.msn.com", "help.bingads.microsoft.com",
            "i1.services.social.microsoft.com", "i1.services.social.microsoft.com.nsatc.net",
            "inference.location.live.net", "js.microsoft.com", "lb1.www.ms.akadns.net", "licensing.md.mp.microsoft.com",
            "live.rads.msn.com", "livetileedge.dsx.mp.microsoft.com", "logging.windows.microsoft.com", "m.adnxs.com",
            "m.anycast.adnxs.com", "mediadiscovery.microsoft.com", "microsoft-hohm.com", "#msftncsi.com",
            "msnportal.112.2o7.net", "msntest.serving-sys.com", "oca.telemetry.microsoft.com",
            "oca.telemetry.microsoft.com.nsatc.net", "onesettings-bn2.metron.live.com.nsatc.net",
            "onesettings-cy2.metron.live.com.nsatc.net", "onesettings-db5.metron.live.com.nsatc.net",
            "onesettings-hk2.metron.live.com.nsatc.net", "otf.msn.com", "popup.msn.com", "pre.footprintpredict.com",
            "rad.live.com", "rad.msn.com", "rad.msn.com.nsatc.net", "redir.metaservices.microsoft.com",
            "reports.wes.df.telemetry.microsoft.com", "rmads.eu.msn.com", "rmads.msn.com", "rpt.rad.msn.com",
            "sb.scorecardresearch.com", "schemas.microsoft.akadns.net", "secure.adnxs.com", "secure.anycast.adnxs.com",
            "secure.flashtalking.com", "services.wes.df.telemetry.microsoft.com", "settings.data.microsoft.com",
            "settings-sandbox.data.glbdns2.microsoft.com", "settings-sandbox.data.microsoft.com",
            "settings-ssl.xboxlive.com", "settings-win.data.microsoft.com", "sgmetrics.cloudapp.net",
            "shell.windows.com", "siweb.microsoft.akadns.net", "skyapi.skyprod.akadns.net", "sls.update.microsoft.com",
            "sls.update.microsoft.com.akadns.net", "sls.update.microsoft.com.nsatc.net", "sO.2mdn.net",
            "spynet.microsoft.com", "spynet2.microsoft.com", "spynetalt.microsoft.com",
            "sqm.df.telemetry.microsoft.com", "sqm.microsoft.com", "sqm.telemetry.microsoft.com",
            "sqm.telemetry.microsoft.com.nsatc.net", "ssw.live.com", "ssw.live.com.nsatc.net", "static.2mdn.net",
            "static-2mdn-net.l.google.com", "statsfe1.ws.microsoft.com", "statsfe1.ws.microsoft.com.nsatc.net",
            "statsfe2.update.microsoft.com.akadns.net", "statsfe2.ws.microsoft.com",
            "statsfe2.ws.microsoft.com.nsatc.net", "storeedgefd.dsx.mp.microsoft.com",
            "support.msn.microsoft.akadns.net", "survey.watson.microsoft.com", "t.urs.microsoft.com.nsatc.net",
            "t0.ssl.ak.dynamic.tiles.virtualearth.net", "t0.ssl.ak.tiles.virtualearth.net",
            "telecommand.telemetry.microsoft.com", "telecommand.telemetry.microsoft.com.nsatc.net",
            "telemetry.appex.bing.net", "telemetry.appex.search.prod.ms.akadns.net", "telemetry.microsoft.com",
            "telemetry.urs.microsoft.com", "tile-service.weather.microsoft.com", "tlu.dl.delivery.mp.microsoft.com",
            "udc.msn.com", "urs.microsoft.com", "version.hybrid.api.here.com", "view.atdmt.com",
            "vortex.data.microsoft.com", "vortex-bn2.metron.live.com.nsatc.net", "vortex-cy2.metron.live.com.nsatc.net",
            "vortex-hk2.metron.live.com.nsatc.net", "vortex-sandbox.data.glbdns2.microsoft.com",
            "vortex-sandbox.data.microsoft.com", "vortex-win.data.microsoft.com", "w3.b.cap-mii.net", "watson.live.com",
            "watson.microsoft.com", "watson.microsoft.com.nsatc.net", "watson.ppe.telemetry.microsoft.com",
            "watson.telemetry.microsoft.com", "watson.telemetry.microsoft.com.nsatc.net",
            "wes.df.telemetry.microsoft.com", "win10.ipv6.microsoft.com.nsatc.net", "www.modern.ie",
            "www.msftncsi.com",
        )
        for i in TaskManager.str_unpack(data):
            TaskManager.add_host('0.0.0.0', i)

    @step('2', 'configure windows update')
    def step_2(self):
        for key in TaskManager.str_unpack(
                r'hkey_local_machine\software\($|Wow6432Node\)microsoft\windows\currentversion\windowsupdate\auto update'):
            TaskManager.reg_add(key, 'auoptions', 'reg_dword', '2', True)
            TaskManager.reg_add(key, 'enablefeaturedsoftware', 'reg_dword', '0', True)
            TaskManager.reg_add(key, 'includerecommendedupdates', 'reg_dword', '0', True)

    @step('3', 'disable automated delivery of internet explorer')
    def step_3(self):
        pass

    @step('4', 'disable ceip')
    def step_4(self):
        for key in TaskManager.str_unpack(r'hkey_local_machine\software\($|Wow6432Node\)microsoft\sqmclient\windows'):
            TaskManager.reg_add(key, 'ceipenable', 'reg_dword', '0', True)

    @step('5', 'disable gwx')
    def step_5(self):
        for i in ('gwx.exe', 'gwxux.exe'):
            if TaskManager.taskkill(i) not in (True, 128): raise
        TaskManager.reg_add(r'hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\gwx',
                            'disablegwx', 'reg_dword', '1', True)

    @step('6', 'disable remote registry')
    def step_6(self):
        if next(TaskManager.sc_query('remoteregistry'))['state'] == '4':
            TaskManager.net_stop('remoteregistry')
        TaskManager.sc_config('remoteregistry', 'disabled')

    @step('7', 'disable scheduled tasks')
    def step_7(self):
        data = (
            r"\microsoft\windows\application experience\aitagent",
            r"\microsoft\windows\application experience\microsoft compatibility appraiser",
            r"\microsoft\windows\application experience\programdataupdater",
            r"\microsoft\windows\autochk\proxy",
            r"\microsoft\windows\customer experience improvement program\consolidator",
            r"\microsoft\windows\customer experience improvement program\kernelceiptask",
            r"\microsoft\windows\customer experience improvement program\usbceip",
            r"\microsoft\windows\diskdiagnostic\microsoft-windows-diskdiagnosticdatacollector",
            r"\microsoft\windows\maintenance\winsat",
            r"\microsoft\windows\media center\activatewindowssearch",
            r"\microsoft\windows\media center\configureinternettimeservice",
            r"\microsoft\windows\media center\dispatchrecoverytasks",
            r"\microsoft\windows\media center\ehdrminit",
            r"\microsoft\windows\media center\installplayready",
            r"\microsoft\windows\media center\mcupdate",
            r"\microsoft\windows\media center\mediacenterrecoverytask",
            r"\microsoft\windows\media center\objectstorerecoverytask",
            r"\microsoft\windows\media center\ocuractivate",
            r"\microsoft\windows\media center\ocurdiscovery",
            r"\microsoft\windows\media center\pbdadiscovery",
            r"\microsoft\windows\media center\pbdadiscoveryw1",
            r"\microsoft\windows\media center\pbdadiscoveryw2",
            r"\microsoft\windows\media center\pvrrecoverytask",
            r"\microsoft\windows\media center\pvrscheduletask",
            r"\microsoft\windows\media center\registersearch",
            r"\microsoft\windows\media center\reindexsearchroot",
            r"\microsoft\windows\media center\sqlliterecoverytask",
            r"\microsoft\windows\media center\updaterecordpath",
            r"\microsoft\windows\pi\sqm-tasks",
            r"\microsoft\windows\power efficiency diagnostics\analyzeSystem",
            r"\microsoft\windows\setup\gwx\refreshgwxconfigandcontent",
            r"\microsoft\windows\windows error reporting\queuereporting",
        )
        for i in TaskManager.str_unpack(self.step7_data):
            if TaskManager.schtasks_exists(i):
                TaskManager.schtasks_disable(i)

    @step('8', 'disable skydrive')
    def step_8(self):
        for key in TaskManager.str_unpack(
                r'hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\skydrive'):
            TaskManager.reg_add(key, 'disablefilesync', 'reg_dword', '1', True)

    @step('9', 'disable spynet')
    def step_9(self):
        for key in TaskManager.str_unpack(
                r'hkey_local_machine\software\($|Wow6432Node\)microsoft\windows defender\spynet'):
            TaskManager.reg_add(key, 'spynetreporting', 'reg_dword', '0', True)
            TaskManager.reg_add(key, 'submitsamplesconsent', 'reg_dword', '0', True)

    @step('10', 'disable telemetry')
    def step_10(self):
        for key in TaskManager.str_unpack(
                os.path.join(self.user_regpath, r'\software\($|Wow6432Node\)policies\microsoft\office\15.0\osm')):
            TaskManager.reg_add(key, 'enablelogging', 'reg_dword', '0', True)
            TaskManager.reg_add(key, 'enablefileobfuscation', 'reg_dword', '1', True)
            TaskManager.reg_add(key, 'enableupload', 'reg_dword', '0', True)
        for key in TaskManager.str_unpack(
                os.path.join(self.user_regpath, r'\software\($|Wow6432Node\)policies\microsoft\office\16.0\osm')):
            TaskManager.reg_add(key, 'enablelogging', 'reg_dword', '0', True)
            TaskManager.reg_add(key, 'enablefileobfuscation', 'reg_dword', '1', True)
            TaskManager.reg_add(key, 'enableupload', 'reg_dword', '0', True)
        for key in TaskManager.str_unpack(
                r'hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\datacollection'):
            TaskManager.reg_add(key, 'allowtelemetry', 'reg_dword', '0', True)
        for key in TaskManager.str_unpack(
                r'hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\scripteddiagnosticsprovider\policy'):
            TaskManager.reg_add(key, 'enablequeryremoteserver', 'reg_dword', '0', True)

    @step('11', 'disable wifisense')
    def step_11(self):
        for key in TaskManager.str_unpack(
                r'hkey_local_machine\software\($|Wow6432Node\)microsoft\wcmsvc\wifinetworkmanager'):
            TaskManager.reg_add(key, 'wifisensecredshared', 'reg_dword', '0', True)
            TaskManager.reg_add(key, 'wifisenseopen', 'reg_dword', '0', True)

    @step('12', 'disable windows 10 download')
    def step_12(self):
        path = os.path.expandvars(r'%systemdrive%\$windows.~bt')
        TaskManager.dir_placeholder(path, True)
        TaskManager.attrib(path, hidden=True)
        TaskManager.fs_lock(path)

    @step('13', 'disable windows 10 upgrade')
    def step_13(self):
        for key in TaskManager.str_unpack(
                r'hkey_local_machine\software\($|Wow6432Node\)policies\microsoft\windows\windowsupdate'):
            TaskManager.reg_add(key, 'disableosupgrade', 'reg_dword', '1', True)

    @step('14', 'remove diagtrack')
    def step_14(self):
        if next(TaskManager.sc_query('diagtrack'))['state'] == '4':
            TaskManager.net_stop('diagtrack')
        TaskManager.sc_delete('diagtrack')

    @step('15', 'NTP setting')
    def step_15(self):
        pass

    @step('16', 'uninstall and hide updates')
    def step_16(self):
        data_uninstall = [971033, 2882822, 2902907, 2922324, 2952664, 2976978, 2977759, 2990214, 3012973, 3014460,
                          3015249, 3021917, 3022345, 3035583, 3042058, 3044374, 3046480, 3058168, 3064683, 3065987,
                          3065988, 3068708, 3072318, 3074677, 3075249, 3075851, 3075853, 3080149, 3081437, 3081454,
                          3081954, 3083324, 3083325, 3083710, 3083711, 3086255, 3088195, 3090045, 3093983, 3102810,
                          3102812, 3112343, 3112336, 3123862, 3135445, 3135449, 3138612, 3138615, 3139929, 3146449]
        data_hide = [971033, 2882822, 2902907, 2922324, 2952664, 2976978, 2977759, 2990214, 2966583, 3012973, 3014460,
                     3015249, 3021917, 3022345, 3035583, 3042058, 3044374, 3046480, 3058168, 3064683, 3065987, 3065988,
                     3068708, 3072318, 3074677, 3075249, 3075851, 3075853, 3080149, 3081437, 3081454, 3081954, 3083324,
                     3083325, 3083710, 3083711, 3086255, 3088195, 3090045, 3093983, 3102810, 3102812, 3112343, 3112336,
                     3123862, 3135445, 3135449, 3138612, 3138615, 3139929, 3146449, 3150513, 3173040]

        TaskManager.uninstall_updates(data_uninstall)
        TaskManager.ps_hide_updates(data_hide)
        if next(TaskManager.sc_query('wuauserv'))['state'] == '4':
            TaskManager.net_stop('wuauserv')

        if next(TaskManager.sc_query('bits'))['state'] == '4':
            TaskManager.net_stop('bits')

        TaskManager.net_start('bits')
        TaskManager.net_start('wuauserv')