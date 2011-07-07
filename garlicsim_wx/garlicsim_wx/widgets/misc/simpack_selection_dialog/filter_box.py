# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''
import wx

from garlicsim_wx.widgets.general_misc.cute_control import CuteControl


filter_help_text = ('Type text in the filter box in order to filter the '
                    'simpacks. You will see only the simpacks that contain '
                    'the text that you typed. For example, type "Physics" '
                    'in order to see only Physics-related simpacks.')


class FilterBox(wx.SearchCtrl, CuteControl):
    def __init__(self, navigation_panel):
        wx.SearchCtrl.__init__(self, navigation_panel)
        self.ShowCancelButton(True)
        self.SetDescriptiveText('')
        self.SetHelpText(filter_help_text) add emitter
        
    filter_words = property(
        lambda self: self.Value.split()
    )