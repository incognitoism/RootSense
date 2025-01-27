import tkinter as tk
from tkinter import messagebox
import psycopg2
import random

class SensorGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Grid Visualization")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")

        self.conn = psycopg2.connect(
            dbname="RootsenseODManager",
            user="postgres",
            password="greymee",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="#2e2e2e", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.nodes = []
        self.node_count = 0 

        controls_frame = tk.Frame(self.root, bg="#1e1e1e")
        controls_frame.pack(fill=tk.X, pady=10)

        self.add_button = tk.Button(
            controls_frame, text="Add New Node", command=self.add_node, bg="#007acc", fg="white",
            font=("Arial", 12), relief="flat", width=15
        )
        self.add_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.refresh_button = tk.Button(
            controls_frame, text="Refresh Nodes", command=self.refresh_nodes, bg="#007acc", fg="white",
            font=("Arial", 12), relief="flat", width=15
        )
        self.refresh_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.auto_node_button = tk.Button(
            controls_frame, text="Auto Node Call", command=self.auto_node_call, bg="#007acc", fg="white",
            font=("Arial", 12), relief="flat", width=15
        )
        self.auto_node_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.scan_button = tk.Button(
            controls_frame, text="Scan Nodes", command=self.scan_nodes, bg="#007acc", fg="white",
            font=("Arial", 12), relief="flat", width=15
        )
        self.scan_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.logout_button = tk.Button(
            controls_frame, text="Logout", command=self.logout, bg="#ff5e57", fg="white",
            font=("Arial", 12), relief="flat", width=10
        )
        self.logout_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.node_count_label = tk.Label(
            controls_frame, text=f"Nodes: {self.node_count}", bg="#1e1e1e", fg="white", font=("Arial", 12)
        )
        self.node_count_label.pack(side=tk.LEFT, padx=10, pady=5)

    def draw_node(self, node, label):
        color = node["status"]
        x, y = node["x"], node["y"]
        r = node["radius"]
        node["circle"] = self.canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=color, outline=""
        )
        self.canvas.create_text(x, y, text=label, fill="white", font=("Arial", 8))

    def update_node(self, node, status):
        node["status"] = status
        color = "red" if status == "red" else "yellow" if status == "yellow" else "green"
        self.canvas.itemconfig(node["circle"], fill=color)

    def refresh_nodes(self):
        if not self.nodes:
            messagebox.showinfo("Info", "No nodes to refresh. Add nodes first.")
            return

        for node in self.nodes:
            status = random.choice(["red", "yellow", "green"])
            self.update_node(node, status)

    def add_node(self):
        rows, cols = 10, 10
        canvas_width = 800
        canvas_height = 600

        if len(self.nodes) >= rows * cols:
            messagebox.showinfo("Info", "Maximum number of nodes reached!")
            return

        spacing = 5
        cell_width = (canvas_width - (cols - 1) * spacing) / cols
        cell_height = (canvas_height - (rows - 1) * spacing) / rows
        radius = min(cell_width, cell_height) / 2

        node_index = len(self.nodes)
        row_index = node_index // cols
        col_index = node_index % cols

        x = col_index * (cell_width + spacing) + cell_width / 2
        y = row_index * (cell_height + spacing) + cell_height / 2

        label = f"{chr(97 + row_index)}{col_index + 1}"

        node = {
            "x": x,
            "y": y,
            "status": "red",
            "radius": radius,
            "circle": None,
        }
        self.nodes.append(node)
        self.draw_node(node, label)
        self.node_count += 1
        self.node_count_label.config(text=f"Nodes: {self.node_count}")

    def auto_node_call(self):
        self.auto_node_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.auto_node_frame.place(x=300, y=300)

        call_max_button = tk.Button(
            self.auto_node_frame, text="Call Max", command=self.call_max, bg="#007acc", fg="white",
            font=("Arial", 12), relief="flat", width=15
        )
        call_max_button.pack(side=tk.TOP, pady=5)

        call_custom_button = tk.Button(
            self.auto_node_frame, text="Call Custom", command=self.call_custom, bg="#007acc", fg="white",
            font=("Arial", 12), relief="flat", width=15
        )
        call_custom_button.pack(side=tk.TOP, pady=5)

    def call_max(self):
        self.node_count = 100  
        self.auto_node_frame.destroy()  
        self.call_nodes(self.node_count) 
        
        
   """ def scan_nodes(self): #please check this _________ i am unable to get this to work 
        def scan_node(index=0):
            if index >= len(self.nodes):
                return
                node = self.nodes[index]
                self.canvas.itemconfig(node["circle"], fill="green")
                self.canvas.after(200, lambda: self.update_node(node, "red"))
                self.canvas.after(300, lambda: scan_node(index + 1))
                scan_node() """

    def call_custom(self):
        def submit_custom_count():
            try:
                count = int(entry.get())
                if count <= 0 or count > 100:
                    raise ValueError("Invalid number")
                self.auto_node_frame.destroy()  
                self.node_count = count 
                self.call_nodes(self.node_count)
                custom_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number between 1 and 100.")

        custom_window = tk.Toplevel(self.root)
        custom_window.title("Custom Node Count")
        custom_window.geometry("300x150")
        custom_window.configure(bg="#1e1e1e")

        label = tk.Label(custom_window, text="Enter number of nodes:", bg="#1e1e1e", fg="white", font=("Arial", 12))
        label.pack(pady=10)

        entry = tk.Entry(custom_window, font=("Arial", 12))
        entry.pack(pady=10)

        submit_button = tk.Button(
            custom_window, text="Submit", command=submit_custom_count, bg="#007acc", fg="white",
            font=("Arial", 12), relief="flat", width=10
        )
        submit_button.pack(pady=10)

    def call_nodes(self, count):
        existing_node_count = len(self.nodes)
        for i in range(existing_node_count, count):
            self.add_node()
            self.node_count_label.config(text=f"Nodes: {len(self.nodes)}")

       

    def logout(self):
        self.root.destroy()
        LoginApp()

class DashboardApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rootsense Manager Dashboard")
        self.root.geometry("925x500")
        self.root.configure(bg="white")

        self.dashboard_frame = tk.Frame(self.root, bg="white", width=925, height=500)
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.dashboard_frame, text="Welcome to Rootsense", font=("Arial", 24, "bold"), bg="white", fg="black").place(x=20, y=20)
        tk.Label(self.dashboard_frame, text="v 0.0.001 rel", font=("Arial", 18), bg="white", fg="black").place(x=20, y=60)
        tk.Label(self.dashboard_frame, text="RELEASE VERSION IS 0.0.001, THIS IS A WORK IN PROGRESS", font=("Arial", 12), bg="white", fg="black").place(x=20, y=100)

        tk.Button(self.dashboard_frame, text="SCREEN TESTS", font=("Arial", 14), bg="black", fg="white", width=20, height=2, border=0).place(x=600, y=50)
        tk.Button(self.dashboard_frame, text="SENSOR OPT", font=("Arial", 14), bg="gray", fg="white", width=20, height=2, border=0).place(x=600, y=140)
        tk.Button(self.dashboard_frame, text="COMMS OPT", font=("Arial", 14), bg="gray", fg="white", width=20, height=2, border=0).place(x=600, y=230)
        tk.Button(self.dashboard_frame, text="NEW MESH SETUP", font=("Arial", 14), bg="navy", fg="white", width=20, height=2, border=0, command=self.open_sensor_grid).place(x=600, y=320)

        tk.Button(self.dashboard_frame, text="Logout", font=("Arial", 12), bg="#00b4d8", fg="white", command=self.logout).place(x=20, y=450)

        self.root.mainloop()

    def open_sensor_grid(self):
        self.root.destroy()
        root = tk.Tk()
        SensorGridApp(root)
        root.mainloop()

    def logout(self):
        self.root.destroy()
        LoginApp()

class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("925x500")
        self.root.configure(bg="white")

        img = tk.PhotoImage(file='pagetrunc.png', width=300, height=200)
        tk.Label(self.root, image=img, bg='white').place(x=10, y=10)
        self.root.img = img

        frame = tk.Frame(self.root, width=350, height=350, bg="white")
        frame.place(x=500, y=70)

        heading = tk.Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23))
        heading.place(x=100, y=5)

        self.user = tk.Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        self.user.place(x=30, y=80)
        tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.password = tk.Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), show="*")
        self.password.place(x=30, y=150)
        self.password.insert(0, 'Password')
        tk.Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

        tk.Button(frame, width=30, pady=5, text='Login', bg='#00b4d8', fg='blue', border=0, command=self.login).place(x=27, y=190)

        label_signup = tk.Label(frame, text="Don't have an account?", fg="black", bg="white", font=('Microsoft YaHei UI Light', 9))
        label_signup.place(x=75, y=270)

        sign_up_button = tk.Button(frame, text="Sign up", border=0, bg="white", cursor="hand2", fg='#57a1f8', font=('Microsoft YaHei UI Light', 9), command=self.on_signup)
        sign_up_button.place(x=210, y=270)

        self.root.mainloop()

    def login(self):
        username = self.user.get()
        password = self.password.get()

        conn = psycopg2.connect(
            dbname="RootsenseODManager",
            user="postgres",
            password="greymee",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Successful", "Welcome to the Sensor Grid App!")
            self.root.destroy()
            DashboardApp()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
        conn.close()

    def on_signup(self):
        username = self.user.get()
        password = self.password.get()

        if username == '' or password == '':
            messagebox.showerror('Error', 'All fields are required!')
            return

        try:
            conn = psycopg2.connect(
                dbname="RootsenseODManager",
                user="postgres",
                password="greymee",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            messagebox.showinfo('Success', 'Account created successfully!')
            conn.close()
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            messagebox.showerror('Error', 'Username already exists.')

if __name__ == "__main__":
    LoginApp()
