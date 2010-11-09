#!/usr/bin/env python

from __future__ import division

from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.showbase import DirectObject
from direct.gui.DirectGui import (DirectFrame, DirectLabel, DirectButton)
from panda3d.core import TextFont, AntialiasAttrib


class MainMenu(DirectFrame):
    def __init__(self, game, *args, **kwargs):
        kwds = dict(
                pos=(0, 0, 0),
                scale=0.1,
                frameColor=(0, 0, 0, 1.0),
            )
        kwds.update(kwargs)
        DirectFrame.__init__(self, *args, **kwds)

        font = loader.loadFont('TRON.ttf')
        #font.setPixelsPerUnit(180)
        font.setRenderMode(TextFont.RMWireframe)


        # Parameters common to all of the menu elements
        common = dict(
                text_fg=(1.0, 1.0, 1.0, 1.0),
                frameColor=(0, 0, 0, 0),
                relief=None,
            )

        title = DirectLabel(
                text="Polyhedral Tron",
                text_font=font,
                scale=1.5, # Bigger than the other text
                **common
            )
        title.reparentTo(self)
        title.setAntialias(AntialiasAttrib.MLine)

        self.startButton = DirectButton(
                text=("Start Game", "<Start Game>", "<Start Game>", "Start Game"),
                text_font=font,
                command=game.startGame,
                **common
            )
        self.startButton.reparentTo(self)
        self.startButton.setAntialias(AntialiasAttrib.MLine)

        self.quitButton = DirectButton(
                text=("Quit", "<Quit>", "<Quit>", "Quit"),
                text_font=font,
                command=game.quit,
                **common
            )
        self.quitButton.reparentTo(self)
        self.quitButton.setAntialias(AntialiasAttrib.MLine)

        byline = DirectLabel(
                text="David Bliss, Devin Banks, and Tom Most",
                scale=0.7,
                **common
            )
        byline.reparentTo(self)

        class_ = DirectLabel(
                text="CSSE351 Computer Graphics, November 2010",
                scale=0.7,
                **common
            )
        class_.reparentTo(self)

        positionMenuItems(
                (title, 2),
                (None, 1),
                (self.startButton, 1.4),
                (self.quitButton, 1.4),
                (None, 1),
                (byline, .8),
                (class_, .8),
            )

def positionMenuItems(*items):
    padding = 0.2
    totalHeight = sum(h for (_, h) in items) + (padding * (len(items) - 1))
    zPos = totalHeight / 2
    for (item, height) in items:
        if item is not None:
            item.setPos(0, 0, zPos)
        zPos -= height
        zPos -= padding

class MenuDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # This doesn't work on Tom's computer.  Perhaps someone
        # else should try it.
        #filters = CommonFilters(base.win, base.cam)
        #if not filters.setBloom(desat=0, ):
        #    print "Failed to enable bloom filter"

        self.mainMenu = MainMenu(self)
        # Automatically reparented to aspect2d

        self.accept('escape', exit)
        self.accept('q', exit)

    def startGame(self):
        print "Start game"
        self.mainMenu.hide()

    def quit(self):
        exit()

if __name__ == '__main__':
    MenuDemo().run()
