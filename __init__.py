#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Inotify tools for entries
version 1.0
history:
2013-6-19    dylanninin@gmail.com    init
"""

import pyinotify
from config import blogconfig as config
from service import EntryService

entryService = EntryService()


class EntryEventHandler(pyinotify.ProcessEvent):
    """
    EntryEventHandler monitor entries added, modified or deleted
    """
    def process_default(self, event):
        mask_add = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVE_SELF
        mask_del = pyinotify.IN_DELETE | pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVE_SELF
        if event.mask & mask_add:
            entryService.add_entry(True, event.pathname)
        if event.mask & mask_del:
            entryService.delete_entry(event.pathname)


wm = pyinotify.WatchManager()
mask = pyinotify.ALL_EVENTS
path =  config.entry_dir
notifier = pyinotify.ThreadedNotifier(wm, EntryEventHandler())
wdd = wm.add_watch(path, mask, rec=True)
notifier.start()
