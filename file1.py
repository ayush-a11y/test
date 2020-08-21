import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
import csv


root = Tk()
root.title("Student Information System")
root.geometry("1350x900")
root.config(bg="gainsboro")
root.state("zoomed")

#                                   Create Variables

'''
we create variables so that we can fetch the data
which enters in entry boxes and store it into database

'''

sRoll = StringVar()
sName = StringVar()
sGender = IntVar()
sPhone = StringVar()
sAddress = StringVar()
sCourse = StringVar()



#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------   


#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

#                           BACK-END  & FUNCTIONS CREATION

#---------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


# Database Creation -->
#-------------------
db = sqlite3.connect("DB.sqlite")
try:
        db.execute("create table student(Roll Integer primary key,Name Text,Gender Text,Phone Text,Address Text,Course Text)")
except:
        pass


#                           Functions Creation
#--------------------------------------------------------------------------------------------

# Function to save Data -->

list2=['Roll No','Name','Gender','Phone','Address','Course']
def save_data():
    list1=[]
    # Validation for Blank Entry Box
    if (len(sRoll.get())!=0):
            # Validation for Inger value only
            if (sRoll.get()).isdigit():
                    Roll = int(sRoll.get())
                    list1.append(Roll)
            else:
                    messagebox.showwarning('Warning','Roll Number must be a Digit')
                    return
                             
    else:
            messagebox.showwarning('Warning','Please Enter Your Roll Number')
            return
        
    # Validation for blank name entry box
    if (len(sName.get())!=0):
            Name = sName.get()
            Name1 = Name.replace(" ","")
            
            # Validation to enter only alphabets
            if Name1.isalpha():
                    #Name = sName.get()
                    list1.append(Name)
            else:
                    messagebox.showwarning('Warning','Name must contain alphabets only')
                    return
                    
    else:   
        messagebox.showwarning('Warning','Please Enter Your Name :')
        return

    # Validation to select at least one option
    if (sGender.get()>=1):
            Gender = int(sGender.get())
            if Gender == 1:
                    list1.append("Male")
            elif Gender == 2:
                    list1.append("Female")
    else:   
        messagebox.showwarning('Warning','Please Select Your Gender :')
        return

    # Validation for blank Entry Box
    if (len(sPhone.get())!=0):
            # Validation for integer value only
            if (sPhone.get()).isdigit():
                    Phone = sPhone.get()
                    # Validation for 10 digit phone num only
                    if len(Phone)==10:
                            list1.append(Phone)
                    else:
                            messagebox.showwarning('Warning',
                                                   'Phone Number must contain 10 digits :')
                            return  
                            
            else:
                  messagebox.showwarning('Warning','Phone Number must contain only digits :')
                  return  
    else:   
        messagebox.showwarning('Warning','Please Enter Your Phone Number :')
        return
    if (len(sAddress.get())!=0):
            Address = sAddress.get()
            list1.append(Address)
    else:   
        messagebox.showwarning('Warning','Please Enter Your Address :')
        return
    if (len(sCourse.get())!=0):
            Course = sCourse.get()
            list1.append(Course)
    else:   
        messagebox.showwarning('Warning','Please Select Your Course :')
        return
    cursor = db.cursor()
    cursor.execute("select *from student")
    var = cursor.fetchall()
    count =0
    for i in range(len(var)):
            if Roll == var[i][0]:
                    count=count+1
            else:
                    count=count
    if count==0:
            db.execute("Insert into student values(?,?,?,?,?,?)",list1)
    else:
            messagebox.showwarning('Warning','Roll Number already exists')
            return
    db.commit()
    cursor = db.cursor()
    cursor.execute("select *from student")
    var = cursor.fetchall()
    f = open("student.csv","w",newline="")
    obj = csv.writer(f)
    obj.writerow(list2)
    for i in var:
        obj.writerow(i)
    messagebox.showinfo('Information','Your Data Saved Successfully')
    print("===Data stored===")
    #txtrollNo.delete(0,END)
    #txtName.delete(0,END)
    #txtPhone.delete(0,END)
    #combo.delete(0,END)
    #txtAddress.delete(0,END)


    
