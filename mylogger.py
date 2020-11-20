import tkinter as tk
from tkinter import ttk
import datetime as dt
from tkcalendar import *
import csv, os, json

#todo : change readonly to the correct one
#todo : add "select all" for chackbox label
#todo : implement messagebox
#todo : after reset, set a new ref automatically
#todo : arrange size of main window

##BASE##
class MyData:
    
    def __init__ (self):
        self.filename="database_mylogger.csv"
        self.list_file="list_file.json"
#        self.list_name=['Estelle','Mampi','Mario','Williamson','Santatra']
        self.list_name=[]
#        self.list_societe=['Roche Noire','Directimmo','Troc & Cash','MKR Property','Wave']
        self.list_societe=[]
        self.load_lists()
        

        self.fields={"Ref":{"type":'Entry',
                       "creation":{"visible":True,"state":"normal"},
                       "modification":{"visible":True,"state":"tk.ReadOnly"}
                           },
                "Date":{"type":'DateEntry',
                       "creation":{"visible":True,"state":"tk.Normal"},
                       "modification":{"visible":True,"state":"tk.Disabled"}
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
                "Alarme":{"type":'DateEntry',
                       "creation":{"visible":True,"state":"tk.Normal"},
                       "modification":{"visible":True,"state":"tk.Normal"}
                         }
                    }
        self.new_file()
        self.data=self.load_records()
        
    def new_file(self):
        """check if database exist"""
        newfile1= not os.path.exists(self.filename)
        if newfile1:
            
            with open(self.filename, 'w', newline='') as fh:
                csvwriter = csv.DictWriter(fh,
                                           fieldnames=[x for x in self.fields.keys()],
                                           delimiter=";"
                                           )
                csvwriter.writeheader()
            print('No database found. Created new database.')
                
        """check if json list exist"""
        newfile2= not os.path.exists(self.list_file)
        if newfile2:
            with open(self.list_file,'w') as fh:
                json.dump({'list_name':self.list_name,'list_societe':self.list_societe},fh)
            print('No datalist found. Created new datalist.')

        
    def save_entry(self,data):
        
        with open(self.filename, 'a',newline='') as fh:
                csvwriter = csv.DictWriter(fh,
                                           fieldnames=[x for x in self.fields.keys()],
                                           delimiter=";"
                                           )
                csvwriter.writerow(data)
        """
NOTE : here we can only use the csviterator once, because csv.DictReader return
a iterator. once it has been fully read (so the pointer goes to the end of the list,
it has no reason to exist anymore. it has done his job as a iterator.
what you can do to read it multiple time is :
    -design the algorythm so it is only used once;
    -make a copy of the iterator in memory (this is what we did here)
    -use itertool.tee (see documentation online)
    def load_records(self):
        existfile = os.path.exists(self.filename)
        if existfile:
            with open(self.filename, 'r',newline='') as fh:
                csviterator = csv.DictReader(fh,
                                           delimiter=";"
                                           )
                csvcopy=list(csviterator)
                if len(list(csvcopy))==0:
                    data = []
                elif len(set(csviterator.fieldnames) -
                    set([x for x in self.fields.keys()])) == 0 :
                    print('Data base is ok.')
                    print('set test')
                    print(set(csviterator.fieldnames))
                    print(set([x for x in self.fields.keys()]))
                    print(csvcopy)
                    data = csvcopy
                    print(data)
                else:
                    print("exception")
                    raise Exception('Error in the CSV file')
                    return
                print('last data')
                print(data)
                return data
            
        else:
            #todo : add this branch in all load:
            #todo : message box about creating a database
            print('No Database. Creating one')
            self.new_file()
            print('Database created.')
            self.load_records()
        """
    def load_records(self):
        existfile = os.path.exists(self.filename)
        if not existfile:
            self.newfile()
            return []
        
        
        with open(self.filename, 'r',newline='') as fh:
            csvreader = csv.DictReader(fh,
                                    delimiter=";"
                                    )
            missing_fields = set(csvreader.fieldnames) - \
                    set([x for x in self.fields.keys()])
            
            if len(missing_fields) > 0:
                raise Exception(
                    "File is missing fields: {}"
                    .format(', '.join(missing_fields))
                                )

            else:
                data =list(csvreader)
                return data
            

    def save_lists(self):
        with open(self.list_file,'w') as fh:
            json.dump({'list_name':self.list_name,'list_societe':self.list_societe},fh)
            
    def load_lists(self):
        existfile = os.path.exists(self.list_file)
        if existfile:
            with open(self.list_file,'r') as fh:
                data=fh.read()
                
                ml=json.loads(data)
            self.list_name=ml.get("list_name")
            self.list_name.sort()
            self.list_societe=ml.get("list_societe")
            self.list_societe.sort()
        else:
            #todo : add this branch in all load:
            #todo : message box about creating a database
            print('No Database list. Creating one')
            self.new_file()
            self.load_lists()
           

        

##WIDGETS##
class TtkText(ttk.Entry):
    
    def __init__(self,parent,borderwidth=0.5,relief='solid',**kwargs):
        
        super().__init__(parent,'text',borderwidth=0.5,relief='solid',**kwargs)

class MyDateEntry(tk.Frame):
    
    def __init__(self,parent,*args,textvariable=tk.StringVar,**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        self.entry_var=textvariable
        self.entry=ttk.Entry(self,textvariable=self.entry_var)
        vcmd=self.entry.register(self._validate)
        invcmd=self.entry.register(self._invalidate)
        self.entry.configure(
            validate='all',
            validatecommand=(vcmd,'%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd,'%P', '%s', '%S', '%V', '%i', '%d')
                        )

        self.button_cal=ttk.Button(self,text='...',command=self.top_cal,width=3)

        self.button_cal.grid(row=0,column=1,sticky='we')
        self.entry.grid(row=0,column=0,sticky='we')

    def top_cal(self):
        
        self.top=tk.Toplevel()
        self.top.update()
        
        self.cal_var=tk.StringVar()
        self.cal=Calendar(self.top,selectmode = 'day',
                          textvariable = self.cal_var,
                          date_pattern = 'dd/mm/y',
                          state = 'normal'
                          )
        self.top.bind('<Button-1>',self.select_date)

        self.cal.grid(row=0,column=0)

    def select_date(self,event):
        
        value=self.cal.get_date()
        if value!='':
            self.entry_var.set(value)
            self.top.destroy()
        


    def _validate(self, proposed, current, char, event, index, action):
        valid=False
        
        if event == 'focusout':
            if not self.entry.get():
                valid = False
            try:
                dt.datetime.strptime(self.entry.get(),"%d/%m/%Y")
                valid=True
            except ValueError:
                valid=False
        elif event =='key':
            if action =='0':
                valid = True
            elif index in ('0','1','3','4','6','7','8','9'):
                valid = char.isdigit()
            elif index in ('2','5'):
                valid = char=='/'
            else:
                valid=False
        return valid

    def _invalidate(self, proposed, current, char, event, index, action):
        pass

    def get(self):
        return self.entry.get()

    def set(self,value):
        self.entry_var.set(value)

    def grid(self,row=None,column=None,**kwargs):
        super().grid(row=row,column=column,**kwargs)

    def delete(self,first,last=tk.END):
        self.entry.delete(first,last)
        
        
class LabelEntry(tk.Frame):
    #todo: make it so it deal with tk.text too
    def __init__(self,parent,label,**kwargs):
        super().__init__(parent,**kwargs)
        self.parent=parent
        self.label=label
        self.var=tk.StringVar()
        self.MyLabel=ttk.Label(self,text=label)
        if parent.data.fields[label]['type']=='Entry':
            self.MyEntry=ttk.Entry(self,textvariable=self.var,**kwargs)
        elif parent.data.fields[label]['type']=='DateEntry':
            self.MyEntry=MyDateEntry(self,textvariable=self.var,**kwargs)    
        else:
            #self.MyEntry=TtkText(self,height=5)
            self.MyEntry=tk.Text(self,height=5,borderwidth=0.5,relief='solid')
        self.sep=ttk.Separator(self,orient="horizontal")


    def grid(self,row=None,column=None,sticky='we',**kwargs):
        super().grid(row=row,column=column,sticky='we',**kwargs)
        self.MyLabel.grid(row=0,column=0,sticky='w')
        self.sep.grid(row=1,column=0,sticky=sticky)
        self.MyEntry.grid(row=2,column=0,sticky=sticky)
        self.columnconfigure(0,weight=1)
        

    def get(self):
        print(self.parent.data.fields[self.label]['type'])
        if self.parent.data.fields[self.label]['type'] in ('Entry','DateEntry'):
            print(self.MyEntry.get())
            return self.MyEntry.get()
        else:
            print(self.MyEntry.get('1.0', tk.END))
            return self.MyEntry.get('1.0', tk.END)

    def set(self,newvalue,*args,**kwargs):
        self.var.set(newvalue,*args,**kwargs)
        
        
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
        
        self.MyLabel.grid(row=0,column=0,sticky='w')
        self.sep.grid(row=1,column=0,sticky='we')
        self.FrameCheck.grid(row=2,column=0,sticky='w')
        
        """creating multiple var"""
        #todo : to refactor
        self.dict_var={}
        for chckbt_label in self.chckbt_labels:
            newvar=chckbt_label
            self.dict_var[newvar]=tk.IntVar(value=0)
        
        """creating multiple checkboxes"""
        self.dict_chckbt={}
        for num,chckbt_label in enumerate(self.chckbt_labels):
            
            self.dict_chckbt[chckbt_label]=ttk.Checkbutton(self.FrameCheck,
                                                           text=chckbt_label,
                                                           variable=self.dict_var[chckbt_label])
            self.dict_chckbt[chckbt_label].grid(row=0,column=num)

        self.button_add=ttk.Button(self.FrameCheck,
                                   text="+",
                                   command= self.calling,
                                   width=3,
                                   )
        
        self.button_add.grid(row=0,column=len(self.chckbt_labels)+1,ipady=1, ipadx=0)
            
    def grid(self,row=None,column=None,sticky='WE',**kwargs):
        super().grid(row=row,column=column,sticky=sticky,**kwargs)
        self.columnconfigure(0,weight=1)

    def get(self):
        #return [self.dict_var[x].get() for x in self.dict_var]
        """return a dict"""
        data={}
        for name,var in self.dict_var.items():
            data[name]=var.get()
        return data

    def set(self,dict_value):
        #todo : add a len checker
        """dict value must be a dict """
        for name,value in dict_value.items:
            self.dict_var[name].set(value)

    def calling(self):
        pass

##VIEW##
class MyView(tk.Frame):
    def __init__(self,parent,data,commands):
        super().__init__(parent)
        self.data=data
        self.commands=commands
        """we put our Fields's widget in a dict"""
        self.Fields={}
        for num,field in enumerate(self.data.fields.keys()):
            if self.data.fields[field]['type'] in ['Entry','DateEntry','Text']:
                self.Fields[field]=LabelEntry(self,field)
                #self.Fields[field].grid(row=num,column=0,rowspan=1)
            elif self.data.fields[field]['type']=='Checkbox':
                self.Fields[field]=LabelCheckbutton(self,field,
                                                    chckbt_labels=self.data.fields[field]['list_name'])
            self.Fields[field].grid(row=num,column=0,sticky='we',pady=2)


        self.button_add=ttk.Button(self,text='+',command=self.commands['add'])
        #self.button_add.grid(row=,column=
        self.columnconfigure(0,weight=1)
        self.button_save=ttk.Button(self,text='Save',command=self.commands['save_entry'])
        self.button_save.grid(row=10,column=0,sticky='e')

    def get(self):
        data={}
        for field,widget in self.Fields.items():
            data[field]=widget.get()
        return data

    def set(self,data):
        """data must be a dict"""
        for field,value in data.items():
            data[field].set(value)

    def reset(self):
        for field,widget in self.Fields.items():
            if field in ('Ref','Date','Alarme'):
                widget.MyEntry.delete(0,tk.END)
            elif field == 'Note':
                widget.MyEntry.delete('1.0',tk.END)
            else:
                for var in widget.dict_var.values():
                    var.set(0)
                
            
        
        

class WidgetAdd(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.MyEntry=ttk.Entry(self,textvariable=tk.StringVar())
        self.MyEntry.grid(row=0,column=0,sticky='we')
        self.MyButton=ttk.Button(self,text='Save')
        self.MyButton.grid(row=1,column=0,sticky='e')
        self.columnconfigure(0,weight=1)


##CONTROLER##
class MyApplication(tk.Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.mode=None
        self.mdt=MyData()
##        self.data=self.mdt.load_records()
##        print("data show")
##        print(self.data)
##
##        print(self.mdt.load_records())
        #self.data=self.mdt.data
        self.commands={'save_entry' : self.save_entry,
                       'load_records' : self.load_records,
                       'add' : self.add
                       }
        self.mv=MyView(self,self.mdt,self.commands)
        
        """auto fill date with today's date"""
        td=dt.date.today()
        self.mv.Fields['Date'].set(td.strftime("%d/%m/%Y"))

        """auto fill ref"""
        #print(self.mdt.data)
        #print(len(self.mdt.data))
        if len(self.mdt.data)==0:
            newref = "ref0001"
        else :
            lastref = self.mdt.data[-1]['Ref']
            refnum=lastref.split('ref')[1]
            newnum=int(refnum)+1
            newref='ref'+str('{:04d}'.format(newnum))
        print(newref)
        self.mv.Fields['Ref'].set(newref)
            
        self.mv.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
        self.columnconfigure(0,weight=1)

    def save_entry(self):
        
        self.mdt.save_entry(self.mv.get())
        self.mv.reset()
        
    def load_records(self):
        pass

    def add(self):
        top=WidgetAdd()
        
        
    

if __name__=='__main__':
    app=MyApplication()
    app.mainloop()
    
    

        
    
