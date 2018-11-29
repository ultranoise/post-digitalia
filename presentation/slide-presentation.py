
#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import urwid
import urwid.raw_display

PY = 'python yellow'
PB = 'python blue'
PS = 'python surround'
PW = 'python shadow'
PC = 'pycon'
PCI = 'pycon in edge'
PCO = 'pycon out edge'
PCW = 'pycon shadow'
URI = 'urwid in edge'
URO = 'urwid out edge'
URW = 'urwid shadow'
FB = 'footer border'
FL = 'footer left'
FD = 'footer division'
FR = 'footer right'
FRH = 'footer right highlight'
UR = 'urwid'
SLG = 'slide gray'
SLR = 'slide red'
SLY = 'slide yellow'
SLB = 'slide blue'
CF = 'check focus'
BT = 'button'
BTF = 'button focus'
BTW = 'button shadow'
ED = 'edit'
EDF = 'edit focus'
EDC = 'edit caption'
EDW = 'edit shadow'

palette = [
    (PS,    'white', 'light gray',  '', '#fff', '#ddd'),
    (PY,    'white', 'brown',       '', '#fff', '#fd6'),
    (PB,    'white', 'dark blue',   '', '#fff', '#68a'),
    (PW,    'white', 'black',       '', '#fff', '#666'),
    (PC,    'black', 'brown',       '', 'black', '#fd6'),
    (PCI,   'white', 'brown',       '', '#fff', '#fd6'),
    (PCO,   'white', 'light gray',  '', '#fff', '#ddd'),
    (PCW,   'white', 'black',       '', '#fff', '#666'),
    (UR,    'light blue', 'dark blue', '', '#68f', '#008'),
    (URI,   'white', 'dark blue',   '', '#fff', '#008'),
    (URO,   'white', 'light gray',  '', '#fff', '#ddd'),
    (URW,   'white', 'black',       '', '#fff', '#666'),
    (FB,    'black', 'light gray',  '', 'black', '#ddd'),
    (FL,    'black', 'brown',       '', '#000', '#fd6'),
    (FR,    'white', 'dark blue',   '', '#fff', '#68a'),
    (FRH,   'light blue', 'dark blue', '', '#8ef,bold', '#68a'),
    (FD,    'black', 'dark blue',   '', 'black', '#68a'),
    (SLG,   'light gray', 'dark cyan',  '', '#666', 'g95'),
    (SLR,   'white', 'dark red',    '', '#fff', '#f88'),
    (SLY,   'white', 'brown',       '', '#fff', '#ff8'),
    (SLB,   'white', 'dark blue',   '', '#fff', '#88f'),
    (BT,    'black', 'dark cyan',   '', '#000', '#8ad'),
    (BTF,   'black', 'dark green',  '', '#000', '#fd6'),
    (BTW,   'dark gray', 'light gray', '', '#666', '#ddd'),
    (CF,    'black', 'dark green',  '', '#000', '#fd6'),
    (ED,    'black', 'dark cyan',   '', '#000', '#8ad'),
    (EDF,   'black', 'dark green',  '', '#000', '#fd6'),
    (EDC,   'black', 'light gray',  '', '#000', '#ddd'),
    (EDW,   'white', 'light gray',  '', 'g90', '#ddd'),
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),

]

palette_slide1 = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),]

palette_slide2 = [
    ('banner', '', '', '', '#ffa', '#60d'),
    ('streak', '', '', '', 'g50', '#60a'),
    ('inside', '', '', '', 'g38', '#808'),
    ('outside', '', '', '', 'g27', '#a06'),
    ('bg', '', '', '', 'g7', '#d06'),]

# temporary attributes while fading
PS_f = urwid.AttrSpec('h232', '#ddd')
PY_f = urwid.AttrSpec('h232', 'h233')
PB_f = urwid.AttrSpec('h232', 'h234')
PW_f = urwid.AttrSpec('h232', 'h242')
PC_f = urwid.AttrSpec('h235', 'h233')
PCI_f = urwid.AttrSpec('h232', 'h233')
PCO_f = urwid.AttrSpec('h232', '#ddd')
PCW_f = urwid.AttrSpec('h232', 'h242')
UR_f = urwid.AttrSpec('h243', 'h244')
URI_f = urwid.AttrSpec('h232', 'h244')
URO_f = urwid.AttrSpec('h232', '#ddd')
URW_f = urwid.AttrSpec('h232', 'h242')
FB_f = urwid.AttrSpec('h237', 'h236')
FL_f = urwid.AttrSpec('h237,bold', 'h238')
FR_f = urwid.AttrSpec('h239', 'h240')
FRH_f = urwid.AttrSpec('h241,bold', 'h240')
FD_f = urwid.AttrSpec('h237', 'h240')

