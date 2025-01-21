from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Modern Login/Signup')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

######################
img = PhotoImage(file='pagetrunc.png')  
Label(root, image=img, bg='white').place(x=10, y=10)
##################

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=500, y=70)
##################################
# Heading
heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23))
heading.place(x=100, y=5)

########################
user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11,))
user.place(x=30, y=80)
user.insert(0, 'Username')
#################################
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

################################
password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11,), show="*")
password.place(x=30, y=150)
password.insert(0, 'Password')
################################
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)


def on_login():
    print("Login button clicked")

Button(frame, width=30, pady=5, text='Login', bg='#00b4d8', fg='blue', border=0, command=on_login).place(x=27, y=190)


def on_signup():
    print("Sign-up button clicked")

label_signup = Label(frame, text="Don't have an account?", fg="black", bg="white", font=('Microsoft YaHei UI Light', 9))
label_signup.place(x=75, y=270)

sign_up_button = Button(frame, text="Sign up", border=0, bg="white", cursor="hand2", fg='#57a1f8', font=('Microsoft YaHei UI Light', 9), command=on_signup)
sign_up_button.place(x=210, y=270)

root.mainloop()
