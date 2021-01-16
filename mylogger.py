import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime as dt
from tkcalendar import *
import csv, os, json, itertools

#done : no confirmation when quitting while cosulting
#done : no confirming when modificaiton, and no change was made
#done : converting chckbox data into dict imediatly when loaded
#done : now text.get return no linebreak anymore
#done : dateentry dealing error differently if req or not 
#done : in dict for "les gens concernés" and "société", it saves only the keys existing when it was saved,
#   not all the existing keys. so when comparing, it will always not be right
#   >>> fix the dicts : only save the keys where the value is 1
#done : fix empty date to return today's date
#done : update self records everytime a new entryis added or modified
#done : saving new log, adding it to treeview
#done : when editing a log, when i press exit, it ask confirmaiton whereas i changed nothing.
#done : deleting multiple lines and solo line
#done : add checkbox filter by gens concerné et csociete - complex filter
#done : when focusing LABELENTRY with date, make it so moving from entry to cal doestnt ccall error


####commit did a lot 001####

#done: displace data treatement with save in App into save in Model
#done: replacing self.Alarme with self.statu in app.save_entry
###commit 002###

#done : removed self.Alarmme from code
#done : in modification, auto change Staus when changing date from something to nothing
#done : complexfilter - finish the display layout
#done : complexfilter - command APPLy
#done : command -  populate according to complex filter selection
###commit 003###

#done : add "select all" for chackbox label
#done : in RESULTAT, implement doubleclick -- change design of doubleckick so it works for whatever instnce of Viewall
#>>> get the name of the widget which has focus, then applying the methods on it
#done : remove size max of main window
###commit 004###

#done : introduction de "Trop tard"
#done : maj auto from "En cours" to ""trop tard"
#done : implemented "Suivi" (which is "en cours" and "trop tard")
#done : ajouter colonne "nombre de jour avant deadline"
###commit 005###

#todo : compare the memory usage of the two approach for updating treeview . destroy populate vs update just 1 entry
#todo : update function for update treeview (destroypopulate)
#todo : add linebreak when checkbox options doesnt fit in one line
#todo : when in disabled mode, disable the calendar button too
#todo : gestion des alarmes : ceux en cours, ceux passé, ceux terminés, récurrence,...
#todo : introduire la récurrence po ur les alarme
#todo : introduire tri en cliquant sur les colones
#todo : quand survol sur un row, info bulle qui montre le nombre de jours restant
#todo : add option filter by word in complexfilter
#todo : create a widget datefourchette for filter use only (init,get,grid,set,etc...) to make it easier
#todo : move the onclick and double click method into the ViewAll class

FIELDS={"Ref":{"type":'Entry',
               "creation":{"visible":True,"state":"normal"},
                "modification":{"visible":True,"state":"normal"},
               "consultation":{"visible":True,"state":"readonly"},
                "width":50,
                "req":True
                   },
        "Date":{"type":'DateEntry',
               "creation":{"visible":True,"state":"normal"},
                "modification":{"visible":True,"state":"normal"},
               "consultation":{"visible":True,"state":"readonly"},
                "width":70,
                "req":True

               },
        "Note":{"type":'Text',
               "creation":{"visible":True,"state":"normal"},
                "modification":{"visible":True,"state":"normal"},
               "consultation":{"visible":True,"state":"normal"},
                "width":200,
               "req":True
               },
        "Les gens concernés":{"type":'Checkbox',
                              "creation":{"visible":True,"state":"normal"},
                              "modification":{"visible":True,"state":"normal"},
                              "consultation":{"visible":True,"state":"disabled"},
                              "list":[],
                              "command":"add_name",
                              "width":150,
                                "req":True
                              
                              },
        "Sociétés/Personnel":{"type":'Checkbox',
                              "creation":{"visible":True,"state":"normal"},
                              "modification":{"visible":True,"state":"normal"},
                              "consultation":{"visible":True,"state":"disabled"},
                              "list":[],
                              "command":"add_societe",
                              "width":150,
                             "req":True

                             },
        "Alarme":{"type":'DateEntry',
               "creation":{"visible":True,"state":"disabled"},
                "modification":{"visible":True,"state":"normal"},
               "consultation":{"visible":True,"state":"disabled"},
               "width":70,
                  "req":False
                 },
        "Status":{"type":'ComboboxEntry',
               "creation":{"visible":False,"state":"normal"},
                "modification":{"visible":True,"state":"normal"},
               "consultation":{"visible":True,"state":"disabled"},
                  "list":[],
               "width":70,
                  "req":True
                  },
        "ETA":{"type":'Entry',
               "creation":{"visible":False,"state":"normal"},
                "modification":{"visible":False,"state":"normal"},
               "consultation":{"visible":False,"state":"disabled"},
                  "list":[],
               "width":115,
                  "req":False
                  }
                }
def testdate(date):
    try:
        dt.datetime.strptime(date,"%d/%m/%Y")
        value=True
    except:
        value=False
    finally:
        return value