#----------------------------------------------------------------------------------------------    

# Function to clear the text boxes

def clear_data():
        
    txtrollNo.delete(0,END)
    optGender1.deselect()
    optGender2.deselect()
    txtName.delete(0,END)
    txtPhone.delete(0,END)
    combo.delete(0,END)
    txtAddress.delete(0,END)
            
#----------------------------------------------------------------------------------------------        
    
# Function to switch to another window to delete data

def delete_window():
        root1 = Tk()
        root1.title("Delete Data")
        root1.geometry("800x300")
        root1.config(bg="skyblue")

        Roll_Label = Label(root1, text="Enter Roll No to Delete Data: ", font=('arial',15,'bold'),
                           bg="skyblue", anchor=N)
        Roll_Label.grid(row=1,column=1, sticky=W)

        delete_window.txtroll = Entry(root1,font =('arial',15,'bold'),width=28)
        delete_window.txtroll.grid(row=1,column=2,sticky=W)

        Label(root1,text=" ",bg="skyblue",width=12).grid(row=0,column=0)
        Label(root1,text=" ",bg="skyblue").grid(row=2,column=2)

        Del_Button=Button(root1,text ="Delete",width=10,height=1,
                      bd=4,font=('arial',12,'bold'),bg ="lightgrey",command=del_data)
        Del_Button.grid(row=3,column=2)



        root1.mainloop()

#----------------------------------------------------------------------------------------------


    
# Function to delete data

def del_data():

        cursor = db.cursor()
        cursor.execute("select * from student")
        var = cursor.fetchall()

        count = 0

        if(len(delete_window.txtroll.get()))!=0:
                if(delete_window.txtroll.get()).isdigit():
                        Roll = int(delete_window.txtroll.get())
                        for i in range(len(var)):
                                if Roll == var[i][0]:
                                        count = count + 1
                                else:
                                        count = count
                        if count == 1:
                                cursor.execute("DELETE FROM student WHERE Roll=?",[Roll])
                                db.commit()
                        else:
                                messagebox.showwarning("Warning","Roll number does not exists")
                                return
                else:
                        messagebox.showwarning("Warning","Roll Number must be in digit")
        else:
                messagebox.showwarning("Warning","Please enter the Roll No")

        cursor = db.cursor()
        cursor.execute("select * from student")
        var = cursor.fetchall()

        f = open("student.csv","w",newline="")
        obj = csv.writer(f)
        obj.writerow(list2)
        for i in var:
                obj.writerow(i)
        messagebox.showinfo('Information',' Roll No {} is Deleted'.format(Roll))
        delete_window.txtroll.delete(0,END)
        print("------Deleted-------")
        f.close()

#----------------------------------------------------------------------------------------------
# Function to close the system

def exit_data():
        close = messagebox.askyesno("Student Database","Do you want to close the window!")
        if close>0:
                root.destroy()
                return
                                

#----------------------------------------------------------------------------------------------



# Funtion to open update window

