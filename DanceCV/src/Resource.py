# -*- coding: utf-8 -*-

import os

class Resource():
    def __init__(self, dataPath = os.path.join("..", "data")):
        self.dataPath = dataPath

    def fileName(self, *name, **args):
        if not args.get("writable", False):
            readOnlyPath = os.path.join(self.dataPath, *name)

            if os.path.isfile(readOnlyPath):
                return readOnlyPath
            return readOnlyPath
        else:
            readOnlyPath = os.path.join(self.dataPath, *name)
            try:
                # First see if we can write to the original file
                if os.access(readOnlyPath, os.W_OK):
                    return readOnlyPath
                # If the original file does not exist, see if we can write to its directory
                if not os.path.isfile(readOnlyPath) and os.access(os.path.dirname(readOnlyPath), os.W_OK):
                    return readOnlyPath
            except:
                raise
