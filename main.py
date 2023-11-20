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
    
def find_duplicates(client_list):
    length = len(client_list)
    myset = set(client_list)
    if length != myset:
        return True
    return False

class HomeScreen(Screen):
   pass

class MyPopup(Popup):

    item = ObjectProperty()
    customer = ObjectProperty()

    def match_photo(self, customer, image):
        
        write_to_csv(customer, image)

    def send_info_to_popup(self, name, image):
        self.ids.label_confirm.text = f"Deseas confirmar a {name.text}?"

        
        

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

class Clientes:

    client_count = 0

    def __init__(self, client, items):
        self.client = client
        self.items = items
        Clientes.client_count += 1
    
    def get_number_of_items(self):
        return len(self.items)
    
    def add_item(self):
        pass
    
    def delete_client(self):
        Clientes.client_count -= 1
        

    def delete_item(self):
        pass
    
    def get_number_of_items(self):
        pass


        

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
    
    def instantiate_client_objects(self):
        with open('appmercadito/kv/data.csv', newline='') as f:
            reader = csv.reader(f)
            database = []
            x = []
            for row in reader:
                database.append(row)
                x.append(Clientes(row[0], row[1]))
            print(find_duplicates(database))
            quit()
            for y in range(0,len(x)):
                print(x[y].client)

        clients = []
        for client in database:
            clients.append(client[0])
        print(clients)
    

MainApp().run()