##BASE##
class MyData:
    filename="database_mylogger.csv"
    list_file="list_file.json"
    list_societe=[]
    list_status=['Note', 'En cours', 'Trop tard', 'Terminé']
    list_name=[]

    def __init__ (self):
        self.load_lists()
        self.new_file()


        self.fields=FIELDS
        for name in self.list_name:
            self.fields["Les gens concernés"]['list'].append(name)
        for societe in self.list_societe:
            self.fields["Sociétés/Personnel"]['list'].append(societe)
        for statu in self.list_status:
            self.fields["Status"]['list'].append(statu)


        
        
        self.filter_fields={"Date début":{"type":'DateEntry',
                                      "creation":{"visible":True,"state":"normal"},
                                      "consultation":{"visible":True,"state":"disabled"},
                                      "width":150
                                     },
                            "Date fin":{"type":'DateEntry',
                                      "creation":{"visible":True,"state":"normal"},
                                      "consultation":{"visible":True,"state":"disabled"},
                                      "width":150
                                     },
                            "Les gens concernés":self.fields["Les gens concernés"],
                            "Sociétés/Personnel":self.fields["Sociétés/Personnel"],
                            "Mots clefs dans notes":{"type":'Entry',
                                      "creation":{"visible":True,"state":"normal"},
                                      "consultation":{"visible":True,"state":"disabled"},
                                      "width":150
                                     },
                            "Status":self.fields["Status"],
                            }
        
    def new_file(self):
        """check if database exist"""
        newfile1= not os.path.exists(self.filename)
        if newfile1:
            
            with open(self.filename, 'w', newline='',encoding='utf-8') as fh:
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
        
        if mode =="creation":
            #here data is a dict
            if 'Status' not in data.keys() or data['Status'] in [None, '']:
                if data['Alarme'] in (None,'','None'):
                    data['Status']='Note'
                else:
                    data['Status']='En cours'
                    
                for field,value in data.items():
                    if value in (None,'','\n'):
                        data[field]='None'


            with open(self.filename, 'a',newline='',encoding='utf-8') as fh:
                csvwriter = csv.DictWriter(fh,
                                        fieldnames=[x for x in self.fields.keys()],
                                        delimiter=";"
                                        )
                csvwriter.writerow(data)
            return True
        
        else:
            #here data is a list of dict

            for row in data:
                for field,value in row.items():
                    if value in ('',None,'\n'):
                        row[field]='None'
                    if field == 'Status' and value not in self.list_status:
                        value='Note'

            with open(self.filename, 'w',newline='',encoding='utf-8') as fh:
                csvwriter = csv.DictWriter(fh,
                                        fieldnames=[x for x in self.fields.keys()],
                                        delimiter=";"
                                        )
                csvwriter.writeheader()
                for row in data:
                    csvwriter.writerow(row)
            return True

            
            

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
        #todo : catch error when file is empty
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
                data = list(csvreader)
                """converting some data into python data"""
                for row in data:
                    for field,value in row.items():
                        if value=='None':
                            row[field]=''
            #we update statut of log with alarm to know if too late 
            #we directly convert our string loaded from save that should be a dict into a dict 
            #we treat and update the ETA
            chck_fields=[x for x in self.fields if self.fields[x]['type']=='Checkbox']
            for row in data:
                if row['Status'] == "En cours":
                    if dt.datetime.strptime(row['Alarme'],"%d/%m/%Y") < dt.datetime.now():
                        row['Status'] = "Trop tard"

                if row['Status'] in ("En cours", "Trop tard"):
                    ETA = dt.datetime.now() - dt.datetime.strptime(row['Alarme'],"%d/%m/%Y")
                    x=str(-int(ETA.days))+' days, '+str(format(int(ETA.seconds/3600),'.1f'))+' hours'
                    if dt.datetime.strptime(row['Alarme'],"%d/%m/%Y") < dt.datetime.now():
                        x="- "+x.replace("-","")
                    row['ETA'] = x
                else:
                    row['ETA'] = 0
                    
                    

                for field in chck_fields:
                    converted=eval(row[field])
                    row[field]=converted

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
            messagebox.showinfo(title='Information',
                                message='No list database found :',
                                detail='New list database created',
                                )
            self.new_file()
            self.load_lists()
           

##WIDGETS##
class MyCombobox(ttk.Combobox):
    def __init__(self,parent,*args,textvariable=None,values=None,**kwargs):
        super().__init__(parent,*args,textvariable=textvariable,values=values,**kwargs)
        self.var = textvariable
        self.values=[*values,'Tout']
        #self.var.trace('w',self.filter)
        #self.bind("<<ComboboxSelected>>", self.event_generate('<Button-1>'))



 


        

##    def filter(self,*args):
##        myinput=self.var.get().lower()
##        init_values=self.values
##        selection=[]
##        for element in self.values:
##            if element.lower().startswith(myinput):
##                selection.append(element)
##        if len(selection) == 1 :
##            self.configure(values=selection)
##            #self.var.set(*selection)
##            self.event_generate('<Down>')
        

