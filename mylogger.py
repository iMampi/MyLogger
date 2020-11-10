import tkinter as tk
from tkinter import ttk
import datetime as dt
from pprint import pprint
#todo : change readonly to the correct one
#todo : "les gens concerné" fix the boolvar
#todo : arrange display. it is centered, we dont want that
#todo : arrange size of ain window

class MyData:
    #todo : value o flist to save in csv. so they  will be load from csv
    def __init__ (self):
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

##WIDGETS##
class TtkText(ttk.Entry):
    def __init__(self,parent=None,borderwidth=0.5,relief='solid',**kwargs):
        super().__init__(parent,'text',borderwidth=0.5,relief='solid',**kwargs)
        
class LabelEntry:
    #todo: make it so it deal with tk.text too
    def __init__(self,parent,label,**kwargs):
        self.var=tk.StringVar()
        self.MyFrame=tk.Frame(parent)
        self.MyLabel=ttk.Label(self.MyFrame,text=label)
        if parent.data.fields[label]['type']=='Entry':
            self.MyEntry=ttk.Entry(self.MyFrame,textvariable=self.var,**kwargs)
        else:
            self.MyEntry=TtkText(self.MyFrame)
        sep=ttk.Separator(self.MyFrame,orient="horizontal")

        self.MyLabel.grid(row=0,column=0)
        sep.grid(row=1,column=0,sticky="WE")
        self.MyEntry.grid(row=2,column=0)

    def grid(self,*args,row=None,column=None,**kwargs):
        self.MyFrame.grid(*args,row=row,column=column,**kwargs)
        
class LabelCheckbutton:
    def __init__(self,parent,label,chckbt_labels=None):
        if isinstance(chckbt_labels,list):
            self.chckbt_labels=chckbt_labels
        else:
            raise Error("kwargs labels only takes list")
        
        self.MyFrame=tk.Frame(parent)
        self.MyLabel=ttk.Label(self.MyFrame,text=label)
        self.MyLabel.grid(row=0,column=0)
        sep=ttk.Separator(self.MyFrame,orient="horizontal")
        sep.grid(row=1,column=0,sticky="WE")
        self.FrameCheck=tk.Frame(self.MyFrame)
        self.FrameCheck.grid(row=2,column=0)

        
        """creating multiple var"""
        #todo : to refactor
        self.dict_var={}
        for chckbt_label in chckbt_labels:
            newvar=chckbt_label
            self.dict_var[newvar]=tk.IntVar(value=0)

        self.dict_chckbt={}
        for num,chckbt_label in enumerate(self.chckbt_labels):
            
            self.dict_chckbt[chckbt_label]=ttk.Checkbutton(self.FrameCheck,text=chckbt_label,variable=self.dict_var[chckbt_label])
            self.dict_chckbt[chckbt_label].grid(row=0,column=num)
            
    def grid(self,row=None,column=None,**kwargs):
        self.MyFrame.grid(row=row,column=column,**kwargs)

    def calling(self):
        pass





##View##
class MyView(tk.Frame):
    def __init__(self,parent,data):
        super().__init__(parent)
        self.data=data
        self.Fields={}
        for num,field in enumerate(self.data.fields.keys()):
            if self.data.fields[field]['type'] in ['Entry','Text']:
                self.Fields[field]=LabelEntry(self,field)
                #self.Fields[field].grid(row=num,column=0,rowspan=1)
            elif self.data.fields[field]['type']=='Checkbox':
                self.Fields[field]=LabelCheckbutton(self,field,chckbt_labels=self.data.fields[field]['list_name'])
                #self.Fields[field].grid(row=num,column=0,rowspan=1)
            #elif self.data.fields[field]['type']=='Text':
                #self.Fields[field]=TtkText(self)
                #self.Fields[field]=ttk.Entry(self,textvariable=tk.StringVar())
                #self.Fields[field].grid(row=num,column=0,rowspan=1)

            self.Fields[field].grid(row=num,column=0)


            
                
                
            
            
            
            
        


root=tk.Tk()
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
    
    mdt=MyData()
    mv=MyView(root,mdt)
    mv.grid(row=0,column=0)
    
    root.mainloop()

        
    
