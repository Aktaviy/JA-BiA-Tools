"""
Created on February 6, 2012

@author: sbobovyc
"""
"""   
    Copyright (C) 2012 Stanislav Bobovych

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import struct          
from collections import OrderedDict
from jabia_file import JABIA_file

class CTX_ID:
    def __init__(self, id, id_name, path):
        self.id = id
        self.id_name = id_name
        self.path = path
 
    def get_packed_data(self): 
        import binascii       
        data_buffer = struct.pack("<II%isI%is" % (len(self.id_name), len(self.path)), 
                                  self.id, len(self.id_name), self.id_name, len(self.path), self.path)
#        print binascii.hexlify(data_buffer)
        return data_buffer
    
    def __repr__(self):
        return "%s(name=%r, id=%r, id_name=%r, path=%r)" % (
             self.__class__.__name__, self.id, self.id_name, self.path)
   
    def __str__(self):
        return "CTX ID: %s, %s = %s" % (self.id, self.id_name, self.path)
 
         
class CTX_language:
    def __init__(self, description_string, data_offset=0):
        self.description_string = description_string
        self.data_offset = data_offset
        self.data_dictionary = OrderedDict()   # {text id : data} mapping
    
    def add_data(self, id, text):
        self.data_dictionary[id] = text
    
    def get_description(self):
        return self.description_string
    
    def get_data(self):
        return self.data_dictionary
    
    def get_num_items(self):
        return len(self.data_dictionary)
    
    def get_last_item_id(self):
        last_item = self.data_dictionary.popitem()  # get last item in ordered dictionary        
        # put item back
        self.add_data(last_item[0], last_item[1])
        last_item_id = last_item[0]
        return last_item_id
    
    def get_description_length(self):
        return len(self.description_string)
    
    def get_packed_data(self):        
        data_buffer = ""
        for key, value in self.data_dictionary.items():       
            encoded_value = value.encode('utf-16le')     
            encoded_size = len(encoded_value)         
            data_packed = struct.pack("<II%is" % encoded_size, key, encoded_size/2, encoded_value)
            #print binascii.hexlify(data_packed)
            data_buffer = data_buffer + data_packed
            #print binascii.hexlify(data_buffer)
        return data_buffer
    
    def __repr__(self):
        return "%s(name=%r, language=%r, data=%r)" % (
             self.__class__.__name__, self.description_string, self.data_dictionary)
   
    def __str__(self):
        return "Language: %s, data offset: %s bytes" % (self.description_string, hex(self.data_offset).rstrip('L'))
        
class VTP_data:
    def __init__(self):
        self.num_items = None
        self.last_item_id = 0
        self.num_languages = None
        self.data_offset = 0 
        self.language_list = []
    
    def get_languages(self):
        return self.language_list
    
    def get_num_languages(self):
        return len(self.language_list)
    
    def insert_language(self, language):
        self.language_list.append(language)
    
    def unpack(self, file_pointer, peek=False, verbose=False):   
        while file_pointer.read(1) != '':
            file_pointer.seek(file_pointer.tell()-1)
            self.magick,self.num_items = struct.unpack("<HxH", file_pointer.read(5))
            print hex(self.magick), self.num_items
            
            # read in static 3d files
            for i in range(0, self.num_items):
                id1,id2,length = struct.unpack("<IHI", file_pointer.read(10))
                print "Resource id",id1,id2,length
                varname, = struct.unpack("%ss" % length, file_pointer.read(length))
                num_types, = struct.unpack("<B", file_pointer.read(1))
                print "Varname", varname, num_types
                for i in range(0, num_types):
                    length, =struct.unpack("<I", file_pointer.read(4))
                    object_type, = struct.unpack("%ss" % length, file_pointer.read(length))
                    print "Type", object_type
                    resource_id, number_of_objects = struct.unpack("<BB", file_pointer.read(2))
                    print resource_id, number_of_objects
                    for i in range(0, number_of_objects):
                        length, = struct.unpack("<I", file_pointer.read(4))                
                        file_path, = struct.unpack("%ss" %length, file_pointer.read(length))
                        print file_path
                # read in trailer
                file_pointer.read(2)                    
            # read in animations
            print hex(file_pointer.tell())
            file_pointer.read(1)
            self.num_animations, = struct.unpack("<H", file_pointer.read(2))
            print "Number of animations", hex(self.num_animations)
            for i in range(0, self.num_animations):
                id1,id2,length = struct.unpack("<HII", file_pointer.read(10))
                print "Animation resource id",id1,id2,length
                print i, self.num_animations
                varname, = struct.unpack("%ss" % length, file_pointer.read(length))
                num_animations, = struct.unpack("<B", file_pointer.read(1))
                print "Varname", varname, num_animations
                for i in range(0, num_animations):
                    length, = struct.unpack("<I", file_pointer.read(4))
                    print "length", length 
                    animation_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                    print animation_name
                    unknown, num_files = struct.unpack("<BB", file_pointer.read(2))
                    print unknown, num_files
                    for i in range(0, num_files):
                        length, = struct.unpack("<I", file_pointer.read(4))
                        path_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                        print "Path name", path_name
                        # read in animations
                # read in trailer
                file_pointer.read(1)
            
            
            print hex(file_pointer.tell())
            file_pointer.read(1)
            self.num_effects, = struct.unpack("<H", file_pointer.read(2))
            print "Number of effects", hex(self.num_effects)
            for i in range(0, self.num_effects):
                id1,id2,length = struct.unpack("<HII", file_pointer.read(10))
                print "Effect resource id",id1,id2,length
                print i, self.num_effects
                varname, = struct.unpack("%ss" % length, file_pointer.read(length))
                num_effects, = struct.unpack("<B", file_pointer.read(1))
                print "Varname", varname, num_effects    
                for i in range(0, num_effects):
                    length, = struct.unpack("<I", file_pointer.read(4))
                    print "length", length 
                    effect_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                    print effect_name
                    unknown, num_files = struct.unpack("<BB", file_pointer.read(2))
                    print unknown, num_files  
                    for i in range(0, num_files):
                        length, = struct.unpack("<I", file_pointer.read(4))
                        path_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                        print "Path name", path_name          
                # read in trailer
                file_pointer.read(1)
            
            print hex(file_pointer.tell())            
            self.num_objects, = struct.unpack("<H", file_pointer.read(2))
            print "Number of objects", hex(self.num_objects)
            for i in range(0, 1):
                id1,id2,length = struct.unpack("<HxII", file_pointer.read(11))
                print "Object resource id",id1,id2,length
                print i, self.num_effects
                varname, = struct.unpack("%ss" % length, file_pointer.read(length))
                print "Varname", varname    
                file_pointer.read(5)
                length, = struct.unpack("<I", file_pointer.read(4))
                material_name, = struct.unpack("%ss" % length, file_pointer.read(length))
                print "Material", material_name
                a,b,c,d,e,f = struct.unpack("<ffffff", file_pointer.read(24))
                print a,b,c,d,e,f
                return
        if peek or verbose:
            pass
        if peek:
            return  
                    
    def get_packed_data(self):
        #1. check to see if all the language have the same amount of items
        #2. check that all languages have the same last item id
        self.num_languages = self.get_num_languages()
        self.num_items = self.language_list[0].get_num_items()
        self.last_item_id = self.language_list[0].get_last_item_id()        
        
        for i in range(1, len(self.language_list)):
            if self.language_list[i].get_num_items() != self.num_items:
                raise  Exception("Languages do not contain same amount of items!")
            if self.language_list[i].get_last_item_id()  != self.last_item_id:
                raise  Exception("The last item in each language does not contain the same id!")
            
        #3. pack each language into a byte string and create the data 
        header_buffer = struct.pack("<III", self.num_items, self.last_item_id, self.num_languages)
        data_buffer = ""
        previous_buffer_length = 0
        for language in self.language_list:
            length = language.get_description_length()
            description = language.get_description()
            header_buffer = header_buffer + struct.pack("<I%isI" % length, length, description, previous_buffer_length)
            #print binascii.hexlify(header_buffer)
            data_buffer = data_buffer + language.get_packed_data()
            previous_buffer_length = len(data_buffer)
            
        #4. concatenate the byte strings and return     
        return (header_buffer + data_buffer)            

    def __repr__(self):
        return "%s(name=%r, languages=%r)" % (
             self.__class__.__name__, self.language_list)
            
class VTP_file(JABIA_file):    
    def __init__(self, filepath=None):
        super(VTP_file,self).__init__(filepath=filepath)
        self.yaml_extension = ".vtp.txt"
        
    def open(self, filepath=None, peek=False):
        super(VTP_file,self).open(filepath=filepath, peek=peek)  
        self.data = VTP_data()

if __name__ == "__main__":
    pass
    vtp = VTP_file("C:\\Program Files (x86)\\Jagged Alliance Back in Action Demo\\bin_win32\main.vtp")
    #cF = CTX_file("/media/Acer/Users/sbobovyc/Desktop/test/bin_win32/interface/equipment.ctx")
    vtp.open()        
    vtp.unpack(verbose=False)    
    #vtp.dump2yaml(".")
#    cF.pack(verbose=False)
    # pack
#    cFnew = CTX_file("new_equipment.ctx")
#    cFnew.yaml2bin("equipment.ctx.txt")

    # create a file programmatically
#    cTest = CTX_file("test.ctx")
#    english = CTX_language("eng")
#    english.add_data(0, u"Officer's key")
#    cTest.data.insert_language(english)
#    cTest.dump2yaml(".")