class MyDateEntry(tk.Frame):
    
    def __init__(self,parent,*args,textvariable=tk.StringVar,state='Normal',**kwargs):
        
        super().__init__(parent,*args,**kwargs)
        
        self.entry_var=textvariable
        self.parent=parent
        
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
        
        self.top=tk.Toplevel(self,name='top3')
        """must add focus first, otherwise the grab won't work on first click, but on second click"""
        self.top.focus_set()
        self.top.grab_set()

        self.top.update_idletasks()

        self.cal_var=tk.StringVar()
        self.cal=Calendar(self.top,selectmode = 'day',
                          textvariable = self.cal_var,
                          date_pattern = 'dd/mm/y',
                          state = 'normal'
                          )
        self.cal.update_idletasks()
        self.top.bind('<Button-1>',self.select_date)

        self.cal.grid(row=0,column=0)
        
        self.top.protocol('WM_DELETE_WINDOW',
                            lambda : self.parent.parent.commands['quit_w'](self.top))


    def select_date(self,event):
        
        value=self.cal.get_date()
        if value!='':
            self.entry_var.set(value)
            self.parent.parent.commands['quit_w'](self.top,save=True)

    def _validate(self, proposed, current, char, event, index, action):
        if FIELDS[self.parent.label]['req']:
            v=self.validate_req(proposed, current, char, event, index, action)
        else:
            v=self.validate_noreq(proposed, current, char, event, index, action)

        return v

    def validate_req(self, proposed, current, char, event, index, action):
        valid=True
        if event == 'focusout':
            if not self.entry.get():
                td=dt.date.today()
                self.entry_var.set(td.strftime("%d/%m/%Y"))

            else:
                print('else')
                print(not self.entry.get())
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
        elif event == 'focusin':
            valid= True
        return valid

    def validate_noreq(self, proposed, current, char, event, index, action):
        valid=True
        if event == 'focusout':
            if not self.entry.get():
                pass
##                print('empty')
            else:
##                print('else')
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
        elif event == 'focusin':
            valid= True
        return valid

    def _invalidate(self, proposed, current, char, event, index, action):
        print(proposed, current, char, event, index, action)
        if FIELDS[self.parent.label]['req']:
            inv=self._invalidate_req(proposed, current, char, event, index, action)
        else:
            inv=self._invalidate_noreq(proposed, current, char, event, index, action)
        
        messagebox.showerror(title='Erreur',
                            message='Date non valide:',
                             detail='Veuillez saisir ou sélectionner une date valide',
                             parent=self)
        return inv
    
    def _invalidate_req(self, proposed, current, char, event, index, action):
        td=dt.date.today()
        self.entry_var.set(td.strftime("%d/%m/%Y"))

    def _invalidate_noreq(self, proposed, current, char, event, index, action):
        self.entry_var.set('')


    def get(self):
        return self.entry.get()

    def set(self,value):
        self.entry_var.set(value)

    def grid(self,row=None,column=None,**kwargs):
        super().grid(row=row,column=column,**kwargs)

    def delete(self,first,last=tk.END):
        self.entry.delete(first,last)
        
        
class LabelEntry(tk.Frame):
    def __init__(self,parent,label,model,**kwargs):
        super().__init__(parent,**kwargs)

        self.parent=parent
        self.model=model
        self.label=label
        self.var=tk.StringVar()
        self.MyLabel=ttk.Label(self,text=label)
        if isinstance(parent,MyView):
            
            checker=self.model.fields
        else:
            checker=self.model.filter_fields


        
        if checker[label]['type']=='Entry':
            self.MyEntry=ttk.Entry(self,
                                   textvariable=self.var,
                                   **kwargs)
        elif checker[label]['type']=='DateEntry':
            self.MyEntry=MyDateEntry(self,
                                     textvariable=self.var,
                                     **kwargs)
        elif checker[label]['type']=='ComboboxEntry':
            self.MyEntry=MyCombobox(self,
                                     textvariable=self.var,
                                     values=checker[label]['list'],
                                     **kwargs)
        else:
            self.MyEntry=tk.Text(self,
                                 height=5,
                                 borderwidth=0.5,
                                 relief='solid')
        self.sep=ttk.Separator(self,orient="horizontal")


    def grid(self,row=None,column=None,sticky='we',**kwargs):
        super().grid(row=row,column=column,sticky='we',**kwargs)
        self.MyLabel.grid(row=0,column=0,sticky='w')
        self.sep.grid(row=1,column=0,sticky=sticky)
        self.MyEntry.grid(row=2,column=0,sticky=sticky)
        self.columnconfigure(0,weight=1)
        

    def get(self):
        try:
            type_=self.model.filter_fields[self.label]['type']
        except:
            type_=self.model.fields[self.label]['type']
        finally:
            if 'Entry' in type_ :
                return self.MyEntry.get()
            else:
                #since in Text, the value will always contains \n in the end, we use rstrip to remove it
                return self.MyEntry.get('1.0', tk.END).rstrip()

    def set(self,newvalue,*args,**kwargs):
        if 'Entry' in self.model.fields[self.label]['type'] :
            self.var.set(newvalue,*args,**kwargs)
        else:
            self.MyEntry.insert('1.0',newvalue,*args,**kwargs)

        
