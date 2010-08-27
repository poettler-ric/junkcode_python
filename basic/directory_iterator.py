#!/usr/bin/python

"""
Test how to iterate over a folder-like structure.
"""

class Folder:
    def __init__(self, name, parent=None, files=(), folders=()):
        self.name = name
        self.parent = parent
        if parent:
            parent.folders.add(self)
        self.files = set(files)
        self.folders = set(folders)

    def __repr__(self):
        return "<folder: %s>" % (self.name)

class File:
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        folder.files.add(self)

    def __repr__(self):
        return "<file: %s>" % (self.name)


"""
create folder structure:
root
    sub_1
        sub_1_1
            file_1
            file_2
            file_3
        sub_1_2
            file_4
            file_5
        sub_1_3
    sub_2
    sub_3
        sub_3_1
        sub_3_2
            file_6
            file_7
        file_8
        file_9
    sub_4
        sub_4_1
            file_10
            file_11
"""

root = Folder("root")

sub_1 = Folder("sub_1", root)
sub_1_1 = Folder("sub_1_1", sub_1)
sub_1_2 = Folder("sub_1_2", sub_1)
sub_1_3 = Folder("sub_1_3", sub_1)

sub_2 = Folder("sub_2", root)

sub_3 = Folder("sub_3", root)
sub_3_1 = Folder("sub_3_1", sub_3)
sub_3_2 = Folder("sub_3_2", sub_3)

sub_4 = Folder("sub_4", root)
sub_4_1 = Folder("sub_4_1", sub_4)

# create files in folders
File("file_1", sub_1_1)
File("file_2", sub_1_1)
File("file_3", sub_1_1)

File("file_4", sub_1_2)
File("file_5", sub_1_2)

File("file_6", sub_3_2)
File("file_7", sub_3_2)

File("file_8", sub_3)
File("file_9", sub_3)

File("file_10", sub_4_1)
File("file_11", sub_4_1)

# iterate over the folders and files

def iterate_folders(root, intention=""):
    new_intention = intention + "  "
    for folder in root.folders:
        print intention + str(folder)
        iterate_folders(folder, new_intention)
    for file in root.files:
        print intention + str(file)

iterate_folders(root)
