import Map
import GUI
import Utilities
import Player
import main
import TowerDragging

from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics import *

class playField(ScatterLayout):
    def __init__(self,**kwargs):
        super(playField,self).__init__(**kwargs)

        ##scatter properties to allow partial scaling and no rotation
        self.scale = 1
        self.scale_max = 1.5
        self.scale_min = 1
        self.do_rotation=False
        self.do_translation = False
        self.size = main.Window.size
        self.size_hint = (1,1)
        self.pos = (0,0)
        self.do_collide_after_children = True
        self.popUpOpen = None
        self.placeholder = self.dragger = None

    def bindings(self, *args):
        self.size = main.Window.size
        print "size", self.size
        for child in self.children:
            child.size = self.size

    def on_touch_down(self, touch):
        self.squarepos = Utilities.getPos(touch.pos)
        self.squarepos = self.adjustInBounds(self.squarepos)
        print "squarepos", self.squarepos, Map.mapvar.squsize, Map.mapvar.scrhei

        #move the selected square if a neighboring tower overlaps
        self.adjustForNeighbor()

        if self.dragger and self.dragger.collide_point(*touch.pos):
            self.dragger.on_touch_down(touch)
            return

        #don't allow touches outside of play boundary if a menu isn't open
        if self.popUpOpen:
            if not self.popUpOpen.collide_point(*touch.pos):
                self.removeAll()
                return
            else:
                return super(playField, self).on_touch_down(touch)

        if not self.popUpOpen:
            if self.outOfBounds(touch.pos):
                self.removeAll()
                return super(playField, self).on_touch_down(touch)
        #do nothing in playfield if paused or menu
        if Player.player.state == 'Paused' or Player.player.state == 'Menu':
            return
        #tower selection buttons
        self.towerSelected(touch)
        #create the tower creation menu and display
        self.openTowerBuilder()
        #returning this super argument allows the touch to propogate to children.
        return super(playField, self).on_touch_down(touch)

    def towerSelected(self,touch):
        for tower in Map.mapvar.towercontainer.walk(restrict=True):
           if tower.collide_point(*touch.pos):
               if Player.player.tbbox != None:
                   self.removeAll()
               Player.player.towerSelected = tower
               GUI.gui.towerMenu(tower.pos)
               return True
    def openTowerBuilder(self):
        if not self.popUpOpen:
            self.placeholder = TowerDragging.TowerPlaceholder(pos=self.squarepos, initial=True)
            self.dragger = TowerDragging.TowerDragger(pos=self.squarepos)
            GUI.gui.builderMenu(self.squarepos)
            self.towerpos=self.squarepos
            return True

    def adjustInBounds(self, pos):
        if pos[0] + 2*Map.mapvar.squsize > Map.mapvar.scrwid - Map.mapvar.squsize * 2:
            pos[0] = Map.mapvar.scrwid - Map.mapvar.squsize * 4
        elif pos[0] < Map.mapvar.squsize * 2:
            pos[0] = Map.mapvar.squsize * 2
        if pos[1] + 2*Map.mapvar.squsize > Map.mapvar.scrhei - Map.mapvar.squsize * 3:
            pos[1] = Map.mapvar.scrhei - Map.mapvar.squsize * 5
        elif pos[1] < Map.mapvar.squsize * 2:
            pos[1] = Map.mapvar.squsize * 2
        return pos

    def adjustForNeighbor(self):
        for tower in Map.mapvar.towercontainer.walk(restrict=True):
            if tower.collide_point(self.squarepos[0]+Map.mapvar.squsize, self.squarepos[1]):
                self.squarepos[0]-=Map.mapvar.squsize
            if tower.collide_point(self.squarepos[0], self.squarepos[1]+Map.mapvar.squsize):
                self.squarepos[1]-=Map.mapvar.squsize
            if tower.collide_point(self.squarepos[0]+Map.mapvar.squsize, self.squarepos[1]+Map.mapvar.squsize):
                self.squarepos[1]-=Map.mapvar.squsize
                self.squarepos[0]-=Map.mapvar.squsize

    def outOfBounds(self, pos):
        if pos[0] >= Map.mapvar.scrwid - Map.mapvar.squsize * 2 or pos[1] >= Map.mapvar.scrhei - Map.mapvar.squsize * 3 or \
            pos[0] < Map.mapvar.squsize * 2 or pos[1] < Map.mapvar.squsize * 2:
            return True
        else:
            return False

    def removeAll(self):
        if Player.player.tbbox:
            Map.mapvar.backgroundimg.remove_widget(Player.player.tbbox)
            Player.player.tbbox = None
            Player.player.layout = None
        if Map.mapvar.enemypanel.parent:
            Map.mapvar.backgroundimg.remove_widget(Map.mapvar.enemypanel)
        if Map.mapvar.triangle:
            Map.mapvar.backgroundimg.canvas.remove(Map.mapvar.triangle)
            Map.mapvar.triangle = None
        if Map.mapvar.towerRange:
            Map.mapvar.backgroundimg.canvas.remove(Map.mapvar.towerRange)
            Map.mapvar.towerRange = None
        if self.placeholder:
            Map.mapvar.backgroundimg.remove_widget(self.placeholder)
            self.placeholder = None
        if self.dragger:
            Map.mapvar.backgroundimg.remove_widget(self.dragger)
            Map.mapvar.towerdragimagecontainer.clear_widgets()
            self.dragger = None
        self.popUpOpen = None

    def on_pressed(self, instance, pos):
        print('pressed at {pos}'.format(pos=pos))