FADE_MAP0= {
    236: ('#aaa', '#ddd'),
    237: ('#aaa', '#000'),
    238: ('#000', '#fd6'),
    239: ('#aaa', '#fff'),
    240: ('#000', '#68a'),
    241: ('#aaa', '#8ef'),
}
FADE_MAP1 = {
    232: ('#ddd', '#fff'),
    233: ('#ddd', '#fd6'),
    234: ('#ddd', '#68a'),
    235: ('#ddd', '#000'),
    242: ('#ddd', '#666'),
    243: ('#ddd', '#68f'),
    244: ('#ddd', '#008'),
}
FADE_MAP2= {
    236: ('#ddd', '#aaa'),
    237: ('#000', '#000'),
    238: ('#fd6', '#000'),
    239: ('#fff', '#aaa'),
    240: ('#68a', '#000'),
    241: ('#8ef', '#aaa'),
}

def fade_palette(map, steps):
    """
    Return a list of palette lists to be passed to
    raw_display.Screen.modify_terminal_palette one at a time.

    map -- {index: (starting colour, ending colour), ...}
        where starting and ending colours are looked up with
        AttrSpec.get_rgb_values()
    steps -- number of steps to generate from starting to ending
        colours

    >>> fade_palette({1:('#000', '#ff0')}, 3)
    [[(1, 0, 0, 0)], [(1, 128, 128, 0)], [(1, 255, 255, 0)]]
    >>> fade_palette({1:('#ff0', '#000')}, 3)
    [[(1, 255, 255, 0)], [(1, 128, 128, 0)], [(1, 0, 0, 0)]]
    """
    assert steps >= 2

    def attr2rgb(a):
        return urwid.AttrSpec(a,"").get_rgb_values()[:3]
    start = dict([(index, attr2rgb(a)) for index, (a,b) in map.items()])
    end = dict([(index, attr2rgb(b)) for index, (a,b) in map.items()])

    out = []
    for i in range(steps):
        run = []
        for index in start.keys():
            r, g, b = start[index]
            er, eg, eb = end[index]
            r = r + urwid.int_scale(i, steps, er-r+1)
            g = g + urwid.int_scale(i, steps, eg-g+1)
            b = b + urwid.int_scale(i, steps, eb-b+1)
            run.append((index, r,g,b))
        out.append(run)
    return out

FADE_PALETTE0 = fade_palette(FADE_MAP0, 16)
FADE_PALETTE1 = fade_palette(FADE_MAP1, 16)
FADE_PALETTE2 = fade_palette(FADE_MAP2, 32)


SLIDE_NAME = urwid.Text("", align=urwid.CENTER)

def make_slide_footer(FL=FL, FB=FB, FD=FD, FR=FR, FRH=FRH):
    return urwid.Pile([
        urwid.AttrWrap(urwid.Divider(u"▁"), FB),
        urwid.Columns([
            ('weight',2,urwid.AttrWrap(SLIDE_NAME, FL)),
            ('fixed',1,urwid.Text((FD, u"▏"))),
            ('weight',5,urwid.AttrWrap(urwid.Text([
                u"Suite Postdigital ∙ ", (FRH, u"ultranoise.es/post"),
                u" ∙ Enrique Tomás ∙ Pontevedra 2018"],
                align=urwid.CENTER, wrap=urwid.CLIP),FR)),
        ])
    ])

SLIDE_FOOTER = make_slide_footer()
SLIDE_FOOTER_f = make_slide_footer(FL_f, FB_f, FD_f, FR_f, FRH_f)


