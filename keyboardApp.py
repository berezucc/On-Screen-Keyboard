# Nikita Berezyuk
# Keyboard application
# Last update: December 24, 2021
# https://www.tutorialspoint.com/python/python_gui_programming.htm 
# https://www.delftstack.com/howto/python/python-copy-to-clipboard/

import pyperclip as pc # to allow for copy to clipboard feature
from tkinter import *
from tkinter import messagebox

'''Tkinter window'''
window = Tk() # window
window.title('On-Screen Keyboard') # title
window.geometry("1500x900") # size

window.iconbitmap('C:\\Users\\nikit\\Desktop\\Keyboard\\icon.ico') # icon
 

'''Global variables for buttons'''
global mode_IsOn, shift_IsOn, caps_IsOn
mode_IsOn = True
shift_IsOn = False
caps_IsOn = False

'''Class for the second lower half of the screen'''
class KeysOutput:
    '''Initialize'''
    def __init__(self):
        self.outString = ""
        self.lastPressed = ""
        self.current = ""
        self.outputFrame = Frame(window, bg = "#D3DBEC", width = 1300, height = 100, pady = 20)
        self.textBox = Text(self.outputFrame, font = ("Arial", 25), bd = 0, width = 50, height = 7)

    '''Prints out the key pressed by user'''
    def key_press(self,event):
        self.lastPressed = event.keysym
        print("You click this: " + str(event.keysym))
        self.outString = event.char
        self.textBox.config(wrap='none')

    '''Prints out the key pressed by user using on screen keyboard'''
    def key_press_onscreen(self, key):
        global shift_IsOn, caps_IsOn
        # Include functionality of backspace to delete last char
        if key == 'BackSpace':
            #print("Backspaced")
            self.current = self.textBox.get("1.0",END)
            self.textBox.delete("1.0",END)
            self.textBox.insert("1.0", str(self.current[0:-2])) # gets all char from 0 to second last

        # Adds the key inputs into the text box
        else:
            # Collects and deletes previous text to concatenate and output the new text
            self.current = self.textBox.get("1.0",END)
            self.textBox.delete("1.0",END)

            # Checks for keys with 2 possible outputs (hold shift to get the second one)
            if type(key) == tuple:
                if shift_IsOn:
                    key = key[1]
                    shift_IsOn = False
                else:
                    key = key[0]

            # Shift key works for only a single key input, so will be set back to False after another key is pressed
            elif shift_IsOn == True:
                key = key.upper()
                #print("Upper: " + key)
                shift_IsOn = False 
            # Sets all characters to uppercase as long as caps lock is one
            elif caps_IsOn == True:
                key = key.upper()
            # caps lock is off, goes back to lower case
            else:
                key = key.lower()

            # concatenates and inserts to text box
            newstring = str(self.current) + str(key)
            x = newstring.replace("\n", "")
            self.textBox.insert(INSERT, str(x))

    '''Adds the key inputs onto the output box'''
    def output(self):
        # Splitting the frame on the bottom of the screen with the output
        self.outputFrame.grid(row=1,column=0)
        self.textBox.grid(row = 0, column = 0, padx = 20, pady = 5)

    '''Copys the text in the text box to the users clipboard'''
    def copyPaste(self):
        # Create the button
        copy = Button(self.outputFrame, text = "Copy", bg = "#b7dbf7", fg = "black", height = 3, width = 6, command = self.copyFunction)
        copy.grid(row = 0, column = 1, padx = 5)

    def copyFunction(self):
        # gets the current text in text box
        self.current = self.textBox.get("1.0",END)
        pc.copy(str(self.current)) # saves to clipboard
        #print(self.current)

    '''Deletes all the text in the text box'''
    def delete(self):
        # Create the button
        delete = Button(self.outputFrame, text = "Del", bg = "#fc5353", fg = "black", height = 3, width = 6, command = self.deleteFunction)
        delete.grid(row = 0, column = 2, padx = 5)

    def deleteFunction(self):
        # gets the current text in text box and deletes it
        self.textBox.delete("1.0",END)
        
