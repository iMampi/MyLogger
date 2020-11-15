import tkinter as tk
from tkinter import ttk
import datetime as dt
import csv, os

#todo : change readonly to the correct one
#todo : "les gens concerné" fix the boolvar
#todo : arrange display. it is centered, we dont want that
#todo : arrange size of ain window

class MyData:
    #todo : value o flist to save in csv. so they  will be load from csv
    def __init__ (self):
        self.filename="database_mylogger.csv"
        self.list_name=["Estelle","Mampi","Mario","Williamson","Santatra"]
        self.list_societe=["Roche Noire","Directimmo","Troc & Cash","MKR Property","Wave"]
        self.fields={"Ref":{"type":'Entry',
                       "creation":{"visible":True,"state":"tk.Normal"},
                       "modification":{"visible":True,"state":"tk.ReadOnly"}
                           },
                "Date":{"type":'Entry',
                       "creation":{"visible":True,"state":"tk.Normal"},
                       "modification":{"visible":True,"state":"tk.ReadOnly"}
                       },
                "Note":{"type":'Text',
                       "creation":{"visible":True,"state":"tk.Normal"},
                       "modification":{"visible":True,"state":"tk.ReadOnly"}
                       },
                "Les gens concernés":{"type":'Checkbox',
                                      "creation":{"visible":True,"state":"tk.Normal"},
                                      "modification":{"visible":True,"state":"tk.Disabled"},
                                      "list_name":self.list_name
                                      },
                "Sociétés/Personnel":{"type":'Checkbox',
                                      "creation":{"visible":True,"state":"tk.Normal"},
                                      "modification":{"visible":True,"state":"tk.Disabled"},
                                      "list_name":self.list_societe
                                     },
                "Alarme":{"type":'Entry',
                       "creation":{"visible":True,"state":"tk.Normal"},
                       "modification":{"visible":True,"state":"tk.Normal"}
                         }
                    }
        
    def save_entry(self,data):
        newfile= not os.path.exists(self.filename)
        if newfile:
            with open(self.filename, 'w', newline='') as fh:
                csvwriter = csv.DictWriter(fh,
                                           fieldnames=[x for x in self.fields.keys()],
                                           delimiter=";"
                                           )
                csvwriter.writeheader()
        with open(self.filename, 'a',newline='') as fh:
                csvwriter = csv.DictWriter(fh,
                                           fieldnames=[x for x in self.fields.keys()],
                                           delimiter=";"
                                           )
                csvwriter.writerow(data)

    def load_records(self):
        existfile = os.path.exists(self.filename)
        if existfile:
            with open(self.filename, 'r',newline='') as fh:
                csvreader = csv.DictReader(fh,
                                           delimiter=";"
                                           )
                if len(set(csvreader.fieldnames) -
                       set([x for x in self.fields.keys()])) == 0 :
                    print('Data base is ok.')

                    data = list(csvreader)
                else:
                    raise Exception('Error in the CSV file')
                    return
            
                return data
            
        else:
            #todo : add this branch in all load:
            #todo : message box about creating a database
            print('No Database. Creating one')
            
            empty_data= {key : '' for key in self.fields.keys()}
            self.save_entry(empty_data)
            print('Database created.')
            self.load_records()

        

##WIDGETS##
class TtkText(ttk.Entry):
    def __init__(self,parent=None,borderwidth=0.5,relief='solid',**kwargs):
        super().__init__(parent,'text',borderwidth=0.5,relief='solid',**kwargs)
        
class LabelEntry(tk.Frame):
    #todo: make it so it deal with tk.text too
    def __init__(self,parent,label,**kwargs):
        super().__init__(parent,**kwargs)
        self.var=tk.StringVar()
        self.MyLabel=ttk.Label(self,text=label)
        if parent.data.fields[label]['type']=='Entry':
            self.MyEntry=ttk.Entry(self,textvariable=self.var,**kwargs)
        else:
            self.MyEntry=TtkText(self,height=5)
        self.sep=ttk.Separator(self,orient="horizontal")

        

    def grid(self,row=None,column=None,sticky='we',**kwargs):
        super().grid(sticky='we',**kwargs)
        self.MyLabel.grid(row=0,column=0)
        self.sep.grid(row=1,column=0,sticky=sticky)
        self.MyEntry.grid(row=2,column=0,sticky=sticky)
        self.columnconfigure(0,weight=1)
        
        #self.grid(row=row,column=column,sticky=sticky,**kwargs)

    def get(self):
        return self.MyEntry.get()
        