def update_data():
        update_data.root3 = Tk()
        update_data.root3.title("Update Data")
        update_data.root3.geometry("650x200")
        update_data.root3.config(bg="skyblue")
        update_data.root3.state("zoomed")

        update_data.sRoll = StringVar()
        update_data.uGender = IntVar()

        lb1 = Label(update_data.root3, text="Enter Roll Number to Update data: ", bg="skyblue",
                    font=('arial',15,'bold'), padx=2, pady=1, fg="black")
        lb1.grid(row=1, column=1)

        update_data.e1 = Entry(update_data.root3, font=('arial',12,'bold'), width=28, fg="black")
        update_data.e1.grid(row=1, column=2, sticky=W)

        # Button to fetch data
        b1 = Button(update_data.root3, text="Fetch", font=('arial',12,'bold'), bd=4,
                    bg="light grey", height=1, width=10,command=Fetch)
        b1.grid(row=2, column=1)

        # Labels for spaces to arrange widgets properly
        Label(update_data.root3,text="",bg="skyblue",width=15,height=5).grid(row=0,column=0)
        Label(update_data.root3,text="",bg="skyblue",width=15,height=5).grid(row=3,column=0)
        Label(update_data.root3,text='',bg='skyblue',width=15,height=5).grid(row=10,column=0)

        #For Roll No
        labelrollNo = Label(update_data.root3,font =('arial',15,'bold'),
                            text = "Enter Roll Number :  ",padx=2,pady=1,bg='skyblue'
                            ,fg='black',width=30,anchor=E)
        labelrollNo.grid(row=4,column=1)
        update_data.uRoll = Entry(update_data.root3,font =('arial',18,'bold'),width=28
                                  ,textvariable=update_data.sRoll)
        update_data.uRoll.grid(row=4,column=2,sticky=W)
        
        #For Name
        labelName = Label(update_data.root3,font =('arial',15,'bold'),
                            text = "Enter Your Name :  ",padx=2,pady=1,bg='skyblue'
                          ,fg='black',width=30,anchor=E)
        labelName.grid(row=5,column=1)
        update_data.txtName = Entry(update_data.root3,font =('arial',18,'bold'),width=28)
        update_data.txtName.grid(row=5,column=2,sticky=W)

        #For Gender
    
        labelGender = Label(update_data.root3,font =('arial',15,'bold'),
                            text = "Select Your Gender :  ",padx=2,pady=1,bg='skyblue'
                            ,fg='black',width=30,anchor=E)
        labelGender.grid(row=6,column=1)

        update_data.optGender1 = Radiobutton(update_data.root3,text='Male',value=1,
                                variable=update_data.uGender,bg='skyblue',font =('arial',12,'bold'))
        update_data.optGender1.grid(row=6,column=2,sticky=W)
    
    

        update_data.optGender2 = Radiobutton(update_data.root3,text='Female',value=2,
                                variable=update_data.uGender,bg='skyblue',font =('arial',12,'bold'))
        update_data.optGender2.grid(row=6,column=3,sticky=S)
    
    
        # For Phone Number
        labelPhone = Label(update_data.root3,font =('arial',15,'bold'),
                            text = "Phone Number :  ",padx=2,pady=1,bg='skyblue'
                           ,fg='black',width=30,anchor=E)
        labelPhone.grid(row=7,column=1)
        update_data.txtPhone = Entry(update_data.root3,font =('arial',18,'bold'),width=28)
        update_data.txtPhone.grid(row=7,column=2,sticky=W)

        # For Address
        labelAddress = Label(update_data.root3,font =('arial',15,'bold'),
                            text = "Address :  ",padx=2,pady=1,bg='skyblue'
                             ,fg='black',width=30,anchor=E)
        labelAddress.grid(row=8,column=1)
        update_data.txtAddress = Entry(update_data.root3,font =('arial',18,'bold'),width=28)
        update_data.txtAddress.grid(row=8,column=2,sticky=W)

        # For Course
        labelCourse = Label(update_data.root3,font =('arial',15,'bold'),
                            text = "Course :  ",padx=2,pady=1,bg='skyblue'
                            ,fg='black',width=30,anchor=E)
        labelCourse.grid(row=9,column=1)
        update_data.v =['BCA','MCA','B.Tech','M.Tech','B.Sc','M.Sc','B.Ed','B.Com','M.Com']
        update_data.combo = Combobox(update_data.root3,values=update_data.v,
                                     textvariable=sCourse,width=57)
        update_data.combo.grid(row=9,column=2,sticky=W)


        # Button to Update Data
        B2= Button(update_data.root3,text='Update',bd=4,
                   font =('arial',12,'bold'),bg='lightgrey',
                   height=1,width='10',command = Update)
        B2.grid(row=11,column=2)
        

        
        update_data.root3.mainloop()