python_logo_plain_sm = [
u"    ▁▁▁▁    \n",
u"   ▕ ∙ ▕▁▁  \n",
u" ▕▔▔▔▔▁▁▏ ▏ \n",
u" ▕ ▕▔▔▁▁▁▁▏ \n",
u"  ▔▔▏ ∙ ▏   \n",
u"    ▔▔▔▔    ",
]
def make_python_logo_sm(PS=PS, PB=PB, PY=PY):
    return urwid.Text([
             (PS,u"    ▁▁▁▁    \n"),
    (PS,u"   ▕"),(PB,u" ∙ ▕"),(PS,u"▁▁  \n"),
    (PS,u" ▕"),(PB,u"▔▔▔▔▁▁"),(PY,u"▏ "),(PS,u"▏ \n"),
    (PS,u" ▕"),(PB,u" ▕"),(PY,u"▔▔▁▁▁▁"),(PS,u"▏ \n"),
    (PS,u"  ▔▔"),         (PY,u"▏ ∙ "),(PS,u"▏   \n"),
                      (PS,u"    ▔▔▔▔    "),
    ])

python_logo_plain = [
u"     ▁▁▁▁▁▁     \n",
u"    ▕ .   ▕     \n",
u"    ▕     ▕▁▁▁  \n",
u" ▕▔▔▔▔▔▔   ▏  ▏ \n",
u" ▕   ▁▁▁▁▁▁▏  ▏ \n",
u" ▕  ▕         ▏ \n",
u" ▕  ▕   ▁▁▁▁▁▁▏ \n",
u"  ▔▔▔▏   . ▏    \n",
u"     ▏     ▏    \n",
u"     ▔▔▔▔▔▔     ",
]

def make_python_logo(PS=PS, PB=PB, PY=PY, PW=PW):
    return urwid.Text((PS,[u"\n",
            u"     ▁▁▁▁▁▁     \n",
    u"    ▕",(PB,u" .   ▕"),"     \n",
    u"    ▕",(PB,u"     ▕"),(PW,u"▁▁"),u"▁  \n",
    u" ▕",(PB,u"▔▔▔▔▔▔   "),(PY,u"▏  "),u"▏ \n",
    u" ▕",(PB,u"   ▁▁▁▁▁▁"),(PY,u"▏  "),(PW,u"▏ \n"),
    u" ▕",(PB,u"  ▕"),(PY,u"         "),(PW,u"▏ \n"),
    u" ▕",(PB,u"  ▕"),(PY,u"   ▁▁▁▁▁▁"),(PW,u"▏ \n"),
    u"  ▔▔",(PW,u"▔"),(PY,u"▏   . "),(PW,u"▏    \n"),
    u"     ",(PY,u"▏     "),(PW,u"▏ "),u"   \n",
            u"     ▔▔",(PW,u"▔▔▔▔  "),u"   \n",
    ]), align=urwid.CENTER)
PYTHON_LOGO = make_python_logo()
PYTHON_LOGO_f = make_python_logo(PS_f, PB_f, PY_f, PW_f)

pycon_logo_plain = [
u"▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n",
u"▏             ▕\n",
u"▏ ▆▇▁         ▕\n",
u"▏  ▔ █▇▁      ▕\n",
u"▏     ▔▁█▇    ▕\n",
u"▏    ▇█▁▔     ▕\n",
u"▏     ▔▁█▇    ▕\n",
u"▏    ▇█▁▔     ▕\n",
u"▏     ▔ ▀█▇▄  ▕\n",
u"▏         ▔ ⌜ ▕\n",
u"▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔",]

def make_pycon_logo(PCO=PCO, PC=PC, PCI=PCI, PCW=PCW):
    return urwid.Text((PC,[
    (PCO,u"▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁  \n"),
    (PCI,u"▏             ▕"),(PCO,u"  \n"),
    (PCI,u"▏"),u" ▆▇▁         ",(PCI,u"▕"),(PCW,u"  \n"),
    (PCI,u"▏"),u"  ▔ █▇▁      ",(PCI,u"▕"),(PCW,u"  \n"),
    (PCI,u"▏"),u"     ▔▁█▇    ",(PCI,u"▕"),(PCW,u"  \n"),
    (PCI,u"▏"),u"    ▇█▁▔     ",(PCI,u"▕"),(PCW,u"  \n"),
    (PCI,u"▏"),u"     ▔▁█▇    ",(PCI,u"▕"),(PCW,u"  \n"),
    (PCI,u"▏"),u"    ▇█▁▔     ",(PCI,u"▕"),(PCW,u"  \n"),
    (PCI,u"▏"),u"     ▔ ▀█▇▄  ",(PCI,u"▕"),(PCW,u"  \n"),
    (PCI,u"▏"),u"         ▔ ⌜ ",(PCI,u"▕"),(PCW,u"  \n"),
    (PCO,u"▔▔"),(PCW,u"▔▔▔▔▔▔▔▔▔▔▔▔▔  "),
    ]), align=urwid.CENTER)

