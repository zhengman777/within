import pygmi
from fighter import Fighter

class Enemy(Fighter):

    def __init__(self,x,y):
        super().__init__(x,y)

    def event_create(self):
        super().event_create()

    def update(self):
        super().update()