class LabelCheckbutton(tk.Frame):
    def __init__(self,parent,label,chckbt_labels=None,**kwargs):
        super().__init__(parent,**kwargs)
        if isinstance(chckbt_labels,list):
            self.chckbt_labels=chckbt_labels
        else:
            raise Error("kwargs labels only takes list")
        
        self.MyLabel=ttk.Label(self,text=label)
        self.sep=ttk.Separator(self,orient="horizontal")
        self.FrameCheck=tk.Frame(self)
        
        self.MyLabel.grid(row=0,column=0)
        self.sep.grid(row=1,column=0,sticky='we')
        self.FrameCheck.grid(row=2,column=0)
        
        """creating multiple var"""
        #todo : to refactor
        self.dict_var={}
        for chckbt_label in chckbt_labels:
            newvar=chckbt_label
            self.dict_var[newvar]=tk.IntVar(value=0)
        
        """creating multiple checkboxes"""
        self.dict_chckbt={}
        for num,chckbt_label in enumerate(self.chckbt_labels):
            
            self.dict_chckbt[chckbt_label]=ttk.Checkbutton(self.FrameCheck,text=chckbt_label,variable=self.dict_var[chckbt_label])
            self.dict_chckbt[chckbt_label].grid(row=0,column=num)
            
    def grid(self,row=None,column=None,sticky='WE',**kwargs):
        super().grid(sticky=sticky,**kwargs)
        self.columnconfigure(0,weight=1)

    def get(self):
        return [self.dict_var[x].get() for x in self.dict_var]
        
        




        #self.grid(row=row,column=column,sticky=sticky,**kwargs)

    def calling(self):
        pass





##View##
class MyView(tk.Frame):
    def __init__(self,parent,data,commands):
        super().__init__(parent)
        self.data=data
        self.commands=commands
        self.Fields={}
        for num,field in enumerate(self.data.fields.keys()):
            if self.data.fields[field]['type'] in ['Entry','Text']:
                self.Fields[field]=LabelEntry(self,field)
                #self.Fields[field].grid(row=num,column=0,rowspan=1)
            elif self.data.fields[field]['type']=='Checkbox':
                self.Fields[field]=LabelCheckbutton(self,field,
                                                    chckbt_labels=self.data.fields[field]['list_name'])
                #self.Fields[field].grid(row=num,column=0,rowspan=1)
            #elif self.data.fields[field]['type']=='Text':
                #self.Fields[field]=TtkText(self)
                #self.Fields[field]=ttk.Entry(self,textvariable=tk.StringVar())
                #self.Fields[field].grid(row=num,column=0,rowspan=1)

            #print("field:")
            #print (self.Fields[field])
            self.Fields[field].grid(row=num,column=0,sticky='we')
        self.columnconfigure(0,weight=1)
        self.button_save=ttk.Button(self,text='Save',command=self.commands['save_entry'])
        self.button_save.grid(row=10,column=0,sticky='e')

    def get(self):
        data={}
        for field,widget in self.Fields.items():
            data[field]=widget.get()
        return data
        


            
                
                
            
            
            
            
        

class MyApplication(tk.Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.mdt=MyData()
        self.commands={'save_entry' : self.save_entry,
                       'load_records' : self.load_records
                       }
        self.mv=MyView(self,self.mdt,self.commands)
        

        self.mv.grid(row=0,column=0,sticky='nswe')
        self.columnconfigure(0,weight=1)

    def save_entry(self,data):
        
        self.mdt.save_entry(self.mv.get())
        

    def load_records(self):
        pass
    

if __name__=='__main__':
##    mdt=MyData()
##    lc=LabelCheckbutton(root,'Les gens concernés',chckbt_labels=mdt.fields['Les gens concernés']["list_name"])
##    lc.grid(row=0,column=0)
    
##    style=ttk.Style()
##    e=ttk.Entry(root,textvariable=tk.StringVar())
##    e_stylename=e.winfo_class()
##    e_layout=style.layout(e_stylename)
##    cb=ttk.Combobox(root)
##    cb_stylename = cb.winfo_class()
##    cb_layout=style.layout(cb_stylename)
##    
##    print(e_stylename)
##    pprint(e_layout)
##    pprint(style.element_options('Entry.textarea'))
    #print(cb_stylename)
    #pprint(cb_layout)
    
##    mdt=MyData()
##    mv=MyView(root,mdt,{})
##    mv.grid(row=0,column=0,sticky='we')
##    
##    root.columnconfigure(0,weight=1)
##    root.mainloop()
    app=MyApplication()
    app.mainloop()
    
    

        
    