PYCON_LOGO = make_pycon_logo()
PYCON_LOGO_f = make_pycon_logo(PCO_f, PC_f, PCI_f, PCW_f)


urwid_logo_plain = [
u"▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n",
u"▏                         ▕\n",
u"▏                 ▄    █  ▕\n",
u"▏  █  █ █▀▀ █ ▄ █ ▄ ▄▀▀█  ▕\n",
u"▏  █  █ █   ▐▌█▐▌ █ █  █  ▕\n",
u"▏   ▀▀  ▀    ▀ ▀  ▀  ▀▀▀  ▕\n",
u"▏                         ▕\n",
u"▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n"
]
def make_urwid_logo(URO=URO, URI=URI, UR=UR, URW=URW):
    return urwid.Text((UR,[u"\n\n",
    (URO,u"▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁  \n"),
    (URI,u"▏"),u"                         ",(URI,u"▕"),(URO,u"  \n"),
    (URI,u"▏"),u"                 ▄    █  ",(URI,u"▕"),(URW,u"  \n"),
    (URI,u"▏"),u"  █  █ █▀▀ █ ▄ █ ▄ ▄▀▀█  ",(URI,u"▕"),(URW,u"  \n"),
    (URI,u"▏"),u"  █  █ █   ▐▌█▐▌ █ █  █  ",(URI,u"▕"),(URW,u"  \n"),
    (URI,u"▏"),u"   ▀▀  ▀    ▀ ▀  ▀  ▀▀▀  ",(URI,u"▕"),(URW,u"  \n"),
    (URI,u"▏"),u"                         ",(URI,u"▕"),(URW,u"  \n"),
    (URO,u"▔▔"),(URW,u"▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  \n")
    ]), align=urwid.CENTER)
URWID_LOGO = make_urwid_logo()
URWID_LOGO_f = make_urwid_logo(URO_f, URI_f, UR_f, URW_f)




def make_logo_slide(python_logo, pycon_logo, urwid_logo):
    return urwid.Filler(urwid.Columns([
        ('weight', 10, urwid_logo),
        ('weight', 5, pycon_logo),
        ('weight', 6, python_logo),
        ]), 'middle')


class Slide(object):
    def __init__(self, name, widget, footer=None):
        self.name = name
        self.widget = widget
        self.footer = footer
        self.auto_forward = False

    def setup(self, main_loop):
        return

    def transition(self, main_loop):
        return



class FadingSlide(Slide):
    def __init__(self, name, widget, footer=None, fade_palette=None,
        auto_forward=False):
        Slide.__init__(self, name, widget, footer)
        self.fade_palette = fade_palette
        self.auto_forward = auto_forward

    def setup(self, main_loop):
        main_loop.screen.modify_terminal_palette(self.fade_palette[0])

    def transition(self, main_loop):
        for i in range(1, len(self.fade_palette)):
            main_loop.screen.modify_terminal_palette(self.fade_palette[i])
            time.sleep(0.0625)

class ListBoxSlide(Slide):
    def setup(self, main_loop):
        main_loop.screen.reset_default_terminal_palette()
        self._input = list(u"McFlÿ") + ["down", "right", " ", "left", " "] + \
            ["down"]*12 + ["up"]*8 + ["page up", "home"] + ["delete"]*5
        self._input = [u"simulated "+x for x in self._input]
        self._i = 0

        self.widget.set_focus(1)
        self.widget.set_focus_valign(urwid.MIDDLE)
        # FIXME ugly:
        self.widget.get_focus()[0].base_widget.edit.set_edit_text("")

        main_loop.set_alarm_in(0.25, self.animate)

    def animate(self, main_loop, user_data):
        if main_loop.widget.get_current_slide() != self:
            # don't animate if we are not still on display
            return

        main_loop.process_input([self._input[self._i]])
        self._i = (self._i + 1) % len(self._input)

        main_loop.set_alarm_in(0.25, self.animate)



class ColorSlide(Slide):
    def setup(self, main_loop):
        main_loop.screen.reset_default_terminal_palette()
        main_loop.set_alarm_in(0.125, self.animate)

    def animate(self, main_loop, user_data):
        if main_loop.widget.get_current_slide() != self:
            # don't animate if we are not still on display
            return

        for w in self.widget.widget_list:
            col, pos = w.body.get_focus()
            w.body.set_focus(pos+1)
        main_loop.set_alarm_in(0.125, self.animate)

