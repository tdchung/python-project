# !/usr/bin/python
# -*- coding: utf8 -*-

# date:    2019-08-21
# author:  tdchung
# mail:    tdchung.9@gmail.com
#
# update
# 2019-xx-xx
#
#

from __future__ import print_function

import wx
import sys
import os
import io
import subprocess
import time
import re
import csv

from collections import OrderedDict

# user library
sys.path.append("{}/../../commonLib".format(os.path.abspath(__file__).
                                            replace(os.path.basename(__file__), "")))

try:
    from lib_myPrint import MyPrint
    from MyImages import MyImages
except:
    print("Import my print ERROR")


    class MyPrint():
        def __init__(self, logLevel=""):
            pass

        def debug(self, string):
            print("DEBUG: " + str(string))

        def error(self, string):
            print("ERROR: " + str(string))

# my define color
MY_COLOR_BLUE = wx.Colour(51, 51, 255)
MY_COLOR_RED = wx.Colour(255, 51, 51)
MY_COLOR_BLACK = wx.Colour(0, 0, 0)
MY_COLOR_ORANGE = wx.Colour(255, 128, 0)
MY_COLOR_YELLOW = wx.Colour(255, 100, 50)
MY_COLOR_VIOLET = wx.Colour(150, 0, 153)

# from  Test import *


# define class
myPrint = MyPrint(logLevel="info")
myPrint.debug("test print")

version = '1.0'
author = "tdchung.9@gmail.com"

data_json_file = "{}/test_json.json".format(os.path.abspath(__file__).
                                            replace(os.path.basename(__file__), ""))
data_aut_file = "{}/test.aut".format(os.path.abspath(__file__).
                                     replace(os.path.basename(__file__), ""))


def handle_json_data(list_data_in):
    data_out = []
    for data in list_data_in:
        with open(data_json_file, "rb") as json_data:
            for line in json_data:
                myPrint.debug("{}   {}".format(type(line), line))
                if type(line) is not str:
                    try:
                        line = line.decode('utf-8')
                    except:
                        # python 2
                        unicode(line, 'utf-8')
                if data in line:
                    data_out.append(line.strip())
    # return data_out
    return OrderedDict((x, True) for x in data_out).keys()


def handle_aut_data(list_data_in):
    data_out = []
    for data in list_data_in:
        with open(data_aut_file, "rb") as aut_data:
            for line in aut_data:
                # print(type(line))
                # print(type(data))
                myPrint.debug("{}   {}".format(type(line), line))
                if type(line) is not str:
                    try:
                        line = line.decode('utf-8')
                    except:
                        # python 2
                        unicode(line, 'utf-8')
                if data in line:
                    data_out.append(line.strip())
    # return data_out
    # TODO: temp, remove duplicates
    return OrderedDict((x, True) for x in data_out).keys()


