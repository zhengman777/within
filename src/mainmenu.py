import pygmi
from menu import PlayButton, QuitButton

class MainMenu(pygmi.Room):

    def __init__(self):
        self.x_dim = 800
        self.y_dim = 600
        super().__init__("mainmenu",self.x_dim,self.y_dim)

    def event_create(self):
        oPlay = PlayButton(800-64,600-60)
        oQuit = QuitButton(self.x_dim-64,self.y_dim-30)
        self.setBackground(self.assets.images["bg"]["title.png"])
        self.game.createInstance(oPlay)
        self.game.createInstance(oQuit)