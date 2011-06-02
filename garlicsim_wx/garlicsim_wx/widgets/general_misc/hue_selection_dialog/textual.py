# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `Textual` class.

See its documentation for more details.
'''

from __future__ import division
from __future__ import with_statement

import wx

from garlicsim.general_misc import freezers
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim.general_misc.context_managers import ReentrantContextManager


def ratio_to_round_degrees(ratio):
    return int(ratio * 360)


def degrees_to_ratio(degrees):
    return degrees / 360


#class ValueFreezer(ReentrantContextManager):
    #'''
    #Freezer for not changing the `Textual`'s text value.

    #Used as a context manager. Anything that happens inside the `with` suite
    #will not cause the `Textual` to update its text value.
    
    #This is useful because when the `Textual`'s value changes, some platforms
    #automatically select all the text in the `Textual`, which is really
    #annoying if you're just typing in it.
    #'''


class Textual(CutePanel):
    '''Display (and allow modifying) the hue as a number 0-359.'''
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 100))
        self.set_good_background_color()
        self.SetHelpText(
            u'Set the hue in angles (0%s-359%s).' % (unichr(176), unichr(176))
        )
        
        self.hue_selection_dialog = hue_selection_dialog
        #self.hue = hue_selection_dialog.hue
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.hue_static_text = wx.StaticText(self, label='&Hue:')
        
        self.main_v_sizer.Add(self.hue_static_text, 0,
                              wx.ALIGN_LEFT | wx.BOTTOM, border=5)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.h_sizer, 0)
        
        self.spin_ctrl = wx.SpinCtrl(self, min=0, max=359,
                                     initial=77,
                                     size=(70, -1), style=wx.SP_WRAP)
        #if wx_tools.is_mac:
            #self.spin_ctrl.SetValue(ratio_to_round_degrees(self.hue))
        
        self.h_sizer.Add(self.spin_ctrl, 0)
        
        self.degree_static_text = wx.StaticText(self, label=unichr(176))
        
        self.h_sizer.Add(self.degree_static_text, 0)
        
        self.SetSizerAndFit(self.main_v_sizer)
        
        self.Bind(wx.EVT_SPINCTRL, self._on_spin, source=self.spin_ctrl)
        self.Bind(wx.EVT_TEXT, self._on_text, source=self.spin_ctrl)
        #self.Bind(wx.EVT_KILL_FOCUS, self._on_kill_focue)
        
        
    value_freezer = freezers.FreezerProperty()
                    
        
    def update(self):
        '''Update to show the new hue.'''
        if not self.value_freezer.frozen and \
           self.hue != self.hue_selection_dialog.hue:
            self.hue = self.hue_selection_dialog.hue
            self.spin_ctrl.SetValue(ratio_to_round_degrees(self.hue))
    

            
    def _on_spin(self, event):
        self.hue_selection_dialog.setter(
            degrees_to_ratio(self.spin_ctrl.Value)
        )

        
    def _on_text(self, event):
        with self.value_freezer:
            self.hue_selection_dialog.setter(
                degrees_to_ratio(self.spin_ctrl.Value)
            )

            
    #def _on_kill_focus(self, event):
        #assert not self.value_freezer.frozen

            
    def set_focus_on_spin_ctrl_and_select_all(self):
        '''
        
        
        The "select all" part works only on Windows and generic `wx.SpinCtrl`
        implementations.
        '''
        self.spin_ctrl.SetFocus()
        self.spin_ctrl.SetSelection(-1, -1)
        