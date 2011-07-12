# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `NavigationPanel` class.

See its documentation for more info.
'''

import os
import sys
import glob
import pkgutil
import itertools
import collections

import wx
import wx.lib.dialogs
import pkg_resources

from garlicsim.general_misc.comparison_tools import underscore_hating_key
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc.wx_tools.keyboard import keys
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim_wx.widgets.general_misc.cute_bitmap_button import \
                                                            CuteBitmapButton
from garlicsim_wx.widgets.general_misc.cute_dir_dialog import CuteDirDialog
from garlicsim_wx.misc.simpack_place import SimpackPlace

import garlicsim_wx

from . import filter_box as filter_box_module

from . import images as __images_package
images_package = __images_package.__name__

# blocktodo: Back and forward buttons should be grayed out sometimes.


class NavigationPanel(CutePanel):
    '''
    Panel for navigating between simpacks.
    
    It contains a filter/search box, back and forward buttons, and an "Add\
    simpacks from a different folder" button.
    '''
    def __init__(self, simpack_selection_dialog):
        CutePanel.__init__(
            self,
            simpack_selection_dialog,
        )
        
        self.simpack_selection_dialog = simpack_selection_dialog
        assert isinstance(self.simpack_selection_dialog,
                          SimpackSelectionDialog)
        
        self._back_queue = collections.deque()
        self._forward_queue  = collections.deque()
        
        self.SetBackgroundColour(
            self.simpack_selection_dialog.GetBackgroundColour()
        )
        
        self.big_v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.big_v_sizer)
        
        self.add_simpacks_from_a_different_folder_button = wx.Button(
            self,
            label='&Add simpacks from a different folder...'
        )
        self.add_simpacks_from_a_different_folder_button.SetHelpText(
            "By default, GarlicSim lets you use simpacks that are included in "
            "GarlicSim's simpack library. If you want to use a different "
            "simpack, press this button and choose the folder that *contains* "
            "your simpack."
        )
        self.big_v_sizer.Add(
            self.add_simpacks_from_a_different_folder_button,
            proportion=0,
            flag=wx.EXPAND | wx.ALL,
            border=5
        )
        
        self.small_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.big_v_sizer.Add(
            self.small_h_sizer,
            proportion=0,
            flag=wx.EXPAND
        )
        
        ### Building filter box: ##############################################
        #                                                                     #
        
        self.filter_sizer = wx.BoxSizer(wx.VERTICAL)
        self.small_h_sizer.Add(
            self.filter_sizer,
            proportion=1,
            flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT,
            border=5
        )
        
        self.filter_static_text = wx.StaticText(
            self,
            label='&Filter simpacks:'
        )
        self.filter_static_text.SetHelpText(filter_box_module.filter_help_text)
        self.filter_sizer.Add(
            self.filter_static_text,
            proportion=1,
            flag=wx.ALIGN_LEFT | wx.TOP,
            border=5,
        )
            
        
        # blocktodo: if `wx.SearchCtrl` doesn't give us everything we need, can
        # find something else.
        # blocktodo: not getting enough padding for the search control on Mac
        self.filter_box = filter_box_module.FilterBox(self)
        self.filter_sizer.Add(
            self.filter_box,
            proportion=0,
            flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
            border=5,
        )
        #                                                                     #
        ### Finished building filter box. #####################################
        
        ### Building back and forward buttons: ################################
        #                                                                     #
        
        # Two peculiar things about how we're binding events here, both due to
        # accelerator weirdnesses:
        #  1. We're binding events to the parent instead of the current widget
        #     because otherwise accelerators don't work on parent on GTK.
        #  2. We're binding both button events *and* menu events, because on 
        #     Mac accelerators can only trigger menu events.
        
        self.back_button = CuteBitmapButton(
            self,
            bitmap=wx_tools.bitmap_tools.bitmap_from_pkg_resources(
                images_package,
                'back.png'
            ),
            tool_tip=(u'Back (%s)' % wx_tools.keyboard.keys.back_key_string),
            help_text=(u'Go to the previously-selected simpack. (%s)' %
                       keys.back_key_string)
        )
        
        self.small_h_sizer.Add(
            self.back_button,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
        )
        
        self.forward_button = CuteBitmapButton(
            self,
            bitmap=wx_tools.bitmap_tools.bitmap_from_pkg_resources(
                images_package,
                'forward.png'
            ),
            tool_tip=(u'Forward (%s)' %
                      wx_tools.keyboard.keys.forward_key_string),
            help_text=(u'Go to the simpack you visited before you hit the '
                       'back button. (%s)' % keys.forward_key_string)
        )
        self.small_h_sizer.Add(
            self.forward_button,
            proportion=0,
            flag=wx.ALL | wx.ALIGN_BOTTOM,
            border=5
        )
        #                                                                     #
        ### Finished building back and forward buttons. #######################
        
        if wx_tools.is_mac:
            self.big_v_sizer.AddSpacer(
                MAC_BOTTOM_SPACING_SIZE
            )
        
        self.simpack_selection_dialog.add_accelerators(
            {wx_tools.keyboard.keys.back_keys: self.back_button.Id,
             wx_tools.keyboard.keys.forward_keys: self.forward_button.Id}
        )
        
        self.bind_event_handlers(NavigationPanel)

            
    def back(self):
        '''Go to the previously-selected simpack.'''
        assert self._back_queue
        current_simpack_metadata = \
                                 self.simpack_selection_dialog.simpack_metadata
        if current_simpack_metadata is not None:
            self._forward_queue.append(current_simpack_metadata)
        new_simpack_metadata = self._back_queue.pop()
        self._set_simpack_metadata_ignoring_history(new_simpack_metadata)
    
    
    def forward(self):
        '''Go to the simpack that was selected before we hit "Back".'''
        assert self._forward_queue
        current_simpack_metadata = \
                                 self.simpack_selection_dialog.simpack_metadata
        if current_simpack_metadata is not None:
            self._back_queue.append(current_simpack_metadata)
        new_simpack_metadata = self._forward_queue.pop()
        self._set_simpack_metadata_ignoring_history(new_simpack_metadata)

        
    def set_simpack_metadata(self, simpack_metadata):
        if not self._should_accept_new_simpack_metadata(simpack_metadata):
            return
        
        self._forward_queue.clear()
        current_simpack_metadata = \
                                 self.simpack_selection_dialog.simpack_metadata
        if current_simpack_metadata is not None:
            self._back_queue.append(current_simpack_metadata)
                        
        self._set_simpack_metadata_ignoring_history(simpack_metadata)

        
    def _set_simpack_metadata_ignoring_history(self, simpack_metadata):
        if not self._should_accept_new_simpack_metadata(simpack_metadata):
            return
        self.simpack_selection_dialog.simpack_metadata = simpack_metadata
        self.simpack_selection_dialog.refresh()

        
    def _should_accept_new_simpack_metadata(self, simpack_metadata):
        current_simpack_metadata = \
                                 self.simpack_selection_dialog.simpack_metadata
        if simpack_metadata is current_simpack_metadata:
            return False
        elif (simpack_metadata is not None) and simpack_metadata not in \
             list(itertools.chain(*self.simpack_selection_dialog.simpack_tree.
                                  _simpack_places_tree.values())):
            return False
        else:
            return True
        

    def refresh(self):
        self.back_button.Enable(bool(self._back_queue))
        self.forward_button.Enable(bool(self._forward_queue))
        
    
    ### Event handlers: #######################################################
    #                                                                         #
        
    def _on_add_simpacks_from_a_different_folder_button(self, event):
        path = CuteDirDialog.create_show_modal_and_get_path(
            self.simpack_selection_dialog,
            'Choose the folder that *contains* your simpack(s), not the '
            'simpack folder itself.',
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        )
        
        if path is None:
            return
            
        if path not in zip(garlicsim_wx.simpack_places)[0]:
            garlicsim_wx.simpack_places.append(SimpackPlace(path, ''))
        if path not in sys.path:
            sys.path.append(path)
        self.simpack_selection_dialog.simpack_tree.reload_tree()
    
    #                                                                         #
    ### Finished event handlers. ##############################################

from .simpack_selection_dialog import (SimpackSelectionDialog,
                                       MAC_BOTTOM_SPACING_SIZE)