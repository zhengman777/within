'''
Created on May 12, 2013

@author: Catt
'''
import pygmi
from menu import *
from street import *
from mainmenu import *

if __name__ == '__main__':
    x_dim = 800
    y_dim = 600
    game = pygmi.Pygmi((x_dim,y_dim), "Test Game", 0)
    game.addRoom(MainMenu())
    game.addRoom(Street())
    game.gotoRoom("mainmenu")


    while(True):
        #update
        game.update()
        #render
        game.render()
        #paint
        game.paint()
