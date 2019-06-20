import pygame
import rockpaper

class Scene(object):
    def __init__(self, name='', **kwargs):
        self._name = name
        self._changing = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def changing(self):
        return self._changing

    @changing.setter
    def changing(self, value):
        if not isinstance(value, bool):
            return
        self._changing = value
    
    def load(self):
        pass

    def draw(self):
        pass

    def run(self, events):
        pass

    def on_change(self):
        pass

    def repost_events(self, events):
        if events.type != pygame.NOEVENT:
            pygame.event.post(events)

    #newscene is the name of scene
    def change(self, newscene):
        self.on_change()
        pygame.event.post(pygame.event.Event(rockpaper.SCENE_CHANGE,{
            'oldscene': self.name,
            'newscene': str(newscene)
        }))
