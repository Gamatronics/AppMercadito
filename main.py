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
    
def duplicated(client_list):
    newlist = [] # empty list to hold unique elements from the list
    duplist = [] # empty list to hold the duplicate elements from the list
    index_duplicated = []
    for i in client_list:
        if i not in newlist:
            newlist.append(i)
        else:
            duplist.append(i,) # this method catches the first duplicate entries, and appends them to the list
            index_duplicated.append(client_list.index(i))
    return set(duplist)

def count_repetitions(reps, client_list):
    # Creates and returns a dictionary with Key (cliente) and value (index of duplicate purchases)
    # e.g. {'Gaston':[3,6,8,9], 'Alma':[6,7]}
    count = {}
    for x in reps:
        count[x] = client_list.count(x)
    return count

def remove_replace(count, client_list):
    # Make copy of list to avoid modifying original list
    passed_list = client_list.copy()
    indices = {}
    keys_list = list(count.keys())
    for key in keys_list:
        index_list = []
        for i in range(count[key]):
            index = passed_list.index(key)
            index_list.append(index)
            passed_list.pop(index)
            passed_list.insert(index,'')
        indices[key] = index_list
    # Returns the indices of repeated items for clients, and a curated list
    # with empty strings in the place of repeated clients
    return indices, passed_list

def find_duplicates(client_list):
    length = len(client_list)
    myset = set(client_list)
    if length != myset:
        return True
    return False

def objects_from_csv(repeated_list, database):
    # Make copy or passed list as to not modify them
    repetition_frequency = repeated_list.copy()
    original_list = database.copy()
    # Get the keys on a list of customers with multiple items
    repeated_clientes = list(repetition_frequency.keys())
    client_objects = []
    original_counter = []
    # Make a list that contains all the elements, so it can later by
    # modified by removing repeats
    for x in range(len(original_list)):
        original_counter.append(x)
    # Two for loops to go thtough the repeated clients and their items
    # and instantiation of the corresponding Clientes object
    for rep in repeated_clientes:
        index_list = []
        for item in repetition_frequency[rep]:

            index_list.append(original_list[item][1])
            original_counter.remove(item)
        client_objects.append(Clientes(rep,index_list))
    # Generate the single buyer Clientes objects
    for x in original_counter:
        client_objects.append(Clientes(original_list[x][0],[original_list[x][1]]))
    



class HomeScreen(Screen):

    def send_data(self):
        data = Clientes.client_names
        names = ''
        for x in data:
            names = f"{names} {x}\n"
        self.manager.get_screen('ver_clientes_screen').ids.list_of_clients.text = names

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
    client_names = []

    def __init__(self, client, items):
        self.client = client
        self.items = items
        Clientes.client_count += 1
        Clientes.client_names.append(client)
    
    def get_number_of_items(self):
        return len(self.items)
    
    def add_item(self):
        pass
    
    def delete_client(self, name):
        Clientes.client_count -= 1
        Clientes.client_names.remove(name)
        

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
        # Open database (CSV file)
        with open('appmercadito/kv/data.csv', newline='') as f:
            reader = csv.reader(f)
            database = []
            clientes = []
            for row in reader:
                # Put the whole contents into database list
                database.append(row)
                # Put the client's name on a different list
                clientes.append(row[0])
        if find_duplicates(clientes): # Function that returns true if there are repeats
            duplicates = duplicated(clientes)
            repeated_list, original_list = remove_replace(count_repetitions(duplicates, clientes), clientes)
        objects_from_csv(repeated_list, database)
        print(Clientes.client_count)
        print(Clientes.client_names)
        
            
         
    

MainApp().run()