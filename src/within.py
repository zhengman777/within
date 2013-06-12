'''
Created on May 12, 2013

@author: Catt
'''
import pygmi, pygame, os, sys, math
from pygame.locals import *
from menu import *
from street import *

if __name__ == '__main__':
    x_dim = 800
    y_dim = 600
    game = pygmi.Pygmi((x_dim,y_dim), "Test Game", 0)
    oPlay = PlayButton(x_dim-64,y_dim-60,game)
    oQuit = QuitButton(x_dim-64,y_dim-30,game)
    mainmenu = pygmi.Room("mainmenu",x_dim,y_dim)
    bgMainMenu = pygmi.Object(pygmi.Sprite("img/bg/title.png",0,0,800,600),0,0)
    mainmenu.addToRoom(bgMainMenu)
    mainmenu.addToRoom(oPlay)
    mainmenu.addToRoom(oQuit)
    game.addRoom(mainmenu)
    game.addRoom(Street(game))
    game.gotoRoom("mainmenu")


    while(True):
        #update
        game.update()
        #render
        game.render()
        #paint
        game.paint()