class LabelCheckbutton(tk.Frame):
    
    def __init__(self,parent,label,model,chckbt_labels=None,add_bt=True,**kwargs):
        
        super().__init__(parent,**kwargs)
        self.model=model
        self.label=label
        self.parent=parent
        self.commands=self.parent.commands
        self.add_bt=add_bt
        self.all_selected=False
        
        
        if isinstance(model.fields[self.label]['list'],list):
            self.chckbt_labels=model.fields[self.label]['list']
        else:
            raise Error("Wrong model, chckbt_labels only takes list")
        
        labelframe=tk.Frame(self)
        labelframe.grid(row=0,column=0,sticky='w')
        
        self.MyLabel=ttk.Label(labelframe,text=self.label)
        self.sep=ttk.Separator(self,orient="horizontal")
        self.FrameCheck=tk.Frame(self)

        bt_all=ttk.Button(labelframe,text='tout',width=4,command=self.select_all)
        bt_all.grid(row=0,column=1,sticky='w')

        
        self.MyLabel.grid(row=0,column=0,sticky='w')
        self.sep.grid(row=1,column=0,sticky='we',columnspan=2)
        self.FrameCheck.grid(row=2,column=0,sticky='w')

        self.dict_var={}
        self.dict_chckbt={}
        if self.add_bt:
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

        if self.add_bt:
            self.button_add.grid_forget()
            self.button_add.grid(row=0,
                            column=len(self.chckbt_labels)+1,
                            ipady=1, ipadx=0
                            )

    class WidgetAdd(tk.Frame):
        def __init__(self,parent,outer_instance):
            super().__init__(parent)
            """create an attribut to store the outer instance, so we can acces it later"""
            self.outer_instance=outer_instance
            self.parent=parent
            self.MyVar=tk.StringVar()
            lab=tk.Label(self,text="Enter new element :")
            lab.grid(row=0,column=0,sticky='we')
            self.MyEntry=ttk.Entry(self,textvariable=self.MyVar)
            self.MyEntry.grid(row=1,column=0,sticky='we')
            self.MyEntry.focus_set()
            self.MyButton=ttk.Button(self,text='Save',command=self.save_new)
            self.MyButton.grid(row=2,column=0,sticky='e')
            self.columnconfigure(0,weight=1)
            
            self.MyEntry.bind('<Return>',self.save_new)
            
        def get(self):
            value=self.MyVar.get()
            if value.islower():
                return value.capitalize()
            else:
                return value

        def save_new(self,*args,**kwargs):

            new=self.get()
            self.outer_instance.model.fields[self.outer_instance.label]['list'].append(new)

            self.outer_instance.generate_chckbt()
            self.outer_instance.parent.commands['quit_w'](self.outer_instance.top,save=True)
            self.outer_instance.update()
            self.outer_instance.model.save_lists()
            messagebox.showinfo(
                title="Information",
                message="Nouvel élément ajouté.",
                parent=self.outer_instance)


    def select_all(self):
        if self.all_selected:
            value=0
            self.all_selected=False
        else:
            value=1
            self.all_selected=True

        for chck in self.dict_var.values():
            chck.set(value)

                
            
        
            
    def grid(self,row=None,column=None,sticky='WE',**kwargs):
        super().grid(row=row,column=column,sticky=sticky,**kwargs)

        self.columnconfigure(0,weight=1)

    def get(self):
        """return a dict of only the items where value is 1"""
        
        data={}
        for name,var in self.dict_var.items():
            if var.get():
                data[name]=var.get()
        return data

    def set(self,dict_value):
        #todo : add a len checker. checker that all fields are there
        """dict value must be a dict """
        """when loaded from csv, data is all string. we convert it into a dict if needed"""
        #todo : get rid of the conversion into dict because we already convert it all into a dict when we load all records
        data=dict_value
        if type(dict_value)!=dict:
            data=eval(dict_value)
        
        for name,value in data.items():
            self.dict_var[name].set(value)

    def add_new(self):
        self.top=tk.Toplevel(self,name='top2')
        
        self.top.title("New element")
        self.top.geometry("250x80")
        self.wa=self.WidgetAdd(self.top,self)
        self.wa.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
        self.top.grab_set()
        self.top.columnconfigure(0,weight=1)

        self.top.protocol('WM_DELETE_WINDOW', lambda : self.parent.commands['quit_w'](self.top))
        
