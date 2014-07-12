#!/usr/bin/python
import sys
import os
if 'MY_HOME' not in os.environ:
    os.environ['MY_HOME']='/usr/libexec/pi-web-agent'
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/toolkit')
sys.path.append(os.environ['MY_HOME']+'/etc/config')
sys.path.append(os.environ['MY_HOME']+'/cgi-bin/chrome')
sys.path.append(os.environ['MY_HOME']+'/objects')
import cgi
import cgitb
cgitb.enable()
from framework import view, output
from live_info import hostname
from live_info import execute
from DependableExtension import DependableExtension
EXTENSION_ID='VNC'

class VNCManager(DependableExtension):
    
    def __init__(self):
        DependableExtension.__init__(self, EXTENSION_ID)
        self.service = 'sudo /etc/init.d/vncboot '    

    def isServiceActive(self):
        arg = 'status'        
        return self._service_action(arg) == 0
            
    def startService(self):
        arg = 'start'
        return self._service_action(arg) == 0
    
    def stopService(self):
        arg = 'stop'
        return self._service_action(arg) == 0

    def restartService(self):
        arg = 'restart'
        return self._service_action(arg) == 0

    def _service_action(self, action):
        output, ret_code = \
            execute(self.service + action)
        return ret_code
    
    def _generateActiveView(self):
        onoffswitch = 'Service status: <div class="onoffswitch">\n' +\
        '<input disabled="disabled" type="checkbox" name="vncboot" ' + \
        'class="onoffswitch-checkbox" id="vncservice" checked/>' +\
        '<label class="onoffswitch-label" for="vncservice">\n' +\
        '<div class="onoffswitch-inner"></div>\n' +\
        '<div class="onoffswitch-switch"></div>\n</label></div>\n'
        html = '<a id="startViewer" class="btn btn-primary" ' +\
        'href="/utilities/viewer-applet-example.html" ' + \
        'onclick="window.open(this.href); return false;"> ' + \
        'Start VNC</a>'
        html = onoffswitch + '</ br>' + html
        return html

    def _generateDisabledView(self):
        onoffswitch = 'Start VNC viewer by executing: /etc/init.d/vncboot start <div class="onoffswitch">\n' +\
        '<input disabled="disabled" type="checkbox" name="vncboot" ' + \
        'class="onoffswitch-checkbox" id="vncservice"/>' +\
        '<label class="onoffswitch-label" for="vncservice">\n' +\
        '<div class="onoffswitch-inner"></div>\n' +\
        '<div class="onoffswitch-switch"></div>\n</label></div>\n'
        html = '<a id="startViewer" class="btn btn-primary" disabled="true"' +\
        'href="#">Start VNC</a>'
        html = onoffswitch + '</ br>' + html
        return html

    def generateView(self):
        if (not self.check_status()):
            return self._generateMissingDependencies()
        if self.isServiceActive():
            return self._generateActiveView()
        return self._generateDisabledView()
        
    def _generateMissingDependencies(self):
        return "The dependencies of this module are missing. Do you want to install them?"

def main():
    vncMgr = VNCManager()
    html = vncMgr.generateView()
    view.setContent('VNC Viewer', html)
    output(view, cgi.FieldStorage())

if __name__ == '__main__':
    main()
