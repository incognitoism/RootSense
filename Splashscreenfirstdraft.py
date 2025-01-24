import tkinter as tk
from tkinter import messagebox
import psycopg2
import random
from math import cos, sin, radians

class SensorGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Grid Visualization")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")

        # Database connection
        self.conn = psycopg2.connect(
            dbname="RootsenseODManager",
            user="postgres",
            password="greymee",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()

        # Canvas
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="#2e2e2e", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.nodes = []
        self.radius = 400
        self.center_x = 400
        self.center_y = 500
        self.nodes_per_cross_section = 5  # Number of dots per cross-section
        self.cross_section_width = 5
        self.node_count = self.calculate_node_count()

        # Controls frame
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

        self.logout_button = tk.Button(
            controls_frame, text="Logout", command=self.logout, bg="#ff5e57", fg="white",
            font=("Arial", 12), relief="flat", width=10
        )
        self.logout_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def calculate_node_count(self):
        return self.cross_section_width * self.nodes_per_cross_section

    def draw_node(self, node):
        color = node["status"]
        x, y = node["x"], node["y"]
        r = 5
        node["circle"] = self.canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=color, outline=""
        )

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
        if len(self.nodes) >= self.node_count:
            messagebox.showinfo("Info", "Maximum number of nodes reached!")
            return

        angle_step = 180 / (self.cross_section_width - 1)
        cross_section_index = len(self.nodes) // self.cross_section_width
        node_index = len(self.nodes) % self.cross_section_width

        angle = angle_step * node_index
        x = self.center_x + self.radius * cos(radians(angle))
        y = self.center_y - (self.radius * sin(radians(angle)) / self.nodes_per_cross_section * (cross_section_index + 1))
        
        node = {
            "x": x,
            "y": y,
            "status": "red",
            "circle": None,
        }
        self.nodes.append(node)
        self.draw_node(node)

    def logout(self):
        self.root.destroy()
        DashboardApp()

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
        self.user.insert(0, 'Username')
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