#-----------------------------------------------------------------------------------------------

#Function to fetch data in Update Data window

def Fetch():

        # Validation for blank entry box
        if(len(update_data.e1.get()))!=0:
                
                # validation for integer value in entry box
                if update_data.e1.get().isdigit():

                        # Validation to know whether roll exists in db or not
                        cursor = db.cursor()
                        cursor.execute("select * from student")
                        var = cursor.fetchall()
                        count=0

                        roll = int(update_data.e1.get())

                        for i in range(len(var)):
                                if roll == var[i][0]:
                                        count = count + 1
                                else:
                                        count=count
                        if count == 1:
                            cursor = db.cursor()
                            cursor.execute("select * from student where Roll=?",[roll])
                            var = cursor.fetchall()    
                            update_data.uRoll.insert(END,var[0][0])
                            update_data.txtName.insert(END,var[0][1])
                            update_data.txtPhone.insert(END,var[0][3])
                            update_data.txtAddress.insert(END,var[0][4])
                            update_data.combo.insert(END,var[0][5])

                            if var[0][2]=="Male":
                                    update_data.optGender1.select()

                            elif var[0][2]=="Female":
                                    update_data.optGender1.select()

                        else:
                                messagebox.showwarning('Warning','Roll Number does not exists')
                                return
                else:
                        messagebox.showwarning('Warning','Roll Number must be a digit')
                        return
        else:
                messagebox.showwarning('Warning','Please Enter Roll Number')
                return

#----------------------------------------------------------------------------------------------

# Function to Update Data

def Update():
        roll = int(update_data.e1.get())
        Gender = update_data.uGender.get()

        if Gender == 1:
                G="Male"
        elif Gender == 2:
                G="Female"

        cursor = db.cursor()

        Rollno = update_data.uRoll.get()
        Name = update_data.txtName.get()
        Phone = update_data.txtPhone.get()
        Address = update_data.txtAddress.get()
        Course = update_data.combo.get()

        cursor.execute("update student set Roll=? where Roll=?",(Rollno,roll))
        cursor.execute("update student set Name =? where Roll=?",(Name,roll))
        #cursor.execute("update student set Gender = ? where Roll=?",(G,roll))
        cursor.execute("update student set Phone = ? where Roll=?",(Phone,roll))
        cursor.execute("update student set Address = ? where Roll=?",(Address,roll))
        cursor.execute("update student set Course = ? where Roll=?",(Course,roll))
        messagebox.showinfo("Information","Information update")
        print("UPDATED")

        db.commit()

        cursor = db.cursor()
        cursor.execute("select *from student")
        var = cursor.fetchall()
        f = open("student.csv","w",newline="")
        obj = csv.writer(f)
        obj.writerow(list2)
        for i in var:
                obj.writerow(i)
        update_data.e1.delete(0,END)
        update_data.uRoll.delete(0,END)
        update_data.txtName.delete(0,END)
        update_data.txtPhone.delete(0,END)
        update_data.combo.delete(0,END)
        update_data.txtAddress.delete(0,END)    

#----------------------------------------------------------------------------------------------

# display all data

