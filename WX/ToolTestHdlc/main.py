#!/usr/bin/python
# -*- coding: utf8 -*-

# date:    2019
# author:  tdchung
# mail:    tdchung.9@gmail.com
#
#           tooltesthdlc.py
#
# update
# 2019-         1.0           Create

from __future__ import print_function
import sys
import os
import glob
import io
import wx
import serial
import time
from threading import Thread


# user lib
ROOT = "{}../..".format(os.path.abspath(__file__).replace(os.path.basename(__file__), ""))
sys.path.append("{}/commonLib".format(ROOT))

from lib_myPrint import MyPrint
from MyImages import MyImages


def serial_ports():
    """ Lists serial port names
        https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        # result.append(port)
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# --------------------------------------------------------------------------------------------------
# MainFrame
# --------------------------------------------------------------------------------------------------
class MainFrame(wx.Frame):

    images = MyImages()
    MyPrint = MyPrint()

    DoINeedTime = True
    ExcelTestOnly = False
    data_tests = []

    def __init__(self, parent, title='Default GUI'):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        # set icon for application
        try:
            icon = wx.Icon()
            data = self.images.getIconApp()
            self.MyPrint.debug(data)
            bytes_stream = io.BytesIO(data)
            self.MyPrint.debug(bytes_stream)
            image = wx.Image(bytes_stream)
            self.MyPrint.debug(image)
            icon.CopyFromBitmap(wx.Bitmap(image))
            self.SetIcon(icon)

        except Exception as e:
            self.MyPrint.error(e)
            pass
        # self.SetBackgroundColour('blue')
        # set minimum size
        self.SetSizeHints(wx.Size(800, 600), wx.DefaultSize)

        self.list_com = serial_ports()
        self.data_tpye = ["String", "Hex", "Binary"]
        self.baudrate = ['4800', '9600', '14400', '19200',
                         '38400', '57600', '115200', '128000', '256000']

        self.isSerialConnected = False
        self.mySerial = None


        self.menu_bar_init()
        self.tool_bar_init()
        self.main_panel_init()
        self.statusBar = self.CreateStatusBar(1)
        self.Centre()
        self.Show()

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
        itemMoreOptions = wx.MenuItem(optionm,
                                      wx.ID_ANY,
                                      "More Options",
                                      wx.EmptyString,
                                      wx.ITEM_NORMAL)
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

        # toolNew = toolBar.AddLabelTool( wx.ID_ANY, u"New",
        # wx.Bitmap('icon\\new.png'), shortHelp="New" )
        icon = self.images.getIconNew()
        icon_stream = io.BytesIO(icon)
        toolNew = toolBar.AddTool(wx.ID_ANY, "New",
                                  bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                  shortHelp="New")
        icon_stream.close()

        toolBar.AddSeparator()

        # toolSave = toolBar.AddLabelTool( wx.ID_ANY, u"Save",
        #  wx.Bitmap('icon\\save.png'), shortHelp="Save"  )
        icon = self.images.getIconSave()
        icon_stream = io.BytesIO(icon)
        toolSave = toolBar.AddTool(wx.ID_ANY, "Save",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Save")
        icon_stream.close()

        toolBar.AddSeparator()

        # toolClear = toolBar.AddLabelTool( wx.ID_ANY, u"Save",
        # wx.Bitmap('icon\\clear4.png'), shortHelp="Clear Logs" )
        icon = self.images.getIconClear()
        icon_stream = io.BytesIO(icon)
        toolClear = toolBar.AddTool(wx.ID_ANY, "Save",
                                    bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                    shortHelp="Clear Logs")
        icon_stream.close()

        toolBar.AddSeparator()
        toolBar.AddSeparator()

        # toolHelp = toolBar.AddLabelTool( wx.ID_ANY, u"Help",
        #  wx.Bitmap('icon\\help.png'), shortHelp="Help"  )
        icon = self.images.getIconHelp()
        icon_stream = io.BytesIO(icon)
        toolHelp = toolBar.AddTool(wx.ID_ANY, "Help",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Help")
        icon_stream.close()

        toolBar.AddSeparator()
        # toolQuit = toolBar.AddLabelTool( wx.ID_ANY, u"Quit",
        # wx.Bitmap('icon\\quit.png'), shortHelp="Quit"  )
        icon = self.images.getIconQuit()
        icon_stream = io.BytesIO(icon)
        toolQuit = toolBar.AddTool(wx.ID_ANY, "Quit",
                                   bitmap=wx.Bitmap(wx.Image(icon_stream)),
                                   shortHelp="Quit")
        icon_stream.close()

        # del icon, icon_stream

        toolBar.Realize()

        # bind events on the tools
        self.Bind(wx.EVT_TOOL, self.on_quit, toolQuit)
        self.Bind(wx.EVT_MENU, self.on_save, toolSave)
        self.Bind(wx.EVT_TOOL, self.on_clear, toolClear)
        self.Bind(wx.EVT_MENU, self.on_help, toolHelp)
        self.Bind(wx.EVT_TOOL, self.on_new, toolNew)

    def main_panel_init(self):

        self.panel = wx.Panel(self)

        # font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font = wx.Font(pointSize=12,
                       family=wx.FONTFAMILY_SCRIPT,
                       style=wx.FONTSTYLE_NORMAL,
                       weight=wx.FONTWEIGHT_BOLD)
        # btnfont = wx.Font(pixelSize = 10, wx.MODERN, wx.NORMAL, wx.BOLD)
        # toofont = wx.Font(pixelSize = 9, wx.MODERN, wx.SLANT , wx.BOLD)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticLine(self.panel), 0, wx.ALL | wx.EXPAND, 0)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sText1 = wx.StaticText(self.panel, label='COM config:', size=(100, 20))
        self.sText1.SetFont(font)
        self.sText_com = wx.StaticText(self.panel, label='  Ports:', size=(-1, 20))
        self.cbox_com_port = wx.ComboBox(self.panel,
                                         choices=self.list_com,
                                         value=self.list_com[-1],
                                         size=(150, 25),)
                                         # style=wx.CB_READONLY)
        self.sText_baudrate = wx.StaticText(self.panel, label='  baudrate:', size=(-1, 20))
        self.cbox_baudrate = wx.ComboBox(self.panel,
                                         choices=self.baudrate,
                                         value=self.baudrate[6],
                                         size=(150, 25),)
                                         # style=wx.CB_READONLY)
        self.sText_values = wx.StaticText(self.panel, label='  8N1  ', size=(-1, 20))
        self.btn_connect = wx.Button(self.panel, label='Connect', size=(100, 25))
        fgs = wx.FlexGridSizer(1, 7, 3, 3)
        fgs.AddMany([(self.sText1, 1, wx.ALIGN_BOTTOM),
                     (self.sText_com, 1, wx.ALIGN_BOTTOM),
                     (self.cbox_com_port, 1, wx.EXPAND | wx.ALIGN_BOTTOM),
                     (self.sText_baudrate, 1, wx.ALIGN_BOTTOM),
                     (self.cbox_baudrate, 1, wx.EXPAND | wx.ALIGN_BOTTOM),
                     (self.sText_values, 1, wx.ALIGN_BOTTOM),
                     (self.btn_connect, 1, wx.EXPAND | wx.ALIGN_BOTTOM)])
        fgs.AddGrowableCol(2, 1)
        hbox1.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        vbox.Add((-1, 5))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sText2 = wx.StaticText(self.panel, label='Send Data:', size=(100, 20))
        self.sText2.SetFont(font)
        self.tCtrl2 = wx.TextCtrl(self.panel)
        self.cbox_data_type = wx.ComboBox(self.panel,
                                          choices=self.data_tpye,
                                          value=self.data_tpye[0],
                                          size=(100, 25),
                                          style=wx.CB_READONLY)
        fgs2 = wx.FlexGridSizer(1, 3, 5, 10)
        fgs2.AddMany([(self.sText2, 1, wx.ALIGN_BOTTOM), (self.tCtrl2, 1, wx.EXPAND),
                      (self.cbox_data_type, 1, wx.ALIGN_BOTTOM)])
        fgs2.AddGrowableCol(1, 1)
        hbox2.Add(fgs2, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        vbox.Add((-1, 5))

        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_send = wx.Button(self.panel, label='Send', size=(70, 30))
        self.btn_r1 = wx.Button(self.panel, label='Bnt_R1', size=(70, 30))
        self.btn_r2 = wx.Button(self.panel, label='Bnt_R2', size=(70, 30))
        gs = wx.GridSizer(1, 5, 5, 5)
        gs.Add(self.btn_send, 0, wx.EXPAND)
        gs.Add(self.btn_r1, 0, wx.EXPAND)
        gs.Add(self.btn_r2, 0, wx.EXPAND)
        hbox6.Add(gs, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        vbox.Add(hbox6, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.ALIGN_BOTTOM, border=2)
        vbox.Add((-1, 5))


        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.tCtrl_log = wx.TextCtrl(self.panel, size=(1000, 1000),
                                     style=(wx.TE_MULTILINE | wx.TE_READONLY |
                                            wx.TE_RICH2 | wx.EXPAND))
        fgs7 = wx.GridSizer(1, 1, 0, 0)
        fgs7.AddMany([(self.tCtrl_log, 1, wx.EXPAND)])
        hbox7.Add(fgs7, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        vbox.Add(hbox7, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=2)
        vbox.Add((-1, 5))

        self.panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.btn_connect_event, self.btn_connect)
        self.Bind(wx.EVT_BUTTON, self.btn_send_event, self.btn_send)
        # self.Bind(wx.EVT_BUTTON, self.btn2_event, self.btn2)
        # self.Bind(wx.EVT_BUTTON, self.btn3_event, self.btn3)
        # self.Bind(wx.EVT_BUTTON, self.btn4_event, self.btn4)
        # self.Bind(wx.EVT_COMBOBOX, self.cblistSelect_event, self.cblistSelect)
        # self.Bind(wx.EVT_COMBOBOX, self.cblistResult_event, self.cblistResult)

    # --- Even ---
    def on_new(self, evt):
        pass

    def on_save(self, evt):
        pass

    def on_clear(self, evt):
        self.tCtrl_log.Clear()
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

    def _my_serial_thread(self):
        out = ""
        # self.MyPrint.debug("thread")
        # while self.isSerialConnected:
        # TODO:
        while True:
            # i = self.mySerial.in_waiting
            # if i < 1:
            #     time.sleep(0.001)
            #     continue
            # self.MyPrint.debug(out)
            # out += self.mySerial.read(10)

            # self.MyPrint.debug(self.mySerial.read(100))
            while self.mySerial.in_waiting:
                time.sleep(.0001)
                self.MyPrint.debug(self.mySerial.read(self.mySerial.inWaiting()))


    def connect_serial(self, com, baudrate):
        try:
            self.mySerial = serial.Serial(port=com, baudrate=int(baudrate))
        except serial.SerialException:
            self.MyPrint.debug("Base class for serial port exceptions.")
            return False
        except ValueError:
            self.MyPrint.debug("ValueError")
            return False
        self.MyPrint.debug("Connected at {}".format(self.mySerial))
        self.reader = Thread(target=self._my_serial_thread)
        self.reader.setDaemon(True)
        self.reader.start()
        return True

    def disconnect_serial(self):
        self.mySerial.close()
        self.MyPrint.debug("Disconnected at {}".format(self.mySerial))
        self.mySerial = None
        self.reader.join()
        return True

    def btn_connect_event(self, evt):

        if not self.isSerialConnected:
            self.MyPrint.debug("Connecting to {}, baudrate {}".format(self.cbox_com_port.GetValue(),
                                                                      self.cbox_baudrate.GetValue())
                               )
            if self.connect_serial(self.cbox_com_port.GetValue(), self.cbox_baudrate.GetValue()):
                self.btn_connect.SetLabel("Disconnect")
                self.isSerialConnected = True
                # TODO:
        else:
            self.MyPrint.debug("Disconnecting")
            if self.disconnect_serial():
                self.btn_connect.SetLabel("Connect")
                self.isSerialConnected = False
        pass

    def btn_send_event(self, evt):
        if self.isSerialConnected:
            value = self.tCtrl2.GetValue()
            if value:
                # TODO: check value format
                value_format = self.cbox_data_type.GetValue()
                self.MyPrint.debug("Sending value: {} ### format: {}".format(value, value_format))

            else:
                self.MyPrint.debug("Value is empty. Nth to do")
            # clear imput form
            self.tCtrl2.Clear()
        else:
            self.MyPrint.error("Serial port is not open")
        pass

    def btn2_event(self, evt):
        data = self.CsvHandler.read_atlas_results(self.tCtrl1.GetValue())
        if not self.DoINeedTime:
            for i in range(0, len(data)):
                data[i] = "%s\t%s" % (data[i].split('\t')[2], data[i].split('\t')[3])
                self.MyPrint.debug(data[i])
            pass
        self.pre_logs()
        if len(data) is 0:
            self.my_print_text("File is not available\n", MY_COLOR_RED)
            self.MyPrint.warn("File is not available")
        else:
            self.my_print_status(data, self.get_print_status())
        self.data_tests = data

    # open excel file
    def btn3_event(self, evt):
        if self.tCtrl2.GetValue() == "":
            self.MyPrint.debug("tCtrl2 is None")
            total_tests, data = self.MyExcelQC.open_excel_file()
        else:
            self.MyPrint.debug("tCtrl2 have value")
            total_tests, data = self.MyExcelQC.open_excel_file(self.tCtrl2.GetValue())

        # if self.ExcelTestOnly:
        #     for i in range(0, len(data)):
        #         data[i] = "%s" % data[i].split('\t')[1]
        #         self.MyPrint.debug(data[i])

        self.pre_logs()
        self.my_print_text("Total tests: %d\n" % total_tests, MY_COLOR_ORANGE)
        self.my_print_status(data, self.get_print_status())
        self.data_tests = data
        pass

    def btn4_event(self, evt):
        self.MyPrint.debug("Create data CSV file")
        with wx.FileDialog(self, "Open excel file",
                           wildcard="Csv files (*.csv)|*.csv|All file (*.*)|*.*",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.MyPrint.debug("CSV file path: %s" % pathname)

            # TODO:
            if not os.path.exists(pathname):
                pass
            self.pre_logs()
            self.my_print_text("Create the CSV data to file: %s\n" % pathname, MY_COLOR_ORANGE)
            self.my_print_text("List Data:\n", MY_COLOR_ORANGE)
            self.my_print_status(self.data_tests, self.get_print_status())
            self.CsvHandler.create_csv_no_header_from_list_data(self.data_tests, pathname)
        pass

    def cblistSelect_event(self, evt):
        # TODO: ---------------
        self.MyPrint.debug("Combo Box event received")

    def cblistResult_event(self, evt):
        self.MyPrint.debug("Result Combo Box event received")
        if "FULL" == self.cblistResult.GetValue():
            self.MyPrint.debug("Change to print full time")
            self.DoINeedTime = True
            self.ExcelTestOnly = False
        elif "Result Only" == self.cblistResult.GetValue():
            self.MyPrint.debug("Print result only")
            self.DoINeedTime = False
            self.ExcelTestOnly = False
        elif "Excel tests" == self.cblistResult.GetValue():
            self.MyPrint.debug("Print result only")
            self.DoINeedTime = False
            self.ExcelTestOnly = True
        else:
            self.MyPrint.debug("Invalid")

    def __del__(self):
        if self.mySerial is not None:
            self.mySerial.close()


if __name__ == '__main__':
    app = wx.App()
    MainFrame(None)
    app.MainLoop()