#####################################################################################################################
#####################################################################################################################
class SlideManager(urwid.WidgetWrap):
    def __init__(self, main_loop, slides):
        self.slides = slides
        self.current = 0 # len(slides)-1
        self.main_loop = main_loop
        self.__super.__init__(
            urwid.Frame(urwid.SolidFill("*"), footer=SLIDE_FOOTER))
        self.slides[self.current].setup(main_loop)
        self.update_content()

    def update_content(self):
        slide = self.slides[self.current]
        self._w.body = urwid.AttrWrap(slide.widget, FB)
        if slide.footer:
            self._w.footer = None #slide.footer
        else:
            self._w.footer = None #SLIDE_FOOTER
        SLIDE_NAME.set_text(slide.name)

    def get_current_slide(self):
        return self.slides[self.current]

    def next_slide(self):
        while True:
            if self.current == len(self.slides)-1:
                return
            self.slides[self.current].transition(self.main_loop)
            self.current += 1
            self.update_content()
            self.slides[self.current].setup(self.main_loop)
            if not self.slides[self.current].auto_forward:
                break
            self.main_loop.draw_screen()

    def prev_slide(self):
        if self.current == 0:
            return
        self.current -= 1
        self.slides[self.current].setup(self.main_loop)
        self.update_content()

    def keypress(self, size, key):
        if key.startswith("simulated "):
            return self._w.keypress(size, key[10:])

        if key in (' ', 'enter', 'right', 'page down'):
            self.next_slide()
        elif key in ('backspace', 'left', 'page up'):
            self.prev_slide()
        elif key == 'f10':
            raise urwid.ExitMainLoop()

LOREM_IPSUM = u"""This is Japanese text as it appears on Japanese websites and Wikipedia
すべての人間は、生まれながらにして自由であり、
かつ、尊厳と権利と について平等である。
人間は、理性と良心とを授けられており、
互いに同胞の精神をもって行動しなければならない。

Help:Multilingual support (East Asian)
From Wikipedia, the free encyclopedia

Throughout Wikipedia, Chinese, Japanese and Korean characters are used in relevant articles. Many computers with English or other Western or Cyrillic operating systems will require some setup to be able to display the characters.

Check for existing support:
If you see boxes, question marks, or meaningless letters mixing into the first part, you do not have support for East Asian characters.

Mac OS X:
All recent versions of OS X support East Asian characters natively.

In very old versions of OS X, such as 10.1 you had to install Languages Kits from Apple in order to read Chinese, Japanese or Korean on the Internet. The Language Kit for CJK contains WorldScript software known as scripts which support the encoding for the character set of a particular language. Each language needs a separate script. In more recent versions of OS X, it is included with all installations of OS X.

Once you have installed the Language Kit, just select the particular language character set that you need to see on the Internet page either from View > Encoding (for Microsoft IE) or View > Character set (for Netscape).
"""


LOREM_IPSUM_C = [
    [(SLR,word), u" "] if u"u" in word else
    [(SLB,word), u" "] if u"r" in word else word+u" "
    for word in LOREM_IPSUM.split(u" ")]


COLOR_WIDGETS = [urwid.Columns([
    urwid.Text(urwid.AttrSpec("h%d"%n,"").foreground, align=urwid.CENTER),
    urwid.AttrWrap(urwid.Divider(), urwid.AttrSpec("", "h%d"%n))])
    for n in range(256)]

class ColorLoop(urwid.ListWalker):
    def __init__(self, focus):
        self._focus = focus

    def get_focus(self):
        return COLOR_WIDGETS[self._focus], self._focus

    def set_focus(self, focus):
        self._focus = focus % 256
        self._modified()

    def get_next(self, start_from):
        pos = (start_from + 1) % 256
        return COLOR_WIDGETS[pos], pos

    def get_prev(self, start_from):
        pos = (start_from - 1) % 256
        return COLOR_WIDGETS[pos], pos


RADIO_BUTTON_GROUP = []

class GraphicEdit(urwid.WidgetWrap):
    def __init__(self, caption="", *argl, **argd):
        w = urwid.Edit((EDC,caption), *argl, **argd)
        self.edit = w
        w = urwid.AttrWrap(w, ED, EDF)
        w = urwid.Pile([w, urwid.Padding(urwid.AttrWrap(
                urwid.Divider(u"▔"),EDW),
                left=urwid.calc_width(caption, 0, len(caption)))])
        w = urwid.Columns([w, (urwid.FIXED, 1, urwid.Text((EDW,u"▏")))])
        self.__super.__init__(w)


