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
#todo : ask confirmation when something has changed qhen quiting
#todo : viewall to update when saving after changed
#todo : update viewall (append) when adding new entry
#todo : think about adding a deleteentry option
#to fix : on a une erreur quand on edit une entrée. erreurs lors de load_reccords

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
                       "consultation":{"visible":True,"state":"readonly"},
                            
                           },
                "Date":{"type":'DateEntry',
                       "creation":{"visible":True,"state":"normal"},
                       "consultation":{"visible":True,"state":"readonly"}
                       },
                "Note":{"type":'Text',
                       "creation":{"visible":True,"state":"normal"},
                       "consultation":{"visible":True,"state":"normal"}
                       },
                "Les gens concernés":{"type":'Checkbox',
                                      "creation":{"visible":True,"state":"normal"},
                                      "consultation":{"visible":True,"state":"disabled"},
                                      "list":self.list_name,
                                      "command":"add_name"
                                      },
                "Sociétés/Personnel":{"type":'Checkbox',
                                      "creation":{"visible":True,"state":"normal"},
                                      "consultation":{"visible":True,"state":"disabled"},
                                      "list":self.list_societe,
                                      "command":"add_societe"
                                     },
                "Alarme":{"type":'DateEntry',
                       "creation":{"visible":True,"state":"normal"},
                       "consultation":{"visible":True,"state":"disabled"}
                         }
                    }
        self.new_file()
        
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

        
    def save_entry(self,data,mode):
        #tofix: add different treatment for new entry and edited entry
        
        
        if mode =="creation":
            #here data is a dict
            for field,value in data.items():
                if value=='':
                    data[field]='None'
            with open(self.filename, 'a',newline='',encoding='utf-8') as fh:
                csvwriter = csv.DictWriter(fh,
                                        fieldnames=[x for x in self.fields.keys()],
                                        delimiter=";"
                                        )
                csvwriter.writerow(data)
        else:
            #here data is a list of dict
            for row in data:
                for field,value in row.items():
                    if value=='':
                        row[field]='None'

            with open(self.filename, 'w',newline='',encoding='utf-8') as fh:
                csvwriter = csv.DictWriter(fh,
                                        fieldnames=[x for x in self.fields.keys()],
                                        delimiter=";"
                                        )
                csvwriter.writeheader()
                for row in data:
                    csvwriter.writerow(row)

            
            

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
        #todo : catch error when file is empty or missing a field
        existfile = os.path.exists(self.filename)
        if not existfile:
            self.newfile()
            return []
        
        
        with open(self.filename, 'r',newline='',encoding='utf-8') as fh:
            csvreader = csv.DictReader(fh,
                                    delimiter=";"
                                    )
            missing_fields = set(csvreader.fieldnames) - \
                    set([x for x in self.fields.keys()])
            
            if len(missing_fields) > 0:
                raise Exception(
                    
                    "File is missing fields: {}".format(', '.join(missing_fields))
                    )
                                

            else:
                data =list(csvreader)
                #print(data[0][])
                for row in data:
                    for field,value in row.items():
                        if value=='None':
                            row[field]=''
                return data
            

    def save_lists(self):
        with open(self.list_file,'w') as fh:
            json.dump({'list_name':self.list_name,'list_societe':self.list_societe},fh)
        print('saved lists')
            
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