'''Class for upper half of the screen which holds the gui of the onscreen keyboard'''
class OnScreen():
    '''Function that puts all of the keyboard keys on the screen'''
    def __init__(self):
        # Frame on top of the screen that holds the keyboard
        self.mainFrame = Frame(window, height = 500, width = 1750)
        self.mainFrame.grid(row=0,column=0)

        # Object to be used in adding functionality to on screen keys
        self.ko = KeysOutput()

        # Caps lock button
        self.caps = Button()

        # --- Font & Colours ---
        self.font_tuple = ("Arial", 18, "bold")
        self.grey = "#949494"
        self.dark = "#3b3b3b"

    '''Sets shift to True'''
    def shiftButton(self):
        #print("Shift pressed")
        global shift_IsOn
        shift_IsOn = True

    '''Toggle Caps Lock button'''
    def capsLock(self):
        #print("Caps Pressed")
        global caps_IsOn
        # When turned on, text turns blue
        if caps_IsOn == False:
            self.caps.configure(fg = "blue")
            caps_IsOn = True
        # Turned off
        elif caps_IsOn == True:
            self.caps.configure(fg = "black")
            caps_IsOn = False       

    '''Holds all the keys/buttons on the keyboard'''
    def keys(self, font_tuple, grey, dark):
        # --- Keys ---
        # First Row (function row)
        esc = Button(self.mainFrame, text = "Esc", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2)
        esc.grid(column=0, row=0, padx = 2, pady = 2, ipadx = 5)

        f1 = Button(self.mainFrame, text = "F1", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F1"))
        f1.grid(column=2, row=0, padx = 2, pady = 2, ipadx = 5)
        f2 = Button(self.mainFrame, text = "F2", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F2"))
        f2.grid(column=3, row=0, padx = 2, pady = 2, ipadx = 5)
        f3 = Button(self.mainFrame, text = "F3", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F3"))
        f3.grid(column=4, row=0, padx = 2, pady = 2, ipadx = 5)
        f4 = Button(self.mainFrame, text = "F4", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F4"))
        f4.grid(column=5, row=0, padx = 2, pady = 2, ipadx = 5)

        f5 = Button(self.mainFrame, text = "F5", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F5"))
        f5.grid(column=6, row=0, padx = 2, pady = 2, ipadx = 5)
        f6 = Button(self.mainFrame, text = "F6", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F6"))
        f6.grid(column=7, row=0, padx = 2, pady = 2, ipadx = 5)
        f7 = Button(self.mainFrame, text = "F7", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F7"))
        f7.grid(column=8, row=0, padx = 2, pady = 2, ipadx = 5)
        f8 = Button(self.mainFrame, text = "F8", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F8"))
        f8.grid(column=9, row=0, padx = 2, pady = 2, ipadx = 5)

        f9 = Button(self.mainFrame, text = "F9", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F9"))
        f9.grid(column=10, row=0, padx = 2, pady = 2, ipadx = 5)
        f10 = Button(self.mainFrame, text = "F10", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F10"))
        f10.grid(column=11, row=0, padx = 2, pady = 2, ipadx = 5)
        f11 = Button(self.mainFrame, text = "F11", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F11"))
        f11.grid(column=12, row=0, padx = 2, pady = 2, ipadx = 5)
        f12 = Button(self.mainFrame, text = "F12", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("F12"))
        f12.grid(column=13, row=0, padx = 2, pady = 2, ipadx = 5)

        # Second Row
        grave = Button(self.mainFrame, text = "`~", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("`","~")))
        grave.grid(column=0, row=1, padx = 2, pady = 2, ipadx = 5)

        one = Button(self.mainFrame, text = "1!", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("1","!")))
        one.grid(column=1, row=1, padx = 2, pady = 2, ipadx = 5)
        two = Button(self.mainFrame, text = "2@", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("2","@")))
        two.grid(column=2, row=1, padx = 2, pady = 2, ipadx = 5)
        three = Button(self.mainFrame, text = "3#", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("3","#")))
        three.grid(column=3, row=1, padx = 2, pady = 2, ipadx = 5)
        four = Button(self.mainFrame, text = "4$", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("4","$")))
        four.grid(column=4, row=1, padx = 2, pady = 2, ipadx = 5)
        five = Button(self.mainFrame, text = "5%", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("5","%")))
        five.grid(column=5, row=1, padx = 2, pady = 2, ipadx = 5)
        six = Button(self.mainFrame, text = "6^", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("6","^")))
        six.grid(column=6, row=1, padx = 2, pady = 2, ipadx = 5)
        seven = Button(self.mainFrame, text = "7&", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("7","&")))
        seven.grid(column=7, row=1, padx = 2, pady = 2, ipadx = 5)
        eight = Button(self.mainFrame, text = "8*", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("8","*")))
        eight.grid(column=8, row=1, padx = 2, pady = 2, ipadx = 5)
        nine = Button(self.mainFrame, text = "9(", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("9","(")))
        nine.grid(column=9, row=1, padx = 2, pady = 2, ipadx = 5)
        zero = Button(self.mainFrame, text = "0)", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("0",")")))
        zero.grid(column=10, row=1, padx = 2, pady = 2, ipadx = 5)
        dash = Button(self.mainFrame, text = "-_", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("-","_")))
        dash.grid(column=11, row=1, padx = 2, pady = 2, ipadx = 5)
        equals = Button(self.mainFrame, text = "=+", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("=","+")))
        equals.grid(column=12, row=1, padx = 2, pady = 2, ipadx = 5)

        backspace = Button(self.mainFrame, text = "⌫", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("BackSpace"))
        backspace.grid(column=13, row=1, padx = 2, pady = 2, ipadx = 5)

        # Third row
        tab = Button(self.mainFrame, text = "Tab", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("    "))
        tab.grid(column=0, row=2, ipadx = 5, padx = 2, pady = 2)
        q = Button(self.mainFrame, text = "Q", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("q"))
        q.grid(column=1, row=2, ipadx = 5, padx = 2, pady = 2)
        w = Button(self.mainFrame, text = "W", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("w"))
        w.grid(column=2, row=2, ipadx = 5, padx = 2, pady = 2)
        e = Button(self.mainFrame, text = "E", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("e"))
        e.grid(column=3, row=2, ipadx = 5, padx = 2, pady = 2)
        r = Button(self.mainFrame, text = "R", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("r"))
        r.grid(column=4, row=2, ipadx = 5, padx = 2, pady = 2)
        t = Button(self.mainFrame, text = "T", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("t"))
        t.grid(column=5, row=2, ipadx = 5, padx = 2, pady = 2)
        y = Button(self.mainFrame, text = "Y", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("y"))
        y.grid(column=6, row=2, ipadx = 5, padx = 2, pady = 2)
        u = Button(self.mainFrame, text = "U", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("u"))
        u.grid(column=7, row=2, ipadx = 5, padx = 2, pady = 2)
        i = Button(self.mainFrame, text = "I", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("i"))
        i.grid(column=8, row=2, ipadx = 5, padx = 2, pady = 2, columnspan = 1)
        o = Button(self.mainFrame, text = "O", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("o"))
        o.grid(column=9, row=2, ipadx = 5, padx = 2, pady = 2)
        p = Button(self.mainFrame, text = "P", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("p"))
        p.grid(column=10, row=2, ipadx = 5, padx = 2, pady = 2)
        openBracket = Button(self.mainFrame, text = "[ {", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("[","{")))
        openBracket.grid(column=11, row=2, ipadx = 5, padx = 2, pady = 2)
        closeBracket = Button(self.mainFrame, text = "] }", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("]","}")))
        closeBracket.grid(column=12, row=2, ipadx = 5, padx = 2, pady = 2)
        slash = Button(self.mainFrame, text = "\ |", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("\\","|")))
        slash.grid(column=13, row=2, ipadx = 5, padx = 2, pady = 2)

        # Fourth Row
        self.caps = Button(self.mainFrame, text = "Caps", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3, command = self.capsLock)
        self.caps.grid(column=0, row=3, ipadx = 5, padx = 2, pady = 2)
        a = Button(self.mainFrame, text = "A", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("a"))
        a.grid(column=1, row=3, ipadx = 5, padx = 2, pady = 2)
        s = Button(self.mainFrame, text = "S", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("s"))
        s.grid(column=2, row=3, ipadx = 5, padx = 2, pady = 2)
        d = Button(self.mainFrame, text = "D", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("d"))
        d.grid(column=3, row=3, ipadx = 5, padx = 2, pady = 2)
        f = Button(self.mainFrame, text = "F", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("f"))
        f.grid(column=4, row=3, ipadx = 5, padx = 2, pady = 2)
        g = Button(self.mainFrame, text = "G", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("g"))
        g.grid(column=5, row=3, ipadx = 5, padx = 2, pady = 2)
        h = Button(self.mainFrame, text = "H", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("h"))
        h.grid(column=6, row=3, ipadx = 5, padx = 2, pady = 2)
        j = Button(self.mainFrame, text = "J", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("j"))
        j.grid(column=7, row=3, ipadx = 5, padx = 2, pady = 2)
        k = Button(self.mainFrame, text = "K", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("k"))
        k.grid(column=8, row=3, ipadx = 5, padx = 2, pady = 2, columnspan = 1)
        l = Button(self.mainFrame, text = "L", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("l"))
        l.grid(column=9, row=3, ipadx = 5, padx = 2, pady = 2)
        colon = Button(self.mainFrame, text = "; :", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen((";",":")))
        colon.grid(column=10, row=3, ipadx = 5, padx = 2, pady = 2)
        quote = Button(self.mainFrame, text = '''' "''', font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("'",'"')))
        quote.grid(column=11, row=3, ipadx = 5, padx = 2, pady = 2)
        enter = Button(self.mainFrame, text = "Enter", font = font_tuple, bg = grey, fg = "black", height = 1, width = 6, command = lambda: self.ko.key_press_onscreen("\n"))
        enter.grid(column=12, row=3, ipadx = 5, padx = 2, pady = 2, columnspan = 2)

        # Fifth Row
        shift = Button(self.mainFrame, text = "Shift", font = font_tuple, bg = grey, fg = "black", height = 1, width = 6, command = self.shiftButton)
        shift.grid(column=0, row=5, ipadx = 5, padx = 2, pady = 2,columnspan = 2)
        z = Button(self.mainFrame, text = "Z", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("z"))
        z.grid(column=2, row=5, ipadx = 5, padx = 2, pady = 2)
        x = Button(self.mainFrame, text = "X", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("x"))
        x.grid(column=3, row=5, ipadx = 5, padx = 2, pady = 2)
        c = Button(self.mainFrame, text = "C", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("c"))
        c.grid(column=4, row=5, ipadx = 5, padx = 2, pady = 2)
        v = Button(self.mainFrame, text = "V", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("v"))
        v.grid(column=5, row=5, ipadx = 5, padx = 2, pady = 2)
        b = Button(self.mainFrame, text = "B", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("b"))
        b.grid(column=6, row=5, ipadx = 5, padx = 2, pady = 2)
        n = Button(self.mainFrame, text = "N", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("n"))
        n.grid(column=7, row=5, ipadx = 5, padx = 2, pady = 2)
        m = Button(self.mainFrame, text = "M", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("m"))
        m.grid(column=8, row=5, ipadx = 5, padx = 2, pady = 2)
        comma = Button(self.mainFrame, text = ", <", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen((",","<")))
        comma.grid(column=9, row=5, ipadx = 5, padx = 2, pady = 2, columnspan = 1)
        period = Button(self.mainFrame, text = ". >", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen((".",">")))
        period.grid(column=10, row=5, ipadx = 5, padx = 2, pady = 2)
        qsmark = Button(self.mainFrame, text = "/ ?", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen(("/","?")))
        qsmark.grid(column=11, row=5, ipadx = 5, padx = 2, pady = 2)
        shiftR = Button(self.mainFrame, text = "Shift", font = font_tuple, bg = grey, fg = "black", height = 1, width = 6, command = self.shiftButton)
        shiftR.grid(column=12, row=5, ipadx = 5, padx = 2, pady = 2,columnspan = 2)

        # Sixth Row (bottom row)
        ctrl = Button(self.mainFrame, text = "Ctrl", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2)
        ctrl.grid(column=0, row=6, ipadx = 5, padx = 2, pady = 2)
        win = Button(self.mainFrame, text = "⊞", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2, command = lambda: self.ko.key_press_onscreen("⊞"))
        win.grid(column=1, row=6, ipadx = 5, padx = 2, pady = 2)
        alt = Button(self.mainFrame, text = "Alt", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2)
        alt.grid(column=2, row=6, ipadx = 5, padx = 2, pady = 2)

        space = Button(self.mainFrame, font = font_tuple, bg = grey, fg = "black", height = 1, width = 20, command = lambda: self.ko.key_press_onscreen(" "))
        space.grid(column=3, row=6, ipadx = 5, padx = 2, pady = 2,columnspan = 6)

        alt = Button(self.mainFrame, text = "Alt", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2)
        alt.grid(column=9, row=6, ipadx = 5, padx = 2, pady = 2)
        function = Button(self.mainFrame, text = "Fn", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2)
        function.grid(column=10, row=6, ipadx = 5, padx = 2, pady = 2)
        menu = Button(self.mainFrame, text = "Menu", font = font_tuple, bg = grey, fg = "black", height = 1, width = 6)
        menu.grid(column=11, row=6, ipadx = 5, padx = 2, pady = 2,columnspan = 2)
        ctrl = Button(self.mainFrame, text = "Ctrl", font = font_tuple, bg = grey, fg = "black", height = 1, width = 2)
        ctrl.grid(column=13, row=6, ipadx = 5, padx = 2, pady = 2)

        # Miscellaneous Row
        self.mainFrame.grid_columnconfigure(14, minsize=40)  # space between main keyboard and extra keys

        screen = Button(self.mainFrame, text = "PrtSc", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        screen.grid(column=15, row=0, ipadx = 5, padx = 2, pady = 2)
        scroll = Button(self.mainFrame, text = "ScrLk", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        scroll.grid(column=16, row=0, ipadx = 5, padx = 2, pady = 2)
        pause = Button(self.mainFrame, text = "Pause", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        pause.grid(column=17, row=0, ipadx = 5, padx = 2, pady = 2)

        insert = Button(self.mainFrame, text = "Ins", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        insert.grid(column=15, row=1, ipadx = 5, padx = 2, pady = 2)
        home = Button(self.mainFrame, text = "Home", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        home.grid(column=16, row=1, ipadx = 5, padx = 2, pady = 2)
        pageup = Button(self.mainFrame, text = "PgUp", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        pageup.grid(column=17, row=1, ipadx = 5, padx = 2, pady = 2)

        delete = Button(self.mainFrame, text = "Del", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3, command = self.ko.deleteFunction)
        delete.grid(column=15, row=2, ipadx = 5, padx = 2, pady = 2)
        end = Button(self.mainFrame, text = "End", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        end.grid(column=16, row=2, ipadx = 5, padx = 2, pady = 2)
        pagedown = Button(self.mainFrame, text = "PgDn", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        pagedown.grid(column=17, row=2, ipadx = 5, padx = 2, pady = 2)

        up = Button(self.mainFrame, text = "↑", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        up.grid(column=16, row=5, ipadx = 5, padx = 2, pady = 2)
        down = Button(self.mainFrame, text = "↓", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        down.grid(column=16, row=6, ipadx = 5, padx = 2, pady = 2)
        left = Button(self.mainFrame, text = "←", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        left.grid(column=15, row=6, ipadx = 5, padx = 2, pady = 2)
        left = Button(self.mainFrame, text = "→", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3)
        left.grid(column=17, row=6, ipadx = 5, padx = 2, pady = 2)

        # Extras Row
        self.mainFrame.grid_columnconfigure(18, minsize=40)  # space between main keyboard and extra keys
        theme = Button(self.mainFrame, text = "Mode", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3, command = self.modeChange)
        theme.grid(column=19, row=0, ipadx = 5, padx = 2, pady = 2)
        help = Button(self.mainFrame, text = "Help", font = ("Arial", 12, "bold"), bg = grey, fg = "black", height = 2, width = 3, command = self.helpPage)
        help.grid(column=20, row=0, ipadx = 5, padx = 2, pady = 2)
    
    '''Changes modes from light or dark themes (Like an on/off button)'''
    def modeChange(self):
        global mode_IsOn
        # Turns on dark mode
        if mode_IsOn:
            window.config(bg='#212121')
            self.mainFrame.config(bg='#212121')
            self.ko.textBox.config(bg = 'black', fg = 'white')
            self.ko.outputFrame.config(bg = '#141414')
            mode_IsOn = False
        # Turns on light mode
        else:
            window.config(bg='#ffffff')
            self.mainFrame.config(bg='#ffffff')
            self.ko.textBox.config(fg = 'black', bg = 'white')
            self.ko.outputFrame.config(bg = '#D3DBEC')
            mode_IsOn = True

    '''Opens new pop up window will instructions and help page'''
    def helpPage(self):
        # Reads the txt file and saves the text in it
        read = open("help.txt", "r")
        text = read.read()
        read.close()

        # Opens the pop up window with the text
        messagebox.showinfo("Help Page", text)

    '''Main function that runs the window and all visuals on the screen'''
    def main(self):
        # runs the gui
        self.keys(self.font_tuple, self.grey, self.dark)

        # Get each event of keyboard key presses
        window.bind("<Key>", self.ko.key_press)

        # Runs the output functions
        self.ko.output()
        self.ko.copyPaste()
        self.ko.delete()

        # runs the tkinter event loop, runs till program is closed
        window.mainloop()

'''Main block'''
if __name__ == '__main__':
    os = OnScreen()
    os.main()