class CsvHandler:

    def __init__(self):
        pass

    # ----------------------------------------------------------------------------------------------
    # create csv file without header from txt file. '\t'
    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def create_csv_no_header_from_txt(txt_file_input, csv_file_output):
        """
        holala
        :param txt_file_input: txt file format
        :param csv_file_output:
        :return:
        """
        with open(txt_file_input, "r") as f:
            txt_data = f.read().splitlines()  # get a list a line
        # print(txt_data)
        with open(csv_file_output, "wb") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for line in range(len(txt_data)):
                filewriter.writerow(txt_data[line].split("\t"))

    # ----------------------------------------------------------------------------------------------
    # create csv file without header from list data. '\t'
    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def create_csv_no_header_from_list_data(data_input, csv_file_output):
        """
        holala
        :param data_input: txt file format
        :param csv_file_output:
        :return:
        """
        # print(data_input)
        with open(csv_file_output, "wb") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for line in range(len(data_input)):
                filewriter.writerow(data_input[line].split("\t"))

    # ----------------------------------------------------------------------------------------------
    # create csv file with header from txt file. '\t'
    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def create_csv_w_header_from_txt(txt_file_input, csv_file_output):
        """
        """
        with open(txt_file_input, "r") as f:
            txt_data = f.read().splitlines()  # get a list a line
        # print(txt_data)
        with open(csv_file_output, 'wb') as outcsv:
            writer = csv.DictWriter(outcsv, fieldnames=["Test Name", "Status"])
            writer.writeheader()
            for line in range(len(txt_data)):
                writer.writerow({"Test Name": txt_data[line].split("\t")[0],
                                 "Status": txt_data[line].split("\t")[1]})

    # ----------------------------------------------------------------------------------------------
    # read_csv_no_header
    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def read_csv_no_header(csv_file_input):
        """
        halo 1
        :param csv_file_input:
        :return:    list data
        """
        data_out = []
        with open(csv_file_input, 'rb') as f:
            reader = csv.reader(f)
            # print(reader)
            for row in reader:
                # print(row)      # print debug
                data_out.append(row)
        return data_out

    # ----------------------------------------------------------------------------------------------
    # read_csv_no_header
    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def read_atlas_results(my_atlas_dir):
        """
        :param my_atlas_dir:
        :return:    list data
        """

        re_search_result = r'(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2}).(\w+)\s::\s(\w+\s\w+|\w+)'

        # result_file = "%s/atlas/res/results.txt" % my_atlas_dir
        result_file = "%s" % my_atlas_dir
        data = []
        try:
            with open(result_file, "r") as f:
                for line in f:
                    match = re.search(re_search_result, line)
                    if match is not None:
                        # print(match.group(0))
                        # print(match.group(1))
                        # print(match.group(2))
                        # print(match.group(3))
                        # print(match.group(4))
                        result = match.group(4)
                        if match.group(4) == "OK":
                            result = "PASSED"
                        elif match.group(4) == "ERROR":
                            result = "FAIL"
                        elif match.group(4) == "NOT APPLICABLE":
                            result = "N/A"
                        # # if DoINeedTime is True:
                        # data_line = "%s\t%s\t%s\t%s" % (match.group(1),
                        #                                 match.group(2),
                        #                                 match.group(3),
                        #                                 result)
                        # # else:
                        # #     data_line = "%s\t%s" % (match.group(3), result)
                        # # print(data_line)
                        # data.append(data_line)
                        data.append((match.group(1), match.group(2), result, match.group(3)))
        except Exception as e:
            data = []

        return data


class LetpJson():
    def __init__(self):
        pass

    @staticmethod
    def create_json_out(file_out, data):
        """
        Create json output file for LeTP test
        """
        with open(file_out, 'wb') as my_file:
            my_file.writelines('[\n')
            for i in range(len(data)):
                my_file.writelines("    {\n")
                my_file.writelines("        {}\n".format(data[i]))
                if i is len(data) - 1:
                    my_file.writelines("    }\n")
                else:
                    my_file.writelines("    },\n")
            my_file.writelines(']\n')
        pass

    @staticmethod
    def get_json_file(path):
        """
        Get all LeTP test
        @paramaters
            path              << IN:  path to json test folders
            list_tests_name   >> OUT: list output test name
            list_tests_json   >> OUT: list output test line
        """
        re_info = r'.py::(LE_\w+)'
        list_tests_name = []
        list_tests_json = []
        i = 0
        myPrint.debug("INFO. All file")
        for filename in os.listdir(path):
            i += 1
            myPrint.debug("    {}: {}".format(i, filename))

            with open("{}/{}".format(path, filename), "rb") as json_file:
                myPrint.debug("INFO. Data in file {}".format(filename))
                for line in json_file:
                    if type(line) is not str:
                        line = line.decode("utf-8")
                    line = line.strip()  # TODO: in case type is not str
                    # test case is found
                    ref = re.search(re_info, line)
                    if ref is not None:
                        myPrint.debug("     {}    {}    {}".format(line, type(line), ref.group(1)))
                        # update here
                        list_tests_name.append(ref.group(1))
                        list_tests_json.append(line)

        return list_tests_name, list_tests_json

    def __del__(self):
        pass


