# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
tododoc
'''

import wx


class NotMainProgramWarningDialog(wx.MessageDialog): 
    
    def __init__(self, frame):
   
        content = '''\
GarlicSim has detected that it's not being run as the main program. (Perhaps you have imported it from another script?)

If this is the case, it will probably not succeed in starting another instance of GarlicSim, which is needed for the action you just tried to do. It can try to continue, but it might not work. If you want to be safe from this problem, run GarlicSim by itself, not importing it from another script.

Do you want to try to continue?'''
        
        wx.MessageDialog.__init__(
            self,
            frame,
            content,
            'Warning',
            wx.YES_NO | wx.ICON_EXCLAMATION
        )
        