class GraphicCheckBox(urwid.CheckBox):
    states = {
        True: urwid.SelectableIcon(u"☑",0),
        False: urwid.SelectableIcon(u"☐",0),
        'mixed': urwid.SelectableIcon(u"▣",0) }
    reserve_columns = 2

class GraphicRadioButton(urwid.RadioButton):
    states = {
        True: urwid.SelectableIcon(u"◉",0),
        False: urwid.SelectableIcon(u"○",0),
        'mixed': urwid.SelectableIcon(u"◍",0) }
    reserve_columns = 2

class GraphicButton(urwid.WidgetWrap):
    def __init__(self, label, on_press=None, user_data=None):
        w = urwid.Button(label, on_press, user_data)
        self._button = w
        w = urwid.AttrWrap(w, BT, BTF)
        w = urwid.Columns([w, (urwid.FIXED, 1, urwid.Text((BTW,u"▄")))])
        w = urwid.Pile([w, urwid.Padding(urwid.AttrWrap(
            urwid.Divider(u"▀"), BTW), left=1)])
        self.__super.__init__(w)

EDIT_EG = [
    urwid.Divider(),
    urwid.Padding(GraphicEdit(u"Way to go: ", u""),urwid.LEFT,30, left=4) ]
CHECKBOX_EG = [urwid.Padding(urwid.GridFlow(
    [urwid.AttrWrap(GraphicCheckBox("Ketchup", True), None, CF),
        urwid.AttrWrap(GraphicCheckBox("Mustard", True), None, CF),
        urwid.AttrWrap(GraphicCheckBox("Relish", False), None, CF)],
    13, 3, 1, 'left') ,
    ('fixed left',4), ('fixed right',3))]
RADIOBUTTON_EG = [
    urwid.Divider(),
    urwid.Padding(urwid.GridFlow(
        [urwid.AttrWrap(GraphicRadioButton(RADIO_BUTTON_GROUP, txt), None, CF)
            for txt in ["Morning", "Afternoon", "Evening", "Weekend"]],
        13, 3, 1, 'left') ,
        ('fixed left',4), ('fixed right',3))]
BUTTON_EG = [
    urwid.Divider(),
    urwid.Padding(urwid.GridFlow(
        [GraphicButton(txt) for txt in ["Graceful", "Restart", "Stop"]],
        13, 3, 1, 'left'),
        ('fixed left',4), ('fixed right',3))]