##VIEW##
class ViewAll(ttk.Treeview):
    def __init__(self,parent,model,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.model=model
        self.headers=self.model.fields.keys()
        #show="headings" make it so #0 column doesnt show
        self.configure(columns=[*self.headers],show="headings")
                       
        for header in self.headers:
            self.heading(header,text=header)
            self.column(header, minwidth=self.model.fields[header]['width'], width=self.model.fields[header]['width'],stretch=True)

        ybar=ttk.Scrollbar(parent,orient="vertical",command=self.yview)
        ybar.grid(row=0,column=1,sticky='nse')
        xbar=ttk.Scrollbar(parent,orient="horizontal",command=self.xview)
        self.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        xbar.grid(row=1,column=0,sticky='swe')

            
    def grid(self,*args,row=None,column=None,sticky='nswe',**kwargs):
        super().grid(*args,row=row,column=column,sticky=sticky,**kwargs)

    def formating(self,row_data):
        row_values=[]
        for header in self.headers:
            #todo : what if ml is empty
            #todo : get rid of the conversion into dict because we already convert it all into a dict when we load all records

            if header in ("Les gens concernés", "Sociétés/Personnel"):
                ml=[]
                if type(row_data[header])!=dict:
                    mydict=eval(row_data[header])
                else:
                    mydict=row_data[header]
                for key,value in mydict.items():
                    if value==1:
                        ml.append(key)
                ml=", ".join(ml)
                row_values.append(ml)
            else:
                row_values.append(row_data[header])
        for index in range(0,len(row_values)):
            if row_values[index]=='None':
                row_values[index]=''
        """it returns a list"""
        return row_values

    def populate(self,data,statu=False):
        """delete rows in treeview"""
        children=self.get_children()
        if len(children) > 0 :
            for child in children:
                self.delete(child)
                
        counter=0
        """formating data from dict to str for treeview"""
        for row_data in data:
            row_values=self.formating(row_data)

            if statu!='Tout':
                if statu == "Suivi":
                    statu_s=["En cours","Trop tard"]
                else:
                    statu_s=[statu]
                if row_data['Status'] in statu_s:
                    self.insert('', 'end', iid=counter, values=row_values)
                    counter += 1
            else:
                self.insert('', 'end', iid=counter, values=row_values)
                counter += 1

    def print_(self):
        print('ViewAll Called')    

class MyView(tk.Frame):
    def __init__(self,parent,data,mode,commands):
        super().__init__(parent)
        self.mode=mode
        self.data=data
        self.parent=parent
        self.commands=commands
        """we put our Fields's widget in a dict"""
        self.Fields={}
        for num,field in enumerate(self.data.fields.keys()):
            if self.data.fields[field][self.mode]['visible']:
                if self.data.fields[field]['type'] in ['Entry','DateEntry','Text','ComboboxEntry']:
                    self.Fields[field]=LabelEntry(self,
                                                  field,self.data)
                elif self.data.fields[field]['type']=='Checkbox':
                    self.Fields[field]=LabelCheckbutton(self,field,
                                                        self.data,chckbt_labels=self.data.fields[field]['list']
                                                        )
                self.Fields[field].grid(row=num,column=0,sticky='we',pady=2,columnspan=2)

        self.update_idletasks()

        self.columnconfigure(0,weight=1)

        self.button_save=ttk.Button(self,text='Save',command=self.commands['save_entry'])
        self.button_save.grid(row=10,column=0,sticky='e')

        self.button_edit=ttk.Button(self,text='Edit',command=self.commands['mode_edit'])
        self.button_edit.grid(row=10,column=1,sticky='e')


        self.Fields['Note'].MyEntry.focus_set()

        self.Fields['Alarme'].var.trace('w', lambda a,b,c : self.trace_alarme(a,b,c))
        
    def get(self):
        data={}
        for field,widget in self.Fields.items():
            data[field]=widget.get()
        return data

    def set(self,data):
        """data must be a dict"""
        for field,value in data.items():
            self.Fields[field].set(value)

    def reset(self):
        for field,widget in self.Fields.items():
            if field in ('Ref','Date','Alarme','Status'):
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
            if field in ("Note","Status"):
                widget.MyEntry.configure(state=state,background=color)
            elif field=="Ref":
                widget.MyEntry.configure(state="disabled",background=color)

            elif field in ("Date","Alarme"):
                widget.MyEntry.entry.configure(state=state,background=color)
            else :
                for chckbt in widget.dict_chckbt.values():
                    chckbt.configure(state=state)
                widget.button_add.configure(state=state)

        self.update_idletasks()

        if self.mode=="consultation":
            self.button_save.configure(state="disabled")
            self.button_edit.configure(state="normal")

        else :
            self.button_edit.configure(state="disabled")
            self.button_save.configure(state="normal")

    def trace_alarme(self,a,b,c):
        var=self.Fields['Alarme'].var.get()
        
        if self.mode=='modification':
            value=None
            if var in ('',None,'None'):
                value='Note'
            elif testdate(var):
                value='En cours'
            else:
                value='Note'
                print('rien')
            self.Fields['Status'].set(value)
        else:
            pass


class ComplexFilter(tk.Frame):
    def __init__(self,parent,model,*args,commands=None,**kwargs):
        #todo : to finish
        super().__init__(parent,*args,**kwargs)
        self.model=model
        labels=[]
        self.commands=commands
        
        #todo : combine those two succesive block
        for header in self.model.fields:
            if self.model.fields[header].get('list',None) != None:
                labels.append(header)
        print(labels)

        self.widgets={}
        counter=0
        for label in labels:
            self.model.fields[label]['list']
            add_bt = False
            self.widgets[label] = LabelCheckbutton(self,label,self.model,self.commands,add_bt=add_bt)
            self.widgets[label].grid(row=counter,column=0,columnspan=2,pady=10)
            counter+=1

        self.widgets["date01"]=LabelEntry(self,"Date début",self.model,**kwargs)
        self.widgets["date01"].grid(row=counter+1,column=0,sticky='we')
        self.widgets["date02"]=LabelEntry(self,"Date fin",self.model,**kwargs)
        self.widgets["date02"].grid(row=counter+1,column=1,sticky='we')

##        sep=ttk.Separator(self,orient="horizontal")
##        sep.grid(row=counter+2,column=0,sticky='we',columnspan=2, padx=0, pady=(10,0))

        
        self.button_ok = ttk.Button(self,text="Apply",
                                    command = self.commands['apply_complex_filter'])
        self.button_ok.grid(row=counter+2,column=1,sticky='e', pady=(0,0))
        
        pass

    def get(self):
        data={}
        for key,widget in self.widgets.items():
            value=widget.get()
            data[key]=value
        #todo : formatting data. None = all. add "Tout" to Status"
        print(data)
        return data

        

##CONTROLER##
class MyApplication(tk.Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.mode="consultation"
        self.statu='Suivi'
        self.mdt=MyData()
        self.selected=None
        self.commands={'save_entry' : self.save_entry,
                       'load_records' : self.load_records,
                       'new_log' : self.new_log,
                       'mode_edit': self.mode_edit,
                       'quit_w': self.quit_w,
                       'apply_complex_filter': self._show_complex_filter
                       }
        self.records=self.mdt.load_records()
        fb=tk.Frame(self,relief='solid')
        fb.grid(row=0,column=0,sticky='we',padx=5,pady=5)
        fb.columnconfigure(0,weight=0)
        fb.columnconfigure(1,weight=0)
        fb.columnconfigure(2,weight=0)
        fb.columnconfigure(3,weight=0)
        fb.columnconfigure(4,weight=1)
        
        self.button_new = ttk.Button(fb,text="New log",
                                     command = lambda : self.commands['new_log']("creation"))
        self.combo_var_all_filter = tk.StringVar()
        self.combobox_all_filter = MyCombobox(fb,
                                textvariable=self.combo_var_all_filter,
                                values = [*self.mdt.fields['Status']['list'],'Tout',"Suivi"],
                                **kwargs)
        self.combobox_all_filter.set("Suivi")
        self.combo_var_all_filter.trace('w',self.combobox_filter_tree)

        self.filter_var=tk.StringVar()
        self.filter = ttk.Entry(fb,textvariable=self.filter_var)
        self.filter_var.trace('w',self.filter_tree)
        self.complex_filter = ttk.Button(fb, text="More Filter",
                                         command = self.complex_filter)
        self.button_delete = ttk.Button(fb, text="Delete", state="disabled",
                                         command = self.del_log)

        #todo : catch error if argument is neither creation or consultation
        self.button_new.grid(row=0,column=0,sticky='w',padx=5,pady=5)
        self.button_delete.grid(row=0,column=1,sticky='w',padx=5,pady=5)
        self.combobox_all_filter.grid(row=0,column=2,sticky='w',padx=5,pady=5)
        self.complex_filter.grid(row=0,column=3,sticky='w',padx=5,pady=5)
        self.filter.grid(row=0,column=4,sticky='we',padx=5,pady=5)

        self.geometry("910x200")
        self.minsize(width=500, height=200)
        self.title('Historique')
        #self.maxsize(width=1500, height=500)
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

        self.viewall.populate(self.records,statu='Suivi')
        
        self.update_idletasks()

        self.viewall.bind('<1>', self.onclick_viewall)

        self.viewall.bind('<Double-1>', self.doubleclick_viewall)
        
        self.focus_set()

    def onclick_viewall(self,e):
        widget_focused=self.focus_get()
        widget_focused.print_()

        item = widget_focused.identify_row(e.y)
        if item in widget_focused.selection():
            widget_focused.selection_remove(item)
            self.selected=None
            self.button_delete.configure(state="disabled")
            """if your binding returns the string 'break', it will stop event propagation and thus prevent the default
            behaviour for double clicking. You wont be able to use the event '<<TreeviewOpen>>', so you will have to 
            use the event '<Double-1 instead>'"""
            return "break"
        else:
            self.selected=item
            self.button_delete.configure(state="normal")


    def complex_filter(self,*args):
        top5 = tk.Toplevel(name='top5')
        top5.title('Filtre')
        top5.columnconfigure(0,weight=1)

        self.complex_wid = ComplexFilter(top5,self.mdt,commands=self.commands)
        self.complex_wid.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)

    def _filtering_data(self,filter_data,exclusif=True):
        if not isinstance(filter_data,dict):
            print('filter_data must be a dict')
            return
        fd=filter_data.copy()
        fd['Date']=[]
        
        
        for _ in filter_data:
            if "date" in _.lower():
                fd['Date'].append(filter_data[_])
                fd.pop(_)
        keeper=[]
        if exclusif:
            
            for record in self.records :
                keep=[]
                for key,value in filter_data.items():
                    
                    if isinstance(value,dict):
                        if len(value.keys())==0:
                            keep.append(True)
                        elif key!="Status":
                            keep.append(record[key]==value)
                        else:
                            x=[]
                            for _ in value:
                                x.append(_ in record[key])
                            keep.append(any(x))
                    elif isinstance(value,list):
                        if value[0]=='' and value[1]=='':
                            keep.append(True)
                        else:    
                            if value[0]=='':
                                try:
                                    date_1=dt.datetime.strptime(value[1],"%d/%m/%Y")
                                except:
                                    print('error for date_1')
                                else:
                                    keep.append(dt.datetime.strptime(record[key],"%d/%m/%Y")<=date_1)

                            elif value[1]=='':
                                try:
                                    date_0=dt.datetime.strptime(value[1],"%d/%m/%Y")
                                except:
                                    print('error for date_0')
                                else:
                                    keep.append(dt.datetime.strptime(record[key],"%d/%m/%Y")>=date_0)

                            else:
                                try:
                                    date_0=dt.datetime.strptime(value[0],"%d/%m/%Y")
                                    date_1=dt.datetime.strptime(value[1],"%d/%m/%Y")
                                except:
                                    print('error for date_1 or date_0')
                                else:
                                    keep.append(date_0<=dt.datetime.strptime(record[key],"%d/%m/%Y")<=date_1)
                keeper.append(all(keep))
        data=itertools.compress(self.records,keeper)
        #it is an iterator, so we can only use it once.carefull
        return data
            
    def combobox_filter_tree(self,*args):
        
        statu=self.combo_var_all_filter.get()
        if statu in (*self.mdt.list_status,'Tout','Suivi'):
            self.statu=statu
            self.viewall.populate(self.records,statu=self.statu)


    def filter_tree(self,*args):
        #fixme : optimize maybe

        init_iids=self.viewall.get_children()
        for iid in init_iids:
            self.viewall.delete(iid)

        self.viewall.populate(self.records,statu=self.combo_var_all_filter.get())
        characters = self.filter.get().lower()
        if characters=='':
            return
        else:
            myiids=list(self.viewall.get_children())
            for myiid in myiids:
                values=self.viewall.set(myiid)
                headers=self.mdt.fields.keys()
                test=[]
                for header in headers:
                    test.append(characters not in values[header].lower())
                if all(test):
                        self.viewall.delete(myiid)

    def save_entry(self):
            #to do : to refactor, make it cleaner
            if self.mode=="creation":
                record=self.mv.get()
                values = [record[header] for header in self.mdt.fields.keys() if self.mdt.fields[header][self.mode]['visible']]

                for field,value in record.items():
                    if value in ['','\n']:
                        record[field]='None'

                #check if there is empty field in the modified record
                empty_req_fields={}
                for key,value in record.items():
                    empty_req_fields[key]=False
                    if self.mdt.fields[key]['req']:
                        if type(value)==dict:
                            if 1 not in value.values():
                                empty_req_fields[key]=True
                        elif self.mdt.fields[key]['type']=='DateEntry':
                            try:
                                dt.datetime.strptime(value,"%d/%m/%Y")
                            except:
                                empty_req_fields[key]=True
                        else:
                            if value in [None, '', '\n','None']:
                                empty_req_fields[key]=True
                if any(empty_req_fields.values()):
                    messagebox.showerror(title='Erreur',
                                        message='Ces champs ne peuvent être vides ou leurs données sont non-valides :',
                                        detail='{}'.format(', '.join([key for key,value in empty_req_fields.items() if value])),
                                        parent=self.mv
                                        )
                    return

                self.mdt.save_entry(record,self.mode)

                self.mv.reset()
                self.top1.destroy()
                    
                values=self.viewall.formating(record)

                #we update viewall now with an updates log by assigning update_tree the right function
                #that will be called later

                if self.statu=='Tout' or self.statu==record['Status']:
                    update_tree="""self.viewall.insert('', 'end', iid=len(self.viewall.get_children())+1, values=values)"""
                else:
                    pass
                
            elif self.mode=="modification":
                record=self.mv.get()
                values = [record[header] for header in self.mdt.fields.keys() if self.mdt.fields[header][self.mode]['visible']]

                #check if there is empty field in the modified record
                empty_req_fields={}
                for key,value in record.items():
                    empty_req_fields[key]=False
                    if self.mdt.fields[key]['req']:
                        if type(value)==dict:
                            if 1 not in value.values():
                                empty_req_fields[key]=True
                        else:
                            if value in [None, '', '\n','None']:
                                empty_req_fields[key]=True
                if any(empty_req_fields.values()):
                    messagebox.showerror(title='Error',
                                        message='Ces champs ne peuvent être vides:',
                                        detail='{}'.format(', '.join([key for key,value in empty_req_fields.items() if value])),
                                        parent=self.mv
                                        )
                    return

                ref=record['Ref']
                for num,log in enumerate(self.records):
                    if log['Ref']==ref:
                        self.records[num]=record
                
                self.mdt.save_entry(self.records,self.mode)
                
                self.mv.reset()
                self.top1.destroy()

                values=self.viewall.formating(record)

                #we update viewall now with an updates log by assigning update_tree the right function
                #that will be called later
                
                if self.statu=='Tout' or self.statu==record['Status']:
                    update_tree='''self.viewall.item(self.selected, text='', values=values)'''
                else :
                    update_tree='''self.viewall.delete(self.selected)'''
                    
            else:
                self.mdt.save_entry(self.records,self.mode)
                
            self.records=self.mdt.load_records()

            try:
                eval(update_tree)
            except:
                pass

            if self.mode in ('modification','creation'):   
                messagebox.showinfo(
                        title="Information",
                        message="Sauvegarde réussie.")
            else:
                messagebox.showinfo(
                        title="Information",
                        message="Ligne(s) effacée(s) avec succès.")

    def del_log(self):
        selections=self.viewall.selection()
        refs=[]
        for row in selections :
            values=self.viewall.set(row)
            refs.append(values['Ref'])
        if refs[-1]=='':
            refs.pop[-1]
        txt=', '.join(refs)

        if len(selections)>1:
            deleting=messagebox.askyesno(title="Suppression",
                             message="Etes-vous sûr de vouloir supprimer ces lignes?",
                            detail=f"{txt}",
                            parent=self)
        else:
            deleting=messagebox.askyesno(title="Suppression",
                                     message="Etes-vous sûr de vouloir supprimer cette ligne?",
                                    detail=f"{txt}",
                                    parent=self)

        if deleting :
            for selection in selections:
                values = self.viewall.set(selection)
                ref=values["Ref"]
                for row,record in enumerate(self.records):
                    if record['Ref']==ref:
                        self.records.pop(row)
                        break
            
                self.viewall.delete(selection)

            self.mode="delete"
            self.save_entry()
                
    def load_records(self):
        pass
    
    def new_log(self,mode):
        self.top1=tk.Toplevel(self,name='top1')
        self.mode=mode
        self.mv=MyView(self.top1,self.mdt,self.mode,self.commands)

        self.top1.protocol('WM_DELETE_WINDOW', lambda : self.quit_w(self.nametowidget('top1')))

        #another more specific way to put the cursor where we want in tk.Text
        #self.mv.Fields['Note'].MyEntry.mark_set("insert","1,0")

        self.mv.change_state("normal")

        if mode=="consultation":
            self.top1.title("Consulting log")

        else :
            self.top1.title("Creating log")

            """auto fill date with today's date"""
            td=dt.date.today()
            self.mv.Fields['Date'].set(td.strftime("%d/%m/%Y"))

            """auto fill ref"""
            if len(self.records)==0 :
                newref = "ref0001"
            else :
                lastref = self.records[-1]['Ref']
                refnum=lastref.split('ref')[1]
                newnum=int(refnum)+1
                newref='ref'+str('{:04d}'.format(newnum))
            self.mv.Fields['Ref'].set(newref)

        self.mv.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
        
        self.top1.grab_set()
        self.columnconfigure(0,weight=1)

        
    def doubleclick_viewall(self,*args):
        self.mode="consultation"
        self.new_log("consultation")
        
        widget_focused=self.focus_get()
        widget_focused.print_()
        
        current = widget_focused.focus()
        self.selected=current
        values = widget_focused.set(current)
        ref=values["Ref"]
        data=self.mdt.load_records()
        for row,values in enumerate(data):
            if values['Ref']==ref:
                row_index=row
                self.mv.reset()
                self.mv.set(data[row_index])
                self.mv.change_state('disabled')
                break
        print(self.mv.Fields['Alarme'].var.get())


    def mode_edit(self):
        self.mode="modification"
        self.mv.mode="modification"
        
        self.mv.change_state("normal")
        self.update()
        self.mv.update()

    def _show_complex_filter(self):
        #todo : change it so it populate the current reeview in main window, and add "selection"in listbox
        filter_data=self.complex_wid.get()
        self.top4=tk.Toplevel(self,name='top4')
        self.top4.title('Résultat')
        tv=ViewAll(self.top4,self.mdt)
        tv.grid(row=0,column=0)
        mydata=self._filtering_data(filter_data,exclusif=True)
        top=self.nametowidget('.top5')
        top.destroy()
        tv.populate(mydata,statu='Tout')
        
        tv.bind('<1>', self.onclick_viewall)

        tv.bind('<Double-1>', self.doubleclick_viewall)

        
    def quit_w(self,w,save=False):
        #todo : w.destroy only once in this code
        if self.mode in ("modification","creation"):
            ##########
            top1=self.nametowidget('.top1')
            if w==top1:
                data=self.mv.get()
                tests=[]
                #detecting if any field is not empty when creation or modifiation mode
                if self.mode=="creation":
                    for key,value in data.items():
                        #todo : if date is diffenrete from today
                        #todo : if alarm is different from empty
                        if key == 'Note':
                            tests.append(data[key]!='')
                        elif key == 'Les gens concernés':
                            tests.append(len(data[key])>0)
                        elif key == 'Sociétés/Personnel':
                            tests.append(len(data[key])>0)
                        elif key == "Alarme":
                            tests.append(data[key]!='')
                        else:
                            tests.append(False)
                        
                elif self.mode=="modification":
                    for record in self.records:
                        if record['Ref']==data['Ref']:
                            for key,value in data.items():
                                tests.append(data[key]!=record[key])

                if not save:
                    if any(tests):
                        fields=self.mdt.fields.keys()
                        dd=dict(zip(fields,tests))
                        x=[field for field,value in dd.items() if value==True]
                        quitting=messagebox.askyesno(title="Quitting",
                                                         message="Des champs ont été modifié : {}.".format(', '.join(x)),
                                                         detail="Etes-vous sûr de vouloir abandonner l'enregistrement en cours?",
                                                         parent=w)
                        if not quitting:
                            return
                        else:
                            pass
                        
                self.grab_set()
            try :
                """widgetadd for checkbuttons first line"""
                top2=self.nametowidget('.top1.!myview.!labelcheckbutton.top2')
                if w==top2:
                    new_element=self.nametowidget('.top1.!myview.!labelcheckbutton.top2.!widgetadd').get()
                    if not save:
                        if new_element!='':
                            quitting=messagebox.askyesno(title="Quitting",
                                                         message="Le champ n'est pas vide.",
                                                         detail="Etes-vous sûr de vouloir abandonner l'enregistrement en cours?",
                                                         parent=w)
                            if not quitting:
                                return
                            else:
                                pass
                    top1.grab_set()
            except:
                print('top2 missing')

            try:
                """widgetadd for checkbuttons second line"""
                top2a=self.nametowidget('.top1.!myview.!labelcheckbutton2.top2')
                if w==top2a:
                    new_element=self.nametowidget('.top1.!myview.!labelcheckbutton2.top2.!widgetadd').get()
                    if not save:
                        if new_element!='':
                            quitting=messagebox.askyesno(title="Quitting",
                                                         message="Le champ n'est pas vide.",
                                                         detail="Etes-vous sûr de vouloir abandonner l'enregistrement en cours?",
                                                         parent=w)
                            if not quitting:
                                return
                            else:
                                pass
                                                
                            print('You entered a new element. Are you sure you wanna leave?')
                    top1.grab_set()
            except:
                print('top2a missing')
                
            try :
                """calendar"""
                top3=self.nametowidget('.top1.!myview.!labelentry2.!mydateentry.top3')
                if w==top3:
                    top1.grab_set()
            except:
                print('top3 missing')
            finally:
                w.destroy()

        else:
            w.destroy()    


if __name__=='__main__':
    app=MyApplication()
    #style=ttk.Style()
    app.mainloop()