class MainFrame(wx.Frame):
    images = MyImages()
    CsvHandler = CsvHandler()
    default_with = 1500
    default_height = 700

    def __init__(self, parent, title='Default GUI', test_list=[]):
        # super(MainFrame, self).__init__(parent,
        # title=title,
        # size=(self.default_with, self.default_height))

        wx.Frame.__init__(self, None, title=title, size=(self.default_with, self.default_height))

        # define
        self.ListControlHeader = ["Test Name", "Status"]
        self.item_index = 0
        self.test_list = test_list

        self.my_paths = [
            "ATLAS  /home/tma/Atlas/Atlas-wp76xx/atlas/res/results.txt",
            "ATLAS  /home/tma/Atlas/Atlas-wp77xx/atlas/res/results.txt",
            "ATLAS  /home/tma/Atlas/Atlas-wp85/atlas/res/results.txt",
            "ATLAS  /home/tma/Atlas/Atlas-wp76xx-Smack/atlas/res/results.txt",
            "ATLAS  /home/tma/Atlas/Atlas-ar758x/atlas/res/results.txt",
            "ATLAS  /home/tma/Atlas/Atlas-ar759x/atlas/res/results.txt",
            "LETP   /home/tma/Atlas/Atlas-wp76xx/qa/letp/log",
            "LETP   /home/tma/Atlas/Atlas-wp77xx/qa/letp/log",
            "LETP   /home/tma/Atlas/Atlas-wp76xx-Smack/qa/letp/log",
            "LETP   /home/tma/Atlas/Atlas-wp85/qa/letp/log",
            "LETP   /home/tma/Atlas/Atlas-ar758x/qa/letp/log",
            "LETP   /home/tma/Atlas/Atlas-ar759x/qa/letp/log",
        ]

        # set icon for application
        try:
            icon = wx.Icon()
            data = self.images.getIconApp()
            bytes_stream = io.BytesIO(data)
            image = wx.Image(bytes_stream)
            icon.CopyFromBitmap(wx.Bitmap(image))
            self.SetIcon(icon)
        except Exception as e:
            myPrint.error(e)
            pass
        # self.SetBackgroundColour('blue')
        # set minimum size
        # self.SetSizeHints(wx.Size(600, 350), wx.DefaultSize)
        self.menu_bar_init()
        self.tool_bar_init()
        self.main_panel_init()
        self.statusBar = self.CreateStatusBar(1)

        # TODO: add exist event to handle if app still in thread

        self.Centre()
        # self.Show()
        self.Layout()

    def menu_bar_init(self):

        # list menu
        menubar = wx.MenuBar()
        filem = wx.Menu()
        editm = wx.Menu()
        optionm = wx.Menu()
        windowm = wx.Menu()

        # list menu in file
        itemNew = wx.MenuItem(filem, wx.ID_ANY, "New", wx.EmptyString, wx.ITEM_NORMAL)
        itemOpen = wx.MenuItem(filem, wx.ID_ANY, "Open", wx.EmptyString, wx.ITEM_NORMAL)
        itemSave = wx.MenuItem(filem, wx.ID_ANY, "Save", wx.EmptyString, wx.ITEM_NORMAL)
        itemSaveAs = wx.MenuItem(filem, wx.ID_ANY, "Save As...", wx.EmptyString, wx.ITEM_NORMAL)
        itemQuit = wx.MenuItem(filem, wx.ID_ANY, "Quit", wx.EmptyString, wx.ITEM_NORMAL)
        filem.Append(itemNew)
        filem.Append(itemOpen)
        filem.AppendSeparator()
        filem.Append(itemSave)
        filem.Append(itemSaveAs)
        filem.AppendSeparator()
        filem.Append(itemQuit)

        # list menu in edit
        itemUndo = wx.MenuItem(editm, wx.ID_ANY, "Undo", wx.EmptyString, wx.ITEM_NORMAL)
        itemRedo = wx.MenuItem(editm, wx.ID_ANY, "Redo", wx.EmptyString, wx.ITEM_NORMAL)
        itemCut = wx.MenuItem(editm, wx.ID_ANY, "Cut", wx.EmptyString, wx.ITEM_NORMAL)
        itemCopy = wx.MenuItem(editm, wx.ID_ANY, "Copy", wx.EmptyString, wx.ITEM_NORMAL)
        itemPaste = wx.MenuItem(editm, wx.ID_ANY, "Paste", wx.EmptyString, wx.ITEM_NORMAL)
        itemDelete = wx.MenuItem(editm, wx.ID_ANY, "Delete", wx.EmptyString, wx.ITEM_NORMAL)
        itemSelectAll = wx.MenuItem(editm, wx.ID_ANY, "Select All", wx.EmptyString, wx.ITEM_NORMAL)
        editm.Append(itemUndo)
        editm.Append(itemRedo)
        editm.AppendSeparator()
        editm.Append(itemCut)
        editm.Append(itemCopy)
        editm.Append(itemPaste)
        editm.Append(itemDelete)
        editm.Append(itemSelectAll)

        # list all menu in options
        itemMoreOptions = wx.MenuItem(optionm, wx.ID_ANY, "More Options",
                                      wx.EmptyString, wx.ITEM_NORMAL)
        itemHelp = wx.MenuItem(optionm, wx.ID_ANY, "Help", wx.EmptyString, wx.ITEM_NORMAL)
        optionm.Append(itemMoreOptions)
        optionm.Append(itemHelp)

        # list all menu in window
        itemWindows = wx.MenuItem(windowm, wx.ID_ANY, "Windows...", wx.EmptyString, wx.ITEM_NORMAL)
        windowm.Append(itemWindows)

        # show menu
        menubar.Append(filem, '&File')
        menubar.Append(editm, '&Edit')
        menubar.Append(optionm, '&Options')
        menubar.Append(windowm, '&Window')
        self.SetMenuBar(menubar)

        # bind events on the menu
        self.Bind(wx.EVT_MENU, self.on_new, itemNew)

        self.Bind(wx.EVT_MENU, self.on_quit, itemQuit)

    def tool_bar_init(self):

        toolBar = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        iconSize = (24, 24)
        toolBar.SetToolBitmapSize(iconSize)

        icon = self.images.getIconNew()
        icon_stream = io.BytesIO(icon)
        toolNew = toolBar.AddTool(wx.ID_ANY, "New",
                                  bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                  shortHelp="New")
        icon_stream.close()

        toolBar.AddSeparator()

        icon = self.images.getIconSave()
        icon_stream = io.BytesIO(icon)
        toolSave = toolBar.AddTool(wx.ID_ANY, "Save",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Save")
        icon_stream.close()

        toolBar.AddSeparator()

        icon = self.images.getIconClear()
        icon_stream = io.BytesIO(icon)
        toolClear = toolBar.AddTool(wx.ID_ANY, "Save",
                                    bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                    shortHelp="Clear Logs")
        icon_stream.close()

        toolBar.AddSeparator()
        toolBar.AddSeparator()

        icon = self.images.getIconHelp()
        icon_stream = io.BytesIO(icon)
        toolHelp = toolBar.AddTool(wx.ID_ANY, "Help",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Help")
        icon_stream.close()

        toolBar.AddSeparator()
        icon = self.images.getIconQuit()
        icon_stream = io.BytesIO(icon)
        toolQuit = toolBar.AddTool(wx.ID_ANY, "Quit",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Quit")
        icon_stream.close()

        del icon, icon_stream

        toolBar.Realize()

        # bind events on the tools
        self.Bind(wx.EVT_TOOL, self.on_quit, toolQuit)
        self.Bind(wx.EVT_MENU, self.on_save, toolSave)
        self.Bind(wx.EVT_TOOL, self.on_clear, toolClear)
        self.Bind(wx.EVT_MENU, self.on_help, toolHelp)
        self.Bind(wx.EVT_TOOL, self.on_new, toolNew)

    def main_panel_init(self):

        self.splitter = wx.SplitterWindow(self,
                                          -1,
                                          style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

        # MAIN PANEL HERE
        self.main_panel = wx.Panel(self.splitter)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticLine(self.main_panel), 0, wx.ALL | wx.EXPAND, 0)

        # 2019-11-08, Add function get result from Atlas/letp logs
        hbox_result = wx.BoxSizer(wx.HORIZONTAL)
        # self.tCtrl_path = wx.TextCtrl(self.main_panel,style=(wx.TE_RICH2 | wx.EXPAND))
        self.tCtrl_path = wx.ComboBox(self.main_panel, id=-1, value=self.my_paths[0],
                                      style=wx.TE_RICH2 | wx.EXPAND,
                                      choices=self.my_paths)
        self.openfile_button = wx.Button(self.main_panel, label='...', size=(40, 27))
        self.framework_type_data = ["Atlas", "LeTP", "reserved"]
        self.framework_type = wx.ComboBox(self.main_panel, id=-1, value=self.framework_type_data[0],
                                          style=wx.CB_READONLY,
                                          choices=self.framework_type_data)
        self.result_button = wx.Button(self.main_panel, label='Get result', size=(140, 30))
        hbox_result.Add(wx.StaticText(self.main_panel, label="Path:", name="."), 1, wx.ALIGN_CENTER)
        hbox_result.Add(self.tCtrl_path, wx.ALL | wx.EXPAND, 10)
        hbox_result.Add(self.openfile_button, wx.ALL | wx.BOTTOM, 10)
        hbox_result.AddSpacer((100))
        hbox_result.Add(self.framework_type, wx.ALL, 10)
        hbox_result.Add(self.result_button, wx.ALL, 10)
        vbox.Add(hbox_result, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        # End 2019-11-08

        vbox.Add(wx.StaticLine(self.main_panel), 0, wx.ALL | wx.EXPAND, 0)
        # test = wx.StaticText(self.main_panel, label="Logs:", name="..")
        vbox.AddSpacer((20))
        my_label = "Ver: {}                Author: {}".format(version, author)
        vbox.Add(wx.StaticText(self.main_panel, label=my_label, name=".."), 0, wx.ALIGN_RIGHT)
        vbox.Add(wx.StaticLine(self.main_panel), 0, wx.ALL | wx.EXPAND, 0)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.tCtrl1 = wx.TextCtrl(self.main_panel,
                                  size=(self.default_with / 4 * 3, self.default_height * 2),
                                  style=(wx.TE_MULTILINE | wx.TE_READONLY
                                         | wx.TE_RICH2 | wx.EXPAND))
        fgs = wx.FlexGridSizer(1, 1, 5, 5)
        fgs.Add(self.tCtrl1, 1, wx.EXPAND)
        fgs.AddGrowableCol(0, 0)
        hbox1.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        vbox.Add((-1, 5))
        self.main_panel.SetSizer(vbox)

        # LEFT PANEL HERE
        self.left_panel = wx.Panel(self.splitter)
        vbox_list = wx.BoxSizer(wx.VERTICAL)
        vbox_list.Add(wx.StaticLine(self.left_panel), 0, wx.ALL | wx.EXPAND, 0)

        self.static_box = wx.StaticBox(self.left_panel, id=-1, label="Infomation")
        self.static_box_sizer = wx.StaticBoxSizer(self.static_box, orient=wx.HORIZONTAL)
        # self.btn1 = wx.Button(self.left_panel, label='btn1 ...', size=(140, 30))

        self.aut_data = [".aut", ".json", ".sh", "reserved"]
        self.aut_type = wx.ComboBox(self.left_panel, id=-1, value=self.aut_data[0],
                                    style=wx.CB_READONLY,
                                    choices=self.aut_data)
        self.generate = wx.Button(self.left_panel, label='GEN ...', size=(140, 30))
        # self.static_box_sizer.Add(self.btn1, wx.ALL | wx.EXPAND, 10)
        self.static_box_sizer.Add(self.aut_type, wx.ALL | wx.EXPAND, 10)
        self.static_box_sizer.AddSpacer((30))
        self.static_box_sizer.Add(self.generate, wx.ALL | wx.EXPAND, 10)

        self.test_name_ctrl = wx.TextCtrl(self.left_panel,
                                          # TODO: will update height of this field. auto size
                                          size=(self.default_with / 4, 1000),
                                          style=(wx.TE_MULTILINE | wx.TE_RICH2))

        self.clear_left = wx.Button(self.left_panel, label='clear', size=(140, 30))

        fgs2 = wx.FlexGridSizer(4, 1, 5, 5)
        fgs2.Add(self.static_box_sizer, 0, 0)
        fgs2.Add(wx.StaticText(self.left_panel, id=-1, label="List test name", name="__"),
                 1,
                 wx.ALIGN_CENTER)
        fgs2.Add(self.test_name_ctrl, 1, wx.ALIGN_TOP | wx.EXPAND)
        fgs2.Add(self.clear_left, 1, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
        fgs2.AddGrowableRow(3)
        vbox_list.Add(fgs2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        vbox_list.Add((-1, 5))
        self.left_panel.SetSizer(vbox_list)

        # Set splitter
        self.splitter.SplitVertically(self.left_panel, self.main_panel, 320)
        self.splitter.SetMinimumPaneSize(200)

        # self.Bind(wx.EVT_BUTTON, self.btn1_event, self.btn1)
        # self.Bind(wx.EVT_BUTTON, self.btn2_event, self.btn2)
        # self.Bind(wx.EVT_BUTTON, self.btn3_event, self.btn3)
        self.Bind(wx.EVT_BUTTON, self.generate_event, self.generate)
        self.Bind(wx.EVT_BUTTON, self.clear_left_event, self.clear_left)
        self.Bind(wx.EVT_BUTTON, self.openfile_btn_event, self.openfile_button)
        self.Bind(wx.EVT_BUTTON, self.result_button_event, self.result_button)

    def list_control_add_new(self, data):
        '''
        :param data: ["test_name", "result"]
        :return:
        '''
        # TODO: test here
        self.my_list_control.Append(data)
        if self.item_index % 2:
            self.my_list_control.SetItemBackgroundColour(self.item_index, "white")
        else:
            self.my_list_control.SetItemBackgroundColour(self.item_index, "gray")
        self.item_index += 1

    # --- Even ---
    def on_new(self, evt):
        # TODO: test
        self.list_control_add_new(["test_", "NO RUN"])

    def on_save(self, evt):
        # TODO: test Here

        test = Test(self.test_list, self.tCtrl1)
        test.start()

        # redirect text here
        # sys.stdout = self.tCtrl1
        # for i in range(100):
        #     print("(MainFrame.py:14110): Gdk-WARNING **: MainFrame.py:
        #     Fatal IO error 11 (Resource temporarily unavailable) on X server :0")

    def on_clear(self, evt):
        # TODO: test
        # self.my_list_control.DeleteAllItems()
        # self.item_index = 0
        # TODO
        # self.test_name_ctrl.Clear()
        self.tCtrl1.Clear()
        pass

    def on_help(self, evt):
        pass

    def on_quit(self, evt):
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
                                wx.YES_NO | wx.ICON_EXCLAMATION)
        _response = dial.ShowModal()
        if _response == wx.ID_YES:
            self.Close(True)
        else:
            return 0

    def openfile_btn_event(self, evt):
        # If Atlas framework
        if self.framework_type.GetSelection() is 0:
            with wx.FileDialog(self, "Open txt file",
                               wildcard="Excel files (*.txt)|*.txt|All file (*.*)|*.*",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind
                # Proceed loading the file chosen by the user
                pathname = fileDialog.GetPath()
                self.my_paths.append("ATLAS  {}".format(str(pathname)))
                self.tCtrl_path.Append("ATLAS  {}".format(str(pathname)))
                self.tCtrl_path.SetSelection(self.tCtrl_path.GetCount() - 1)
        # LeTP framework
        elif self.framework_type.GetSelection() is 1:
            with wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE) as dirDialog:
                if dirDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind
                # Proceed loading the file chosen by the user
                pathname = dirDialog.GetPath()
                self.my_paths.append("LETP   {}".format(str(pathname)))
                self.tCtrl_path.Append("LETP   {}".format(str(pathname)))
                self.tCtrl_path.SetSelection(self.tCtrl_path.GetCount() - 1)

        else:  # Not deploy yet
            pass

    def result_button_event(self, evt):
        self.tCtrl1.Clear()
        data = []
        print(self.tCtrl_path.GetValue())
        re_response = re.search(r"(ATLAS|LETP)\s+([^\n|\s]+)",
                                self.tCtrl_path.GetValue())
        if re_response is None:
            myPrint.error("Not correct format")
        else:
            myPrint.debug(re_response.group(1))
            myPrint.debug(re_response.group(2))
            if re_response.group(1) == "ATLAS":
                data = self.CsvHandler.read_atlas_results(re_response.group(2))
            elif re_response.group(1) == "LETP":
                # reRunPy
                reRun = r"(\d+)_(\d+)_(\w+).log"
                reRunPy = r"(\d+)_(\d+)_(le_\w+)_py.log"
                reRunJson = r"(\d+)_(\d+)_(le_\w+)_json.log"
                reRunTest = r"(\d+)_(\d+)_(LE_\w+).log"
                for filename in os.listdir(re_response.group(2)):
                    myPrint.debug(filename)
                    # check result:
                    founded = False
                    out_re = re.match(reRun, filename)
                    with open("{}/{}".format(re_response.group(2), filename), 'rb') as myfile:
                        for line in myfile:
                            if founded:
                                testre = re.search(r"(PASSED|FAIL)\s([^\n|\s]+::(\w+))",
                                                   line.decode("utf-8"))
                                # print(testre)
                                if testre is not None:
                                    myPrint.debug("    --->{} {} {}".format(testre.group(1),
                                                                            testre.group(2),
                                                                            testre.group(3)))
                                    date = "{}-{}-{}".format(out_re.group(1)[0:4],
                                                             out_re.group(1)[4:6],
                                                             out_re.group(1)[6:])
                                    time = "{}-{}-{}".format(out_re.group(2)[0:2],
                                                             out_re.group(2)[2:4],
                                                             out_re.group(2)[4:])
                                    data.append((date, time, testre.group(1),
                                                 testre.group(3), testre.group(2)))
                                else:
                                    break
                            if not founded and re.search("short test summary info",
                                                         line.decode("utf-8")):
                                founded = True

            else:
                myPrint.error("Not correct framework")

            # add to GUI
            self.tCtrl1.Clear()

            def sortTime(val):
                return val[1]

            def sortDate(val):
                return val[0]

            data.sort(key=sortTime)
            data.sort(key=sortDate)
            for i in data:
                if i[2] == "PASSED":
                    self.tCtrl1.SetDefaultStyle(wx.TextAttr(MY_COLOR_BLUE))
                    self.tCtrl1.AppendText("{}\t{}\t{}\t{}\n".format(i[0], i[1], i[3], i[2]))
                elif i[2] == "FAIL":
                    self.tCtrl1.SetDefaultStyle(wx.TextAttr(MY_COLOR_RED))
                    self.tCtrl1.AppendText("{}\t{}\t{}\t{}\n".format(i[0], i[1], i[3], "FAILED"))
                elif i[2] == "N/A":
                    self.tCtrl1.SetDefaultStyle(wx.TextAttr(MY_COLOR_VIOLET))
                    self.tCtrl1.AppendText("{}\t{}\t{}\t{}\n".format(i[0], i[1], i[3], i[2]))
                else:
                    self.tCtrl1.SetDefaultStyle(wx.TextAttr(MY_COLOR_BLACK))
                    self.tCtrl1.AppendText("{}\t{}\t{}\t{}\n".format(i[0], i[1], i[3], i[2]))

    def btn1_event(self, evt):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()

    def btn2_event(self, evt):
        pass

    def btn3_event(self, evt):
        pass

    def clear_left_event(self, evt):
        self.test_name_ctrl.Clear()

    def generate_event(self, evt):
        start_time = time.time()
        myPrint.debug("EVENT")
        myPrint.debug(self.aut_type.GetSelection())
        myPrint.debug(self.aut_type.GetStringSelection())

        data_in = self.test_name_ctrl.GetValue()
        # myPrint.debug(data_in)
        data_in = data_in.split("\n")
        # myPrint.debug(data_in)
        my_data_in = []
        for line in data_in:
            if re.search(r"LE_\w+", line) is not None:
                myPrint.debug("{}   {}".format(line.strip(), type(line)))
                my_data_in.append(line.strip())

        self.tCtrl1.Clear()

        # generate the .json file to run in LeTP framework
        if self.aut_type.GetSelection() is 1:
            data = handle_json_data(my_data_in)
            myPrint.debug(data)
            if data == []:
                self.tCtrl1.AppendText("None")
            else:
                self.tCtrl1.SetDefaultStyle(wx.TextAttr(MY_COLOR_VIOLET))
                # for data_line in data:
                #     self.tCtrl1.AppendText("{}\n".format(data_line))
                self.tCtrl1.AppendText('[\n')
                for i in range(len(data)):
                    self.tCtrl1.AppendText("    {\n")
                    self.tCtrl1.AppendText("        {}\n".format(data[i]))
                    if i is len(data) - 1:
                        self.tCtrl1.AppendText("    }\n")
                    else:
                        self.tCtrl1.AppendText("    },\n")
                self.tCtrl1.AppendText(']\n')

        # generate .aut file test run with Atlas framework
        elif self.aut_type.GetSelection() is 0:
            data = handle_aut_data(my_data_in)
            myPrint.debug(data)
            if data == []:
                self.tCtrl1.AppendText("None")
            else:
                self.tCtrl1.SetDefaultStyle(wx.TextAttr(MY_COLOR_BLUE))
                self.tCtrl1.AppendText('<?xml version="1.0" encoding="utf-8"?>\n')
                self.tCtrl1.AppendText('<tokens>\n')
                for data_line in data:
                    self.tCtrl1.AppendText("{}\n".format(data_line))
                self.tCtrl1.AppendText('</tokens>\n')

        # generate bash script to test with letp
        elif self.aut_type.GetSelection() is 2:

            data = handle_json_data(my_data_in)
            if data == []:
                self.tCtrl1.AppendText("None")
            else:
                self.tCtrl1.SetDefaultStyle(wx.TextAttr(MY_COLOR_YELLOW))
                # for data_line in data:
                #     self.tCtrl1.AppendText("{}\n".format(data_line))
                self.tCtrl1.AppendText('#!/bin/bash\n')
                self.tCtrl1.AppendText('VERSION=1.0\n')
                # clean folder
                self.tCtrl1.AppendText('rm -r *.update; rm -r _*\n')
                for data_line in data:
                    self.tCtrl1.AppendText("letp -o run {} -r fp\n".format(data_line.split('"')[3]))

        else:
            pass

        myPrint.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    app = wx.App()
    main_frame = MainFrame(None, test_list=["test_script.py"])
    main_frame.Show()
    app.MainLoop()