################################################################################################################
################################################################################################################
SLIDES = [
    Slide("Titulo",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital "), align='center'), 'streak')), 'bg')),
    Slide("Titulo2",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n"), align='center'), 'streak')), 'bg')),
    Slide("Titulo3",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n "), align='center'), 'streak')), 'bg')),
    Slide("Titulo4",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n o cómo post-componer música"), align='center'), 'streak')), 'bg')),
    Slide("Titulo5",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n o cómo post-componer música \n después de Spotify"), align='center'), 'streak')), 'bg')),
    Slide("Titulo6",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n o cómo post-componer música \n después de Spotify \n"), align='center'), 'streak')), 'bg')),
    Slide("Titulo7",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n o cómo post-componer música \n después de Spotify \n \n"), align='center'), 'streak')), 'bg')),
    Slide("Titulo8",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n o cómo post-componer música \n después de Spotify \n \n por"), align='center'), 'streak')), 'bg')),
    Slide("Titulo9",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n o cómo post-componer música \n después de Spotify \n \n por \n"), align='center'), 'streak')), 'bg')),
    Slide("Titulo10",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n o cómo post-componer música \n después de Spotify \n \n por \n \n"), align='center'), 'streak')), 'bg')),
    Slide("Titulo11",urwid.AttrMap(urwid.Filler(urwid.AttrMap(urwid.Text(('banner', u" Suite Postdigital \n \n o cómo post-componer música \n después de Spotify \n \n por \n \n Enrique Tomás"), align='center'), 'streak')), 'bg')),
    Slide("pronounciation", urwid.Overlay(urwid.BigText(
        u"Parte 1 Blockchain:\n Los mineros", urwid.HalfBlock5x4Font()), urwid.SolidFill(" "),
        urwid.CENTER, None, urwid.MIDDLE, None)),
    FadingSlide("", urwid.AttrWrap(urwid.SolidFill(" "), FB_f),
        SLIDE_FOOTER_f, FADE_PALETTE0),
    FadingSlide("welcome", make_logo_slide(PYTHON_LOGO_f, PYCON_LOGO_f, URWID_LOGO_f),
        fade_palette=FADE_PALETTE1, auto_forward=True),
    Slide("welcome", make_logo_slide(PYTHON_LOGO, PYCON_LOGO, URWID_LOGO)),
    Slide("pronounciation", urwid.Overlay(urwid.BigText(
        u"Parte 1 Blockchain:\n Los mineros", urwid.HalfBlock5x4Font()), urwid.SolidFill(" "),
        urwid.CENTER, None, urwid.MIDDLE, None)),
    Slide("text", urwid.Filler(urwid.Text(LOREM_IPSUM))),
    Slide("text alignment", urwid.Filler(urwid.Columns([
        urwid.AttrWrap(urwid.Text(LOREM_IPSUM),SLG),
        urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.CENTER),SLG),
        urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.RIGHT),SLG),
        ], 2))),
    Slide("text wrapping", urwid.Pile([
        urwid.Filler(urwid.Columns([
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM),SLG),
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.CENTER),SLG),
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.RIGHT),SLG),
        ], 2)),
        ('flow',urwid.Divider()),
        urwid.Filler(urwid.Columns([
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.LEFT, urwid.ANY),SLG),
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.CENTER, urwid.ANY),SLG),
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.RIGHT, urwid.ANY),SLG),
        ], 2)),
        ('flow',urwid.Divider()),
        urwid.Filler(urwid.Columns([
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.LEFT, urwid.CLIP),SLG),
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.CENTER, urwid.CLIP),SLG),
            urwid.AttrWrap(urwid.Text(LOREM_IPSUM, urwid.RIGHT, urwid.CLIP),SLG),
        ], 2)),
        ])),
    Slide("text color", urwid.Filler(urwid.Text(LOREM_IPSUM_C))),
    ColorSlide("colors", urwid.Columns([
        urwid.ListBox(ColorLoop(0)),
        urwid.ListBox(ColorLoop(64)),
        urwid.ListBox(ColorLoop(128)),
        urwid.ListBox(ColorLoop(192)),
        ])),
    Slide("text editing", urwid.ListBox(urwid.SimpleListWalker(
        EDIT_EG,
        ))),
    Slide("check boxes", urwid.ListBox(urwid.SimpleListWalker(
        EDIT_EG +
        CHECKBOX_EG
        ))),
    Slide("radio buttons", urwid.ListBox(urwid.SimpleListWalker(
        EDIT_EG +
        CHECKBOX_EG +
        RADIOBUTTON_EG
        ))),
    Slide("buttons", urwid.ListBox(urwid.SimpleListWalker(
        EDIT_EG +
        CHECKBOX_EG +
        RADIOBUTTON_EG +
        BUTTON_EG
        ))),
    ListBoxSlide("listbox", urwid.ListBox(urwid.SimpleListWalker(
        EDIT_EG +
        CHECKBOX_EG +
        RADIOBUTTON_EG +
        BUTTON_EG + [
        urwid.Divider(),
        urwid.Text(LOREM_IPSUM),
        ]))),
    FadingSlide("get it", urwid.AttrWrap(urwid.Overlay(urwid.BigText(
        u"excess.org/urwid", urwid.HalfBlock5x4Font()),
        urwid.SolidFill(" "),
        urwid.CENTER, None, urwid.MIDDLE, None), FB_f),
        SLIDE_FOOTER_f, FADE_PALETTE2),
    Slide("get it", urwid.AttrWrap(urwid.Overlay(urwid.BigText(
        u"excess.org/urwid", urwid.HalfBlock5x4Font()),
        urwid.SolidFill(" "),
        urwid.CENTER, None, urwid.MIDDLE, None), FB_f),
        SLIDE_FOOTER_f),
]


def main():
    main_loop = urwid.MainLoop(None, palette)
    main_loop.screen.set_terminal_properties(colors=256)
    main_loop.widget = SlideManager(main_loop, SLIDES)
    main_loop.run()

def run_commandline():
    import sys
    if "--test" in sys.argv:
        import doctest
        doctest.testmod()
    else:
        main()

if __name__=='__main__':
    run_commandline()
