# from __future__ import print_function
# import time

string = """


I want a wx.TextCtrl to take the entire remaining width of a panel. It is placed with a wx.StaticText and a wx.Button in a horizontal wx.BoxSizer in a vertical wx.BoxSizer in a wx.lib.scrolledpanel.ScrolledPanel (which is self below):

# create TextCtrl
self.fileNameInput = wx.TextCtrl (self, style=wx.TE_PROCESS_ENTER)
# create horizontal sizer with 3 items
self.fileNameSizer = wx.BoxSizer (wx.HORIZONTAL)
self.fileNameSizer.Add (wx.StaticText (self, -1, 'none'), flag=(wx.ALIGN_CENTER_VERTICAL))
self.fileNameSizer.Add (self.fileNameInput, proportion=1, flag=(wx.EXPAND | wx.ALIGN_CENTER_VERTICAL))
self.fileNameSizer.Add (wx.Button (self, label='Button'), flag=(wx.ALIGN_CENTER_VERTICAL))
# create vertical sizer
self.SetSizer (wx.BoxSizer (wx.VERTICAL))
self.GetSizer ().Add (self.fileNameSizer)

Neither proportion nor wx.EXPAND help to make the TextCtrl larger, presumably because the sizer looks at the TextCtrls own width. But I did not find any style or flag for the `'TextCtrl' to make it variable-width..?

Thanks for ideas!

EDIT: Replaced "..." by something working
wxpython width textctrl
shareimprove this question
edited Dec 6 '13 at 8:56
asked Dec 5 '13 at 18:03
virtualnobi
77599 silver badges2727 bronze badges

    2
    You'll get more answers if you make it easier for people. This would be much easier to answer if you posted a self-contained minimal example that would actually run. I think I know what's wrong, but I don't want to post an answer until I check it, and I'm not going to spend all time replacing "..."s, etc. – tom10 Dec 6 '13 at 5:27 

@tom10: thanks for being so thorough, but I wanted to keep uninteresting stuff outside and assumed I would be able to figure out the details if I get a hint from someone who thinks he knows what's wrong... :-| Anyway, I replaced the ...s – virtualnobi Dec 6 '13 at 8:58
1
It would be very helpful if you create self-contained minimal runnable example which demonstrates the problem. Similar to my answer. – Fenikso Dec 6 '13 at 9:19

"""


# string = """
# python thread example
# threading timer python
# thread module in python
# threading trong python
# Knowing When A Python Thread Has Died - A. Jesse Jiryu Davis
# """


for i in range(10):
    safe_print(string)
    time.sleep(2)