from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

import os
import csv

def write_to_csv(client, pic):
    with open('appmercadito/kv/data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([client, pic])
        csvfile.close()
    

class HomeScreen(Screen):
    pass

class MyPopup(Popup):

    item = ObjectProperty()
    customer = ObjectProperty()

    def match_photo(self, customer, image):
        
        write_to_csv(customer, image)

    def send_info_to_popup(self, name, image):
        self.ids.label_confirm.text = f"Deseas confirmar a {name.text}?"
        print(image.source)
        
        

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
        
    def match_photo(self):
        cliente = self.ids.assignee.text
        pic = self.ids.pic_assign.source
        print(cliente,pic)
        #write_to_csv(cliente, pic)
    
    def what_i_need(self):
        print(self.ids.pic_assign.source)


        

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
    
    def match_photo(self):
        cliente = self.ids.assignee.text
        pic = self.ids.pic_assign.source
        write_to_csv(cliente, pic)
    

MainApp().run()