def display_data():
        display_data.root4 = Tk()
        display_data.root4.title("Display Reults")
        display_data.root4.geometry("700x700")
        display_data.root4.config(bg="skyblue")
        display_data.root4.state("zoomed")

        appLabel = Label(display_data.root4, text="Student Management System",
                        fg="black", width=40,bg="skyblue")
        appLabel.config(font=("Sylfaen", 30))
        appLabel.pack()

        tree = ttk.Treeview(display_data.root4)
        tree["columns"] = ("zero","one","two","three","four","five")

        tree.heading("zero", text="RollNo")
        tree.heading("one", text="Name")
        tree.heading("two", text="Gender")
        tree.heading("three", text="Phone Number")
        tree.heading("four", text="Address")
        tree.heading("five", text="Course")
        

        cursor = db.cursor()
        cursor.execute("select * from student")
        var = cursor.fetchall()

        i=0

        for row in var:
                tree.insert("",i,text="Student " +str(row[0]),
                            values =(row[0],row[1],row[2],row[3],
                                     row[4],row[5]))
                i=i+1
        tree.pack()
        
        
        db.commit()

        
        display_data.root4.mainloop()

                        
#----------------------------------------------------------------------------------------------


# Function to open search window

def search_data():
        root2=Tk()
        root2.title("Search data")
        root2.config(bg='skyblue')
        root2.geometry('1325x690')
        root2.state('zoomed')
        srRoll = Label(root2,font =('arial',15,'bold'),
                    text = "Enter Roll Number to Search Data :  ",padx=2,pady=1,bg='skyblue'
                  ,fg='black',width=30,anchor=E)
        srRoll.grid(row=1,column=1)
        search_data.txtsrRoll = Entry(root2,font =('arial',18,'bold'),width=28)
        search_data.txtsrRoll.grid(row=1,column=2,sticky=W)
        # Add Scroll Bar and List Box
        scroll = Scrollbar(root2)
        Label(root2,text=" ",bg='skyblue',height=4).grid(row=2,column=2)
        Label(root2,text=" ",bg='skyblue',height=5).grid(row=0,column=2)
        Bsearch =  Button(root2,text='Search',bd=4,
                   font =('arial',12,'bold'),bg='lightgrey',
                   height=1,width='10',command = Search)
        Bsearch.grid(row=3,column=1)
        scroll = Scrollbar(root2)
        scroll.grid(row=4,column=4,sticky='ns')
        search_data.studentInfoList=Listbox(root2,width=60,height=24,
                               font=('arial',12,'bold'),yscrollcommand=scroll.set)
        search_data.studentInfoList.grid(row=4,column=3,padx=8)
        scroll.config(command=search_data.studentInfoList.yview)
        root2.mainloop()

#----------------------------------------------------------------------------------------------


# Function to search data

def Search():
        list1=[]
        list2=['Roll No','Name','Gender','Phone','Address','Course']
        count=0
        if (len(search_data.txtsrRoll.get()))!=0:
                roll=int(search_data.txtsrRoll.get())
                if (search_data.txtsrRoll.get()).isdigit():
                        cursor = db.cursor()
                        cursor.execute("select *from student where Roll=?",[roll])
                        var = cursor.fetchall()
                        for i in range(len(var)):
                                if roll== var[i][0]:
                                        count=count+1
                                else:
                                        count=count
                        print(count)
                        if count!=0: 
                                for i in range (len(var[0])):
                                        list1.append(var[0][i])

                                for it in range (len(list1)):
                                        search_data.studentInfoList.insert(END," \n"+str(list2[it])+" : "+str(list1[it]),str(""))
                                search_data.txtsrRoll.delete(0,END)
                        else:
                                messagebox.showwarning('Warning','Roll Number Does not exists')
                                
                else:
                        messagebox.showwarning('Warning','Roll Number must be a digit')
                        return
                        
        else:
                messagebox.showwarning('Warning','Please Enter Roll Number')
                return
       
#----------------------------------------------------------------------------------------------    
                        

#----------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

#                               FRONT END CREATION

#---------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


#                                All Frames Creation

MainFrame = Frame(root,bg='gainsboro')
MainFrame.grid()


# 1) HeadFrame Creation -->
HeadFrame = Frame(MainFrame,padx=10,pady=10
                  ,bg="gainsboro",relief=RIDGE)
HeadFrame.pack(side=TOP)


# 2) operation Frame Creation -->(All the buttons are inside this operation frame)

