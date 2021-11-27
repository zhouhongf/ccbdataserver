# encoding=utf-8
import win32serviceutil
import win32service
import win32event
import win32evtlogutil
import winerror
import servicemanager
import time
import sys
import os
import threading
from server import app


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def thread_target():
    app.run(host='0.0.0.0', port=9005, debug=True)


class PyDataService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PyDataService"  # 服务名
    _svc_display_name_ = "Python Data Service"  # 服务在windows系统中显示的名称
    _svc_description_ = "This is a python data service for ccb"  # 服务的描述

    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.run = True

    def SvcDoRun(self):
        th = threading.Thread(target=thread_target)
        th.start()
        try:
            while self.run:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            pass

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(PyDataService)
            servicemanager.Initialize('PyDataService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(PyDataService)

