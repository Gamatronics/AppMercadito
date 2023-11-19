from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import os

class HomeScreen(Screen):
    pass


class Asignar(Screen):
    index = 0
    def move_forward(self, is_forward):
        
        file_list = os.listdir('appmercadito/kv/images')
        list_length = len(file_list)
        if is_forward and self.index < list_length - 1:
            self.index += 1
        elif (not is_forward and self.index > 0):
            self.index -= 1
        self.ids.pic_assign.source = f'kv/images/{file_list[self.index]}'
        
        
        

class VerClientes(Screen):
    pass

class VerFotos(Screen):
    pass


class ImageButton(ButtonBehavior, Image):
    pass

GUI = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return GUI
    
    def change_screen(self, screen_name):
        # Get screen manager from kv file
        screen_manager = self.root.ids['screen_manager']
        #screen_manager.transition
        screen_manager.current = screen_name
        #screen_manager = self.root.ids
    

MainApp().run()