OperationFrame = Frame(MainFrame,bd=1,width=1300,height=60,padx=10,pady=20
                  ,bg="gainsboro",relief=RIDGE)
OperationFrame.pack(side=BOTTOM)


# 3) Body Frame Creation-->(All the labels ,text boxes are inside this body frame)

BodyFrame = Frame(MainFrame,bd=2,width=1290,height=400,padx=50,pady=20
                  ,bg="gainsboro",relief=RIDGE)
BodyFrame.pack(side=BOTTOM)


        # 3.1 a ) Inside Body frame creation -->

'''               These two are made inside the body frame
                  so that left body frame can have all the text boxes and labels
'''
 
LeftBodyFrame = LabelFrame(BodyFrame,text="Add Student Details",bd=2,width=600
                           ,height=380,padx=20,pady=50,bg="skyblue",
                           relief=RIDGE,font=('arial',15,'bold'))
LeftBodyFrame.pack(side=LEFT)


#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


#                                Title Creation inside Head Frame


Ititle=Label(HeadFrame,text="Student Information System ",bg="gainsboro"
         ,fg="steel blue",width=31,font=('arial',50,'bold'))
Ititle.grid()

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------





#                         Add the widgets to the Left Body Frame



#For Roll No 
labelrollNo = Label(LeftBodyFrame,font =('arial',15,'bold'),
                    text = "Enter Roll Number :  ",padx=2,pady=1,bg='skyblue'
                    ,fg='black',width=30,anchor=E)
labelrollNo.grid(row=1,column=1)
txtrollNo = Entry(LeftBodyFrame,font =('arial',18,'bold'),
                  textvariable = sRoll,width=28)
txtrollNo.grid(row=1,column=2,sticky=W)

#For Name 
labelName = Label(LeftBodyFrame,font =('arial',15,'bold'),
                    text = "Enter Your Name :  ",padx=2,pady=1,bg='skyblue'
                  ,fg='black',width=30,anchor=E)
labelName.grid(row=3,column=1)
txtName = Entry(LeftBodyFrame,font =('arial',18,'bold'),
                  textvariable = sName,width=28)
txtName.grid(row=3,column=2,sticky=W)


#For Gender 
labelGender = Label(LeftBodyFrame,font =('arial',15,'bold'),
                    text = "Select Your Gender :  ",padx=2,pady=1,bg='skyblue'
                    ,fg='black',width=30,anchor=E)
labelGender.grid(row=5,column=1)
i = IntVar()
optGender1 = Radiobutton(LeftBodyFrame,text='Male',value=1,
                         variable=sGender,bg='skyblue',font =('arial',12,'bold'))
optGender1.grid(row=5,column=2,sticky=W)
optGender2 = Radiobutton(LeftBodyFrame,text='Female',value=2,
                         variable=sGender,bg='skyblue',font =('arial',12,'bold'))
optGender2.grid(row=5,column=2,sticky=S)


# For Phone Number
labelPhone = Label(LeftBodyFrame,font =('arial',15,'bold'),
                    text = "Phone Number :  ",padx=2,pady=1,bg='skyblue'
                   ,fg='black',width=30,anchor=E)
labelPhone.grid(row=7,column=1)
txtPhone = Entry(LeftBodyFrame,font =('arial',18,'bold'),
                  textvariable = sPhone,width=28)
txtPhone.grid(row=7,column=2,sticky=W)


# For Address
labelAddress = Label(LeftBodyFrame,font =('arial',15,'bold'),
                    text = "Address :  ",padx=2,pady=1,bg='skyblue'
                     ,fg='black',width=30,anchor=E)
labelAddress.grid(row=9,column=1)
txtAddress = Entry(LeftBodyFrame,font =('arial',18,'bold'),
                  textvariable = sAddress,width=28)
txtAddress.grid(row=9,column=2,sticky=W)

# For Course
labelCourse = Label(LeftBodyFrame,font =('arial',15,'bold'),
                    text = "Course :  ",padx=2,pady=1,bg='skyblue'
                    ,fg='black',width=30,anchor=E)
labelCourse.grid(row=11,column=1)
v =['BCA','MCA','B.Tech','M.Tech','B.Sc','M.Sc','B.Ed','B.Com','M.Com']
combo = Combobox(LeftBodyFrame,values=v,textvariable=sCourse,width=57)
combo.grid(row=11,column=2,sticky=W)



# For spaces
Label(LeftBodyFrame,text =" ",bg='skyblue',width=21).grid(row=2,column=0,sticky=W)
Label(LeftBodyFrame,text =" ",bg='skyblue').grid(row=4,column=3,sticky=W)
Label(LeftBodyFrame,text =" ",bg='skyblue').grid(row=6,column=4,sticky=W)
Label(LeftBodyFrame,text =" ",bg='skyblue').grid(row=8,column=5,sticky=W)
Label(LeftBodyFrame,text =" ",bg='skyblue').grid(row=10,column=6,sticky=W)
Label(LeftBodyFrame,text =" ",bg='skyblue').grid(row=12,column=7,sticky=W)
Label(LeftBodyFrame,text =" ",bg='skyblue',width=41).grid(row=14,column=8,sticky=W)




#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------








#                       Add Buttons in operation Frame

# Save Button -->
save_btn =  Button(OperationFrame,text='Save',bd=4,
                   font =('arial',12,'bold'),bg='lightgrey',
                   height=1,width='10',command = save_data)
save_btn.grid(row=0,column=1)

# Clear Button
clr_btn =  Button(OperationFrame,text='Clear',bd=4,
                   font =('arial',12,'bold'),bg='lightgrey',
                   height=1,width='10',command = clear_data)
clr_btn.grid(row=0,column=3)

# Update Button
updt_btn = Button(OperationFrame,text='Update',bd=4,
                   font =('arial',12,'bold'),bg='lightgrey',
                   height=1,width='10',command = update_data)
updt_btn.grid(row=0,column=5)


# Delete Button
dlt_btn = Button(OperationFrame,text='Delete',bd=4,
                   font =('arial',12,'bold'),bg='lightgrey',
                   height=1,width='10',command = delete_window)
dlt_btn.grid(row=0,column=7)


# Search Button
search_btn = Button(OperationFrame,text = 'Search',bd=4,font=('arial',12,'bold'),bg='lightgrey'
                    ,height=1,width='10',command=search_data)
search_btn.grid(row=0,column=9)

# Display Button
display_btn = Button(OperationFrame,text='Display',bd=4,
                   font =('arial',12,'bold'),bg='lightgrey',
                   height=1,width='10',command = display_data)
display_btn.grid(row=0,column=11)



# Exit Button
exit_btn = Button(OperationFrame,text='Exit',bd=4,
                   font =('arial',12,'bold'),bg='lightgrey',
                   height=1,width='10',command = exit_data)
exit_btn.grid(row=0,column=13)


# For spaces
Label(OperationFrame,text =" ",bg='white',width=10).grid(row=0,column=0,sticky=W)
Label(OperationFrame,text =" ",bg='white',width=8).grid(row=0,column=2,sticky=W)
Label(OperationFrame,text =" ",bg='white',width=8).grid(row=0,column=4,sticky=W)
Label(OperationFrame,text =" ",bg='white',width=8).grid(row=0,column=6,sticky=W)
Label(OperationFrame,text =" ",bg='white',width=8).grid(row=0,column=8,sticky=W)
Label(OperationFrame,text =" ",bg='white',width=8).grid(row=0,column=10,sticky=W)
Label(OperationFrame,text=" ",bg='white',width=8).grid(row=0,column=12,sticky=W)
Label(OperationFrame,text =" ",bg='white',width=10).grid(row=0,column=14,sticky=W)

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


root.mainloop()