class MyDateEntry(tk.Frame):
    
    def __init__(self,parent,*args,textvariable=tk.StringVar,state='Normal',**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.entry_var=textvariable
        
        self.entry=ttk.Entry(self,textvariable=self.entry_var,state=state)
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
    def __init__(self,parent,label,state='normal',**kwargs):
        super().__init__(parent,**kwargs)
        #self.mode=mode
        self.parent=parent
        self.label=label
        self.var=tk.StringVar()
        self.MyLabel=ttk.Label(self,text=label)
        if parent.data.fields[label]['type']=='Entry':
            self.MyEntry=ttk.Entry(self,
                                   textvariable=self.var,
                                   state=state,
                                   **kwargs)
        elif parent.data.fields[label]['type']=='DateEntry':
            self.MyEntry=MyDateEntry(self,
                                     textvariable=self.var,
                                     state=state,
                                     **kwargs)    
        else:
            #self.MyEntry=TtkText(self,height=5)
            self.MyEntry=tk.Text(self,
                                 height=5,
                                 borderwidth=0.5,
                                 relief='solid',
                                 state=state)
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
        if self.parent.data.fields[self.label]['type'] in ('Entry','DateEntry'):
            #print(self.MyEntry.get())
            self.var.set(newvalue,*args,**kwargs)
        else:
            self.MyEntry.insert('1.0',newvalue,*args,**kwargs)


        
        #self.var.set(newvalue,*args,**kwargs)
        
        
class LabelCheckbutton(tk.Frame):
    
    def __init__(self,parent,label,model,chckbt_labels=None,**kwargs):
        
        super().__init__(parent,**kwargs)
        self.model=model
        self.label=label
        
        
        if isinstance(model.fields[self.label]['list'],list):
            self.chckbt_labels=model.fields[self.label]['list']
        else:
            raise Error("Wrong model, chckbt_labels only takes list")
        
        self.MyLabel=ttk.Label(self,text=self.label)
        self.sep=ttk.Separator(self,orient="horizontal")
        self.FrameCheck=tk.Frame(self)
        
        self.MyLabel.grid(row=0,column=0,sticky='w')
        self.sep.grid(row=1,column=0,sticky='we')
        self.FrameCheck.grid(row=2,column=0,sticky='w')

        self.dict_var={}
        self.dict_chckbt={}
        self.button_add=ttk.Button(self.FrameCheck,
                                       text="+",
                                       command=self.add_new,
                                       width=3,
                                       )
        self.generate_chckbt()

    def generate_chckbt(self):
        """creating multiple var"""
        #todo : to refactor

        for chckbt_label in self.chckbt_labels:
            newvar=chckbt_label
            if newvar not in self.dict_var.keys():
                self.dict_var[newvar]=tk.IntVar(value=0)
        
        """creating multiple checkboxes"""
        for num,chckbt_label in enumerate(self.chckbt_labels):
            if chckbt_label not in self.dict_chckbt.keys():
                self.dict_chckbt[chckbt_label]=ttk.Checkbutton(self.FrameCheck,
                                                           text=chckbt_label,
                                                           variable=self.dict_var[chckbt_label])
                self.dict_chckbt[chckbt_label].grid(row=0,column=num)

        self.button_add.grid_forget()
        self.button_add.grid(row=0,
                            column=len(self.chckbt_labels)+1,
                            ipady=1, ipadx=0
                            )

    class WidgetAdd(tk.Frame):
        def __init__(self,parent,outer_instance):
            super().__init__(parent)
            #todo : add more text, title, adjust padding, wiget size
            """create an attribut to store the outer instance, so we can acces it later"""
            self.outer_instance=outer_instance
            self.parent=parent
            self.MyVar=tk.StringVar()
            self.MyEntry=ttk.Entry(self,textvariable=self.MyVar)
            self.MyEntry.grid(row=0,column=0,sticky='we')
            self.MyButton=ttk.Button(self,text='Save',command=self.save_new)
            self.MyButton.grid(row=1,column=0,sticky='e')
            self.columnconfigure(0,weight=1)

        def get(self):
            return self.MyVar.get()

        def save_new(self):
            new=self.get()
            #self.outer_instance.model.list_name.append(new)
            self.outer_instance.model.fields[self.outer_instance.label]['list'].append(new)

            self.outer_instance.generate_chckbt()
            self.parent.destroy()
            self.outer_instance.update()
            self.outer_instance.model.save_lists()


            
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
        #print(type(eval(dict_value)))
        """when loaded from csv, data is all string. we convert it into a dict"""
        data=eval(dict_value)
        for name,value in data.items():
            self.dict_var[name].set(value)

    def add_new(self):
        self.top=tk.Toplevel(self)
        self.wa=self.WidgetAdd(self.top,self)
        self.wa.grid(row=0,column=0,sticky='nswe')

class ViewAll(ttk.Treeview):
    def __init__(self,parent,model,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.model=model
        #self.parent=parent
        self.headers=self.model.fields.keys()
        self.configure(columns=[*self.headers],show="headings")
        
                       
        #self.heading('#0',text='N°')
        #self.column('#0',minwidth=40,width=40,stretch=True)
        #todo : remove the first column '#0'
        for header in self.headers:
            self.heading(header,text=header)
            self.column(header, minwidth=40, width=80,stretch=True)

        ybar=ttk.Scrollbar(parent,orient="vertical",command=self.yview)
        ybar.grid(row=0,column=1,sticky='nse')
        xbar=ttk.Scrollbar(parent,orient="horizontal",command=self.xview)
        self.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        xbar.grid(row=1,column=0,sticky='swe')

            
    def grid(self,*args,row=None,column=None,sticky='nswe',**kwargs):
        super().grid(*args,row=row,column=column,sticky=sticky,**kwargs)

    def populate(self,data):
        counter=0
        for row_data in data:
            row_values = [row_data[header] for header in self.headers ]
            self.insert('', 'end', iid=counter, values=row_values)
            counter += 1


 

        
##VIEW##
class MyView(tk.Frame):
    def __init__(self,parent,data,mode,commands):
        super().__init__(parent)
        #todo : add button edit and grey save
        self.mode=mode
        self.data=data
        self.commands=commands
        """we put our Fields's widget in a dict"""
        self.Fields={}
        for num,field in enumerate(self.data.fields.keys()):
            if self.data.fields[field]['type'] in ['Entry','DateEntry','Text']:
                self.Fields[field]=LabelEntry(self,field)
            elif self.data.fields[field]['type']=='Checkbox':
                self.Fields[field]=LabelCheckbutton(self,field,
                                                    self.data,chckbt_labels=self.data.fields[field]['list']
                                                    )
            self.Fields[field].grid(row=num,column=0,sticky='we',pady=2)

        self.columnconfigure(0,weight=1)

        self.button_edit=ttk.Button(self,text='Edit',command=self.commands['mode_edit'])
        self.button_edit.grid(row=10,column=1,sticky='e')

        self.button_save=ttk.Button(self,text='Save',command=self.commands['save_entry'])
        self.button_save.grid(row=10,column=0,sticky='e')

        self.update_idletasks()
            
        
        #self.button_print=ttk.Button(self,text='view all',command=self.commands['print_'])
        #self.button_print.grid(row=10,column=1,sticky='e')
        

    def get(self):
        data={}
        for field,widget in self.Fields.items():
            data[field]=widget.get()
        return data

    def set(self,data):
        """data must be a dict"""
        #print(data.items())
        for field,value in data.items():
            #print(data[field])
            #print(value)
            self.Fields[field].set(value)

    def reset(self):
        for field,widget in self.Fields.items():
            if field in ('Ref','Date','Alarme'):
                widget.MyEntry.delete(0,tk.END)
            elif field == 'Note':
                widget.MyEntry.delete('1.0',tk.END)
            else:
                for var in widget.dict_var.values():
                    var.set(0)

    def change_state(self,state):
        #todo : to refactor so it depends on widget type. might need to make them uniform
        if state == "disabled" :
            color='#d9d9d9'
        else:
            color='white'
            
        for field,widget in self.Fields.items():
            if field in ("Ref","Note"):
                widget.MyEntry.configure(state=state,background=color)
            elif field in ("Date","Alarme"):
                widget.MyEntry.entry.configure(state=state,background=color)
            else :
                for chckbt in widget.dict_chckbt.values():
                    chckbt.configure(state=state)
                widget.button_add.configure(state=state)

        self.update_idletasks()

        if self.mode=="consultation":
            self.button_save.configure(state="disabled")
        else :
            self.button_edit.configure(state="disabled")
            self.button_save.configure(state="normal")



        
                


        
        


##CONTROLER##
class MyApplication(tk.Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.mode="consultation"
        self.mdt=MyData()
        self.selected=None
        self.commands={'save_entry' : self.save_entry,
                       'load_records' : self.load_records,
                       'new_log' : self.new_log,
                       'mode_edit': self.mode_edit
                       }
        self.records=self.mdt.load_records()
        #####
        self.button_new = ttk.Button(self,text="New log",command = lambda : self.commands['new_log']("creation"))
        #todo : catch error if argument is neither creation or consultation
        self.button_new.grid(row=0,column=0,sticky='w',padx=5,pady=5)
        
        self.geometry("500x200")
        self.minsize(width=250, height=200)
        self.title("Historique")
        self.maxsize(width=1000, height=500)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=0)
        self.rowconfigure(1,weight=1)

        f=tk.Frame(self)
        f.grid(row=1,column=0,sticky='nswe',padx=5,pady=5)
        f.columnconfigure(0,weight=1)
        f.rowconfigure(0,weight=1)
        self.viewall=ViewAll(f,self.mdt)
        self.viewall.grid(row=0,column=0,sticky='nswe')
        self.viewall.columnconfigure(0,weight=1)
        self.viewall.rowconfigure(0,weight=1)
        
        self.viewall.populate(self.records)
        
        self.update_idletasks()

        self.viewall.bind('<<TreeviewOpen>>', self.doubleclick_viewall)
        #####






    def save_entry(self):
        #tofix : when we save a edited log. it is saved last in the csv,not replacing the old log 

            if self.mode=="creation":
                record=self.mv.get()
                values = [record[header] for header in self.mdt.fields.keys() ]
                #self.insert('', 'end', iid=counter, values=row_values)

                print(record)
                self.mdt.save_entry(record,self.mode)
                self.mv.reset()
                self.top1.destroy()
                self.update()

                #we update viewall now if new log or an update        
                if self.selected==None:
                    self.viewall.insert('', 'end', iid=len(self.records)+1, values=values)
                else:
                    self.viewall.item(self.selected, text='', values=values)
            else:
                record=self.mv.get()
                values = [record[header] for header in self.mdt.fields.keys() ]
                #self.insert('', 'end', iid=counter, values=row_values)

                print(record)
                self.records[int(self.selected)]=record
                
                self.mdt.save_entry(self.records,self.mode)
                self.mv.reset()
                self.top1.destroy()
                self.update()

                #we update viewall now if new log or an update        
                if self.selected==None:
                    self.viewall.insert('', 'end', iid=len(self.records)+1, values=values)
                else:
                    self.viewall.item(self.selected, text='', values=values)

            self.records=self.mdt.load_records()

                

        
        #todo : insert messagebox "saved"
        
    def load_records(self):
        pass
    
    def new_log(self,mode):
        self.top1=tk.Toplevel(self)
        self.mode=mode
        self.mv=MyView(self.top1,self.mdt,self.mode,self.commands)

        if mode=="consultation":
            self.top1.title("Consulting log")
        else :
            self.top1.title("Creating log")

            """auto fill date with today's date"""
            td=dt.date.today()
            self.mv.Fields['Date'].set(td.strftime("%d/%m/%Y"))

            """auto fill ref"""
            if len(self.records)==0:
                newref = "ref0001"
            else :
                lastref = self.records[-1]['Ref']
                refnum=lastref.split('ref')[1]
                newnum=int(refnum)+1
                newref='ref'+str('{:04d}'.format(newnum))
                #print(newref)
                self.mv.Fields['Ref'].set(newref)


        #####
        
            
        self.mv.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)

        self.columnconfigure(0,weight=1)
        
        
        #####


        
    def doubleclick_viewall(self,*args):
        #todo : fix this so it open the selected line in edit or readonly mode
        self.mode="consultation"
        self.new_log("consultation")
        current = self.viewall.focus()
        self.selected=current
        values = self.viewall.set(current)
        ref=values["Ref"]
        data=self.mdt.load_records()
        #print(data)
        for row,values in enumerate(data):
            if values['Ref']==ref:
                row_index=row
                #self.construction(myindex=row_index)
                self.mv.reset()
                #print(data[row_index])
                self.mv.set(data[row_index])
                self.mv.change_state('disabled')
                
                #self.top1.destroy()
                break

    def mode_edit(self):
        self.mv.mode="creation"
        self.mv.change_state("normal")
        self.update()
        self.mv.update()



    def print_(self):
        print(self.var_list_name.get())
        print(self.mv.Fields["Les gens concernés"].chckbt_labels)

    

if __name__=='__main__':
    app=MyApplication()
    style=ttk.Style()
    app.mainloop()
    
    

        
    
