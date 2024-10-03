import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog,simpledialog
from PIL import Image, ImageTk
import re
from datetime import datetime


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return None if self.isEmpty() else self.items.pop()

    def isEmpty(self):
        return self.items == []

    def top(self):
        return None if self.isEmpty() else self.items[-1]

    def count(self):
        return None if self.isEmpty() else len(self.items)


pages_stack = Stack()

def back():
    if pages_stack.isEmpty() == False:  # there is a previous page
        previous_page = pages_stack.pop()
        previous_page()  # call

class User:
    def __init__(self, username, email, password,bio):
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.friends = []
        self.friend_requests = []
        self.posts = []
        self.messages_to_you = []
        self.messages_from_you = []
        self.notifications = []
        self.saved_posts = []


    def get_dict(self):
        dict_obj = {
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "Bio": self.bio,
                "friends": [],
                "friend_requests": [],
                "posts": [],
                "messages_to_you": [],
                "messages_from_you": [],
                "notifications": [],
                "saved_posts": []
            }
        return dict_obj

# inheritance  & polymorphism : inheritance , override
class Post:
    def __init__(self, author, post_id):
        self.author = author
        self.post_id = post_id
        self.likes = 0
        self.comments = []
        self.liked_by = []

    def to_dict(self):
        return {
            "author": self.author,
            "post_id": self.post_id,
            "likes": self.likes,
            "liked_by": self.liked_by,
            "comments": self.comments
        }
class TextPost(Post):
    def __init__(self, author, post_id, content):
        super().__init__(author, post_id)
        self.type = "text"
        self.content = content

    def to_dict(self):
        post_dict = super().to_dict()
        post_dict["type"] = self.type
        post_dict["content"] = self.content
        return post_dict
class ImagePost(Post):
    def __init__(self, author, post_id, image_path):
        super().__init__(author, post_id)
        self.type = "image"
        self.image_path = image_path

    def to_dict(self):
        post_dict = super().to_dict()
        post_dict["type"] = self.type
        post_dict["image_path"] = self.image_path
        return post_dict

class SocialMediaManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.posts_file = 'posts.json'
        self.load_data()

    def load_data(self):
        with open(self.users_file, 'r') as f:
            self.users = json.load(f)

        with open(self.posts_file, 'r') as f:
            self.posts = json.load(f)

    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
        with open(self.posts_file, 'w') as f:
            json.dump(self.posts, f, indent=4)

    def get_user_data(self, username):
        return self.users.get(username)

    def save_user_data(self, username, user_data):
        self.users[username] = user_data
        self.save_data()

    def create_post(self, username, content, post_type):
        self.load_data()
        post_id = len(self.posts) + 1
        if post_type == "text":
            post = TextPost(username, post_id, content)
        elif post_type == "image":
            post = ImagePost(username, post_id, content)

        self.posts[post_id] = post.to_dict()
        self.users[username]['posts'].append(post_id)
        self.save_data()
        return post

    def send_friend_request(self, from_user, to_user):
        self.load_data()
        if to_user in self.users and from_user not in self.users[to_user]['friend_requests']:
            self.users[to_user]['friend_requests'].append(from_user)
            self.save_data()

    def accept_friend_request(self, user, friend):
        self.load_data()
        if friend in self.users[user]['friend_requests']:
            self.users[user]['friends'].append(friend)
            self.users[friend]['friends'].append(user)
            self.users[user]['friend_requests'].remove(friend)
            self.save_data()

    def decline_friend_request(self, user, friend):
        self.load_data()
        if friend in self.users[user]['friend_requests']:
            self.users[user]['friend_requests'].remove(friend)
            self.save_data()

    def view_friend_requests(self, user):
        self.load_data()
        return self.users[user]['friend_requests']

    def send_message(self, from_user, to_user, message):
        self.load_data()
        if to_user in self.users and from_user in self.users:
            timestamp = datetime.now().isoformat()
            self.users[to_user]['messages_to_you'].append({
                'from': from_user,
                'content': message,
                'time': timestamp
            })
            self.users[from_user]['messages_from_you'].append({
                'to': to_user,
                'content': message,
                'time': timestamp
            })

            self.save_data()

    def view_inbox(self, user):
        return self.users[user]['messages_to_you'],self.users[user]['messages_from_you']

    def like_post(self, post_id, user):
        self.load_data()
        if post_id in self.posts and user in self.users:
            self.posts[post_id]['likes'] += 1
            self.save_data()

    def comment_on_post(self, post, comment, user):
        self.load_data()
        new_comment = {
            "user": user,
            "comment": comment,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Save time of comment
        }
        post["comments"].append(new_comment)
        self.save_data()

    def quick_sort(self, list):
        if len(list) <= 1:
            return list
        pivot = list[len(list) // 2]
        left = [x for x in list if x < pivot]
        middle = [x for x in list if x == pivot]
        right = [x for x in list if x > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)

    def binary_search(self, myList, target):
        left, right = 0, len(myList) - 1

        while left <= right:
            mid = (left + right) // 2
            if myList[mid] == target:
                return True
            elif myList[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return False

    def ret_sorted_list(self,lst):
        return self.quick_sort(lst)

    def user_search(self, search_username):
        usernames = self.ret_sorted_list(list(self.users.keys()))
        found = self.binary_search(usernames, search_username)
        if found:
            return self.users[search_username]
        else:
            return None

    def get_user_posts(self, username):
        self.load_data()
        return [post for post in self.posts.values() if post['author'] == username]

    def delete_post(self, post_id, username):
        self.load_data()
        if post_id in self.users[username]['posts']:
            self.users[username]['posts'].remove(post_id)

        if post_id in self.posts:
           del self.posts[post_id]
        self.save_data()

    def save_post_for_user(self, user_name, post):
        self.load_data()
        user_data = self.get_user_data(user_name)
        if 'saved_posts' not in user_data:
            user_data['saved_posts'] = []

        if post not in user_data['saved_posts']:
            user_data['saved_posts'].append(post)
            self.save_user_data(user_name, user_data)

    def get_saved_posts(self, user_name):
        self.load_data()
        user_data = self.get_user_data(user_name)
        return user_data.get('saved_posts', [])


def login():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("700x700")
    login_window.configure(bg="light pink")

    frame = tk.Frame(login_window, bg="#F8BBD0")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    title_label = tk.Label(frame, text="Welcome Back", font=("Arial", 24, "bold"), bg="#F8BBD0", fg="#880E4F")
    title_label.pack(pady=20)

    tk.Label(frame, text="Email", font=("Arial", 14, "bold"), bg="#F8BBD0", fg="#880E4F").pack(pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30, bd=2, relief="groove")
    email_entry.pack(pady=5)

    tk.Label(frame, text="Password", font=("Arial", 14, "bold"), bg="#F8BBD0", fg="#880E4F").pack(pady=5)
    password_entry = tk.Entry(frame, font=("Arial", 12), width=30, bd=2, relief="groove", show="*")
    password_entry.pack(pady=5)

    error_label = tk.Label(frame, text="", fg="red", bg="#F8BBD0", font=("Arial", 12, "italic"))
    error_label.pack(pady=10)

    def validate_login():
        email = email_entry.get()
        password = password_entry.get()
        users = load_users()

        if not email or not password:
            error_label.config(text="Email and Password cannot be empty")
            return

        for username, user_data in users.items():
            if user_data['email'] == email and user_data['password'] == password:
                login_window.destroy()
                home_page(tk.Tk(), SMM, username)
                return

        error_label.config(text="Invalid email or password")

    button_style = {"font": ("Times New Roman", 15, "bold"), "fg": "white", "bg": "#9B59B6"}
    tk.Button(frame, text="Login", **button_style, width=15, bd=0, command=validate_login).pack(pady=10)
    tk.Button(frame, text="Register", **button_style, width=15, bd=0,
              command=lambda: [login_window.destroy(), register()]).pack(pady=5)
    tk.Button(frame, text="Exit", **button_style, width=10, bd=0, command=login_window.destroy).pack(pady=20)
    login_window.mainloop()

def register():
    register_window = tk.Tk()
    register_window.title("Register")
    register_window.geometry("700x700")
    register_window.configure(bg="#F8BBD0")

    frame = tk.Frame(register_window, bg="#F8BBD0")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    title_label = tk.Label(frame, text="Create Account", font=("Arial", 24, "bold"), bg="#F8BBD0", fg="#880E4F")
    title_label.pack(pady=20)

    tk.Label(frame, text="Name", font=("Arial", 14, "bold"), bg="#F8BBD0", fg="#880E4F").pack(pady=5)
    name_entry = tk.Entry(frame, font=("Arial", 12), width=30, bd=2, relief="groove")
    name_entry.pack(pady=5)

    tk.Label(frame, text="Email", font=("Arial", 14, "bold"), bg="#F8BBD0", fg="#880E4F").pack(pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30, bd=2, relief="groove")
    email_entry.pack(pady=5)

    tk.Label(frame, text="Password", font=("Arial", 14, "bold"), bg="#F8BBD0", fg="#880E4F").pack(pady=5)
    password_entry = tk.Entry(frame, font=("Arial", 12), width=30, bd=2, relief="groove", show="*")
    password_entry.pack(pady=5)

    error_label = tk.Label(frame, text="", fg="red", bg="#F8BBD0", font=("Arial", 12, "italic"))
    error_label.pack(pady=10)

    def save_registration():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not (name and email and password):
            error_label.config(text="Please fill all fields")
            return

        if not is_valid_email(email):
            error_label.config(text="Invalid email format")
            return

        users = load_users()

        if any(user['email'] == email for user in users.values()):
            error_label.config(text="Email already exists")
        else:
            users[name] = {
                "username": name,
                "email": email,
                "password": password,
                "Bio": "Hello, I'm " + name,
                "friends": [],
                "friend_requests": [],
                "posts": [],
                "messages_to_you": [],
                "messages_from_you": [],
                "notifications": [],
                "saved_posts": []
            }
            save_users(users)
            messagebox.showinfo("Successfully", "Registration successful")
            register_window.destroy()
            login()

    button_style = {"font": ("Times New Roman", 15, "bold"), "fg": "white", "bg": "#9B59B6"}
    tk.Button(frame, text="Register",**button_style, width=15, bd=0,command=save_registration).pack(pady=10)
    tk.Button(frame, text="Cancel",**button_style, width=15, bd=0,command=lambda: [register_window.destroy(), login()]).pack(pady=10)

    register_window.mainloop()

def clear(window):
    for widget in window.winfo_children():
        widget.destroy()

def home_page(main_window, s_manager, user_name):
    clear(main_window)
    main_window.title("Home Page")
    main_window.geometry("700x700")
    main_window.configure(bg="lavender")

    button_frame = tk.Frame(main_window, bg="lavender")
    button_frame.pack(pady=10, fill="x")

    button_style = {"font": ("Times New Roman", 12, "bold"), "fg": "white", "bg": "#9B59B6"}

    add_post_button = tk.Button(button_frame, text="Add Post", command=lambda: add_post_form(main_window, s_manager, user_name), **button_style)
    add_post_button.pack(side="left", padx=5)

    search_button = tk.Button(button_frame, text="Search", command=lambda: open_search(main_window, s_manager, user_name), **button_style)
    search_button.pack(side="left", padx=5)

    profile_button = tk.Button(button_frame, text="Profile", command=lambda: user_profile_page(main_window, s_manager, user_name), **button_style)
    profile_button.pack(side="left", padx=5)

    messages_button = tk.Button(button_frame, text="Messages", command=lambda: open_messages(main_window, s_manager, user_name), **button_style)
    messages_button.pack(side="left", padx=5)

    requests_button = tk.Button(button_frame, text="Friend Requests", command=lambda: open_friend_requests(main_window, s_manager, user_name), **button_style)
    requests_button.pack(side="left", padx=5)

    notifications_button = tk.Button(button_frame, text="Notifications", command=lambda: open_notifications(main_window, s_manager, user_name), **button_style)
    notifications_button.pack(side="left", padx=5)

    saved_posts_button = tk.Button(button_frame, text="Saved Posts", command=lambda: open_saved_posts(main_window, s_manager, user_name), **button_style)
    saved_posts_button.pack(side="left", padx=5)

    posts_frame = tk.Frame(main_window, bg="purple")
    posts_frame.pack(fill="both", expand=True, pady=20)

    canvas = tk.Canvas(posts_frame, bg="lavender")
    scrollbar = ttk.Scrollbar(posts_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="lavender")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n")  # Center alignment using anchor="n"

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_home_page():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for post_id, post in s_manager.posts.items():
            post_author = post['author']
            post_content = post.get('content', '')

            post_frame = tk.Frame(scrollable_frame, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="lavender")
            post_frame.pack(pady=10, anchor="center")  # Centering the posts in the frame

            author_label = tk.Label(post_frame, text=f"Posted by: {post_author}", font=("Arial", 12, "bold"), bg="lavender")
            author_label.pack(anchor="w")

            if post['type'] == "text":
                content_label = tk.Label(post_frame, text=post_content, font=("Arial", 11), bg="lavender")
                content_label.pack(anchor="w", pady=5)
            elif post['type'] == "image":
                image = Image.open(post['image_path'])
                image = image.resize((400, 300))
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(post_frame, image=photo, bg="lavender")
                image_label.image = photo
                image_label.pack(anchor="w", pady=5)

            like_button = tk.Button(post_frame, text=f"Like ({post['likes']})",
                                    command=lambda p=post: toggle_like(p, user_name, refresh_home_page), **button_style)
            like_button.pack(side="left", padx=10)

            comment_button = tk.Button(post_frame, text="Comments",
                                       command=lambda p=post: open_comments(s_manager, p, user_name), **button_style)
            comment_button.pack(side="left", padx=10)

            save_button = tk.Button(post_frame, text="Save Post",
                                    command=lambda p=post: save_post(s_manager, p, user_name), **button_style)
            save_button.pack(side="left", padx=10)

    refresh_home_page()
    def logout():
        main_window.destroy()
        login()

    logout_button = tk.Button(main_window, text="Logout", command=logout, **button_style)
    logout_button.pack(side="bottom", pady=10)

def add_post_form(main_window,s_manager,user_name):
    clear(main_window)
    pages_stack.push(lambda: home_page(main_window, s_manager, user_name))
    main_window.title("Add Post")
    main_window.geometry("700x700")
    main_window.configure(bg="lavender")

    style = ttk.Style()
    style.configure("Custom.TLabel", background="lavender", foreground="#301934")
    style.configure("Custom.TButton", background="#9B59B6", foreground="purple")

    label = ttk.Label(main_window, text="Add Post Page", font=("Times New Roman", 16, "bold", "italic"), style="Custom.TLabel")
    label.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

    def browse_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            image_entry.delete(0, tk.END)
            image_entry.insert(0, file_path)

    # Type menu
    ttk.Label(main_window, text="Post Type:", style="Custom.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    type_choice = tk.StringVar()
    type_menu = ttk.Combobox(main_window, textvariable=type_choice, values=["text", "image"], state="readonly")
    type_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    type_menu.current(0)

    content_label = ttk.Label(main_window, text="Content:", style="Custom.TLabel")
    content_entry = ttk.Entry(main_window, width=40)
    image_label = ttk.Label(main_window, text="Image Path:", style="Custom.TLabel")
    image_entry = ttk.Entry(main_window, width=30)

    browse_button = ttk.Button(main_window, text="Browse", command=browse_image, style="Custom.TButton")

    # fields based on  type
    def show_specific(*args):
        if type_choice.get() == "text":
            image_label.grid_forget()
            image_entry.grid_forget()
            browse_button.grid_forget()
            content_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            content_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        elif type_choice.get() == "image":
            content_label.grid_forget()
            content_entry.grid_forget()
            image_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            image_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
            browse_button.grid(row=2, column=2, padx=5, pady=5)

    type_choice.trace("w", show_specific)

    def save_post():
        post_type = type_choice.get()
        if post_type == "text":
            content = content_entry.get()
            if not content:
                messagebox.showwarning("Input Error", "Text content cannot be empty!")
                return
            post = s_manager.create_post(user_name, content, "text")

        elif post_type == "image":
            image_path = image_entry.get()
            if not image_path:
                messagebox.showwarning("Input Error", "Please select an image!")
                return
            post = s_manager.create_post(user_name, image_path, "image")

        messagebox.showinfo("Success", "Post added successfully!")
        s_manager.save_data()

    button_frame = tk.Frame(main_window, bg="lavender")
    button_frame.grid(row=3, column=0, columnspan=2, pady=20)

    add_button = ttk.Button(button_frame, text="Add Post", command=save_post, style="Custom.TButton")
    add_button.grid(row=0, column=0, padx=10)
    back_button = ttk.Button(button_frame, text="Back",command=back, style="Custom.TButton")
    back_button.grid(row=0, column=1, padx=10)

def user_profile_page(main_window, s_manager, user_name):
    clear(main_window)
    pages_stack.push(lambda: home_page(main_window, s_manager, user_name))
    main_window.title(f"{user_name}'s Profile")
    main_window.geometry("700x700")
    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    back_button = tk.Button(main_window, text="Back", command=back,**button_style)
    back_button.place(relx=0.0, rely=0.0, anchor="nw")

    user_data = s_manager.users.get(user_name)
    post_data = []
    for p_id, post in s_manager.posts.items():
        if post['author'] == user_name:
            post_data.append((p_id, post))

    def show_post_details(post):
        details_window = tk.Toplevel(main_window)
        details_window.title("Post Details")
        details_window.geometry("500x500")

        details_frame = tk.Frame(details_window, padx=10, pady=10)
        details_frame.pack(expand=True, fill="both")
        details = f"Likes: {post['likes']}\n\nComments:\n"
        if post['comments'] == []:
            details += "No Comments Yet!"
        else:
            for comment in post['comments']:
                details += f"{comment['user']}: {comment['comment']}\n"
        tk.Label(details_frame, text=details, wraplength=280, justify="left", font=("Times New Roman", 15)).pack(
            pady=10)
        close_button = tk.Button(details_frame, text="Close", command=details_window.destroy, **button_style)
        close_button.pack(pady=10)

    def delete_post(post_id):
        s_manager.delete_post(post_id, user_name)
        tk.messagebox.showinfo("Deleted", "Post deleted successfully!")
        # refresh
        user_profile_page(main_window, s_manager, user_name)

    # frame1: username, posts num, friends num
    post_num = len(post_data)
    friends_num = len(user_data['friends'])

    frame1 = tk.Frame(main_window, highlightbackground="purple", highlightthickness=2, highlightcolor="purple")
    frame1.pack(pady=10)
    tk.Label(frame1, text=user_data['username'], font=("Times New Roman", 15, "bold")).grid(row=0, column=0,columnspan=2)
    tk.Label(frame1, text="Posts", font=("Times New Roman", 13)).grid(row=1, column=0)
    tk.Label(frame1, text=f'{post_num}', font=("Times New Roman", 12), fg="purple").grid(row=2, column=0)
    tk.Label(frame1, text="Friends", font=("Times New Roman", 13)).grid(row=1, column=1)
    tk.Label(frame1, text=f'{friends_num}', font=("Times New Roman", 12), fg="purple").grid(row=2, column=1)

    # frame2: bio
    frame2 = tk.Frame(main_window, highlightbackground="purple", highlightthickness=2, highlightcolor="purple")
    frame2.pack(pady=10)

    tk.Label(frame2, text="Bio", font=("Times New Roman", 13)).pack()
    bio_label = tk.Label(frame2, text=user_data.get('Bio', 'No bio'), wraplength=400, justify="left",font=("Times New Roman", 12), fg="purple")
    bio_label.pack()

    def edit_bio():
        new_bio = simpledialog.askstring("Edit Bio", "Enter new bio:")
        if new_bio:
            user_data['Bio'] = new_bio
            messagebox.showinfo("Success", "Bio updated successfully!")
            bio_label.config(text=new_bio)
            s_manager.save_data()
        # refresh
        user_profile_page(main_window, s_manager, user_name)

    edit_bio_button = tk.Button(frame2, text="Edit Bio", command=edit_bio, **button_style)
    edit_bio_button.pack(pady=5)

    # frame3: posts
    frame3 = tk.Frame(main_window, highlightbackground="gray", highlightthickness=2, highlightcolor="purple", bg="white")
    frame3.pack(pady=10, fill="both", expand=True)

    # scrollbar
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Vertical.TScrollbar", background="lavender", troughcolor="lavender", arrowcolor="purple")
    canvas = tk.Canvas(frame3)
    scrollbar = ttk.Scrollbar(frame3, orient=tk.VERTICAL, command=canvas.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)
    post_frame = tk.Frame(canvas)
    canvas.create_window((300, 0), window=post_frame, anchor="n")  # center

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    post_frame.bind("<Configure>", on_frame_configure)

    if post_data == []:
        post_label = tk.Label(post_frame, text="No posts to show!", wraplength=400, justify="left",
                              font=("Times New Roman", 12), fg="gray")
        post_label.pack(pady=5, anchor=tk.CENTER)
    else:
        for post_id, post in post_data:
            post_container = tk.Frame(post_frame, highlightbackground="gray", highlightthickness=1, bg="#F5F5DC")
            post_container.pack(pady=10, anchor=tk.CENTER, fill="x")
            if post['type'] == 'text':
                post_label = tk.Label(post_container, text=post['content'], wraplength=400, justify="left",bg="#F5F5DC")
            elif post['type'] == 'image':
                image = Image.open(post['image_path'])
                image = image.resize((250, 250))  # Resize
                photo = ImageTk.PhotoImage(image)
                post_label = tk.Label(post_container, image=photo, bg="#F5F5DC")
                post_label.image = photo  # reference

            post_label.pack(pady=5, anchor=tk.CENTER)

            details_button = tk.Button(post_container, text="Details", command=lambda p=post: show_post_details(p),**button_style)
            details_button.pack(anchor=tk.CENTER)
            delete_button = tk.Button(post_container, text="Delete", command=lambda p_id=post_id: delete_post(p_id),**button_style)
            delete_button.pack(anchor=tk.CENTER)

def toggle_like(post, user_name, refresh_function):
    if 'liked_by' not in post:
        post['liked_by'] = []

    # Check if liked  post
    if any(like['user'] == user_name for like in post['liked_by']):
        post['liked_by'] = [like for like in post['liked_by'] if like['user'] != user_name]
        post['likes'] -= 1
    else:
        post['liked_by'].append({
            'user': user_name,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        post['likes'] += 1

    SMM.save_data()
    refresh_function()

def open_profile_view(main_window, s_manager, username, posts):
    new_window = tk.Toplevel()
    new_window.title(f"{username}'s Profile")
    new_window.geometry("500x500")
    tk.Label(new_window, text=f"{username}'s Profile", font=("Times New Roman", 16, "bold", "italic"), fg="#301934", bg="lavender").pack(pady=20)

    # Scrollbar
    canvas = tk.Canvas(new_window)
    scrollbar = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    tk.Label(scrollable_frame, text=f"{username}'s Posts:", font=("Times New Roman", 12, "bold"),bg="lavender").pack(anchor="w", pady=(10, 0))

    if posts:
        for post in posts:
            post_frame = tk.Frame(scrollable_frame, bd=1, relief="solid", padx=10, pady=5, bg="#F5F5DC")
            post_frame.pack(fill=tk.X, pady=5)

            if post['type'] == "text":
                tk.Label(post_frame, text=f"Text Post: {post['content']}", wraplength=300, justify="left", bg="#F5F5DC").pack(anchor="w")
            elif post['type'] == "image":
                tk.Label(post_frame, text="Image Post:", bg="#F5F5DC").pack(anchor="w")
                try:
                    image_path = post['image_path']
                    image = Image.open(image_path)
                    image = image.resize((200, 200), Image.Resampling.LANCZOS)
                    img = ImageTk.PhotoImage(image)
                    img_label = tk.Label(post_frame, image=img, bg="#F5F5DC")
                    img_label.image = img  # reference
                    img_label.pack(anchor="w")
                except Exception as e:
                    tk.Label(post_frame, text=f"Error loading image: {e}", fg="red", bg="#F5F5DC").pack(anchor="w")
    else:
        tk.Label(scrollable_frame, text="No posts available.", fg="gray", bg="#F5F5DC").pack()

def open_search(new_window, s_manager, user_name):
    clear(new_window)
    pages_stack.push(lambda: home_page(new_window, s_manager, user_name))
    new_window.title("Search for User")
    new_window.geometry("700x700")
    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    tk.Label(new_window, text="Enter username:", font=("Times New Roman", 16, "bold", "italic"),fg="#301934", bg="lavender").pack(pady=20)

    search_frame = tk.Frame(new_window)
    search_frame.pack(pady=5)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)
    back_button = tk.Button(new_window, text="Back", command=back, **button_style)
    back_button.place(relx=0.0, rely=0.0, anchor="nw")

    canvas = tk.Canvas(new_window)
    scrollbar = tk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    result_frame = tk.Frame(scrollable_frame)
    result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    def search_user():
        for widget in result_frame.winfo_children():
            widget.destroy()

        username = search_entry.get()
        user_data = s_manager.user_search(username)

        if user_data:
            post_data = s_manager.get_user_posts(username)
            display_user_bar(username, post_data)
        else:
            tk.Label(result_frame, text="User not found.", fg="red").pack()

    def display_user_bar(username, posts):
        bar_frame = tk.Frame(result_frame, bd=2, relief="groove", padx=10, pady=5)
        bar_frame.pack(fill=tk.X, pady=5)

        user_label = tk.Label(bar_frame, text=username, font=("Times New Roman", 12, "bold"))
        user_label.pack(side=tk.LEFT)

        follow_button = tk.Button(bar_frame, text="Send Friend Request",command=lambda: send_friend_request(username, follow_button), **button_style)
        follow_button.pack(side=tk.RIGHT, padx=5)
        view_profile_button = tk.Button(bar_frame, text="View Profile",command=lambda: open_profile_view(new_window, s_manager, username, posts), **button_style)
        view_profile_button.pack(side=tk.RIGHT, padx=5)
        posts_frame = tk.Frame(result_frame, bd=2, relief="groove", padx=10, pady=5)
        posts_frame.pack(fill=tk.X, pady=10)
        tk.Label(posts_frame, text=f"{username}'s Posts:", font=("Times New Roman", 12, "bold")).pack(anchor="w")

        if posts:
            for post in posts:
                post_frame = tk.Frame(posts_frame, bd=1, relief="solid", padx=10, pady=5, bg="#F5F5DC")
                post_frame.pack(fill=tk.X, pady=5)

                if post['type'] == "text":
                    tk.Label(post_frame, text=f"Text Post: {post['content']}", wraplength=300, justify="left", bg="#F5F5DC").pack(anchor="w")
                elif post['type'] == "image":
                    tk.Label(post_frame, text="Image Post:", bg="#F5F5DC").pack(anchor="w")
                    try:
                        image_path = post['image_path']
                        image = Image.open(image_path)
                        image = image.resize((200, 200), Image.Resampling.LANCZOS)
                        img = ImageTk.PhotoImage(image)
                        img_label = tk.Label(post_frame, image=img, bg="#F5F5DC")
                        img_label.image = img  # reference
                        img_label.pack(anchor="w")
                    except Exception as e:
                        tk.Label(post_frame, text=f"Error loading image: {e}", fg="red", bg="#F5F5DC").pack(anchor="w")

                like_button = tk.Button(post_frame, text=f"Like ({post['likes']})",
                                        command=lambda p=post: toggle_like(p, user_name, refresh_user_posts), **button_style)
                like_button.pack(side="left", padx=10)
                comment_button = tk.Button(post_frame, text="Comments",
                                           command=lambda p=post: open_comments(s_manager, p, user_name), **button_style)
                comment_button.pack(side="left", padx=10)
        else:
            tk.Label(posts_frame, text="No posts available.", fg="gray", bg="#F5F5DC").pack()

    def refresh_user_posts():
        for widget in result_frame.winfo_children():
            widget.destroy()

        username = search_entry.get()
        post_data = s_manager.get_user_posts(username)
        display_user_bar(username, post_data)

    def send_friend_request(username, follow_button):
        success = False
        if username in s_manager.users:
            s_manager.send_friend_request(user_name, username)
            success = True

        if success:
            messagebox.showinfo("Friend Request", f"You sent a friend request to {username}.")
            follow_button.config(text="Request Sent", state=tk.DISABLED)
        else:
            messagebox.showwarning("Friend Request", f"Could not send a friend request to {username}.")

    search_button = tk.Button(search_frame, text="Search", command=search_user, **button_style)
    search_button.pack(side=tk.LEFT)

def open_friend_requests(new_window, s_manager, user_name):
    clear(new_window)
    pages_stack.push(lambda: home_page(new_window, s_manager, user_name))
    new_window.title("Friend Requests Page")
    new_window.geometry("700x700")
    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    tk.Label(new_window, text="Friend Requests Page", font=("Times New Roman", 16, "bold", "italic"), fg="#301934",bg="lavender").pack(pady=20)
    back_button = tk.Button(new_window, text="Back", command=back, **button_style)
    back_button.place(relx=0.0, rely=0.0, anchor="nw")

    friend_requests = s_manager.view_friend_requests(user_name)
    if not friend_requests:
        tk.Label(new_window, text="No friend requests available.", font=("Times New Roman", 15), fg="gray").pack(pady=20)
        return

    def accept_friend_request_handler(friend):
        s_manager.accept_friend_request(user_name, friend)
        refresh_friend_requests()

    def decline_friend_request_handler(friend):
        s_manager.decline_friend_request(user_name, friend)
        refresh_friend_requests()

    def refresh_friend_requests():
        for widget in request_frame.winfo_children():
            widget.destroy()

        friend_requests_updated = s_manager.view_friend_requests(user_name)
        if not friend_requests_updated:
            tk.Label(new_window, text="No friend requests available.", font=("Times New Roman", 14), fg="gray").pack(pady=20)
        else:
            for friend in friend_requests_updated:
                bar_frame = tk.Frame(request_frame, bd=2, relief="groove", padx=10, pady=5, bg="#F5F5DC")
                bar_frame.pack(fill=tk.X, pady=5)

                friend_label = tk.Label(bar_frame, text=friend, font=("Times New Roman", 12, "bold"), bg="#F5F5DC")
                friend_label.pack(side=tk.LEFT)

                accept_button = tk.Button(bar_frame, text="Accept", command=lambda f=friend: accept_friend_request_handler(f), **button_style)
                accept_button.pack(side=tk.RIGHT, padx=5)
                delete_button = tk.Button(bar_frame, text="Delete", command=lambda f=friend: decline_friend_request_handler(f), **button_style)
                delete_button.pack(side=tk.RIGHT, padx=5)
                view_profile_button = tk.Button(bar_frame, text="View Profile",command=lambda f=friend: open_profile_view(new_window, s_manager, f, s_manager.get_user_posts(f)), **button_style)
                view_profile_button.pack(side=tk.RIGHT, padx=5)

    request_frame = tk.Frame(new_window)
    request_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    refresh_friend_requests()

def open_messages(new_window,s_manager, user_name):
    clear(new_window)
    pages_stack.push(lambda: home_page(new_window, s_manager, user_name))
    new_window.title("Messages Page")
    new_window.geometry("700x700")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Modern.TButton", font=("Times New Roman", 13), padding=10, background="#9A7BBA", foreground="#E4E1E1")
    style.map("Modern.TButton", background=[("active", "#CCCCFF")], foreground=[("active", "gray")])
    tk.Label(new_window, text=f"{user_name} Messages", font=("Times New Roman", 16, "bold"), fg="#4f4f4f",bg="lavender").pack(pady=30)
    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    back_button = tk.Button(new_window, text="Back", command=back,**button_style)
    back_button.place(relx=0.0, rely=0.0, anchor="nw")

    user_data = s_manager.users.get(user_name)
    if user_data["friends"] == []:
        post_label = tk.Label(new_window, text="you don't have friends!", wraplength=400, justify="left",font=("Times New Roman", 12), fg="gray")
        post_label.pack(pady=5, anchor=tk.CENTER)

    for friend in user_data["friends"]:
        btn = ttk.Button(new_window, text=friend, width=30, style="Modern.TButton", command=lambda x=friend: open_friend_chat(new_window,s_manager, user_name, x))
        btn.pack(pady=15)

def open_friend_chat(chat_window ,s_manager, user_name, friend):
    clear(chat_window)
    pages_stack.push(lambda: open_messages(chat_window,s_manager, user_name))
    chat_window.title(f"{friend}'s Chat")
    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    back_button = tk.Button(chat_window, text="Back",command=back,**button_style)
    back_button.place(relx=0.0, rely=0.0, anchor="nw")
    chat_window.geometry("700x700")
    tk.Label(chat_window, text=f"{friend}'s Chat", font=("Times New Roman", 16, "italic"), fg="#4f4f4f",bg="lavender").pack(pady=30)

    chat_frame = tk.Frame(chat_window)
    chat_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(chat_frame)
    scrollbar.pack(side="right", fill="y")
    text_area = tk.Text(chat_frame, height=20, yscrollcommand=scrollbar.set, wrap="word")
    text_area.pack(fill="both", expand=True)
    scrollbar.config(command=text_area.yview)

    user_data = s_manager.users.get(user_name)
    chat_list = []
    for received in user_data.get("messages_to_you", []):
        if received["from"] == friend:
            chat_list.append({'user': 'friend', 'time': received["time"], 'message': received["content"]})

    for sent in user_data.get("messages_from_you", []):
        if sent["to"] == friend:
            chat_list.append({'user': 'me', 'time': sent["time"], 'message': sent["content"]})

    if chat_list ==[]:
        text_area.insert("end", "No Messages to show.", "no_messages")
        text_area.tag_config("no_messages", foreground="gray")
    else:
        chat_list.sort(key=lambda x: x['time'])
        for message in chat_list:
            message_time = datetime.strptime(message['time'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%H:%M")
            if message['user'] == 'friend':
                text_area.insert("end", f"{friend}: {message_time} : {message['message']}\n", "friend")
            else:
                text_area.insert("end", f"Me: {message_time} : {message['message']}\n", "mee")

        text_area.tag_config("friend", foreground="purple", background="#CCCCFF", font=("Times New Roman", 12))
        text_area.tag_config("mee", foreground="black", background="gray", font=("Times New Roman", 12))

    entry_frame = tk.Frame(chat_window)
    entry_frame.pack(fill="x", padx=10, pady=10)
    new_message = tk.Entry(entry_frame, font=("Times New Roman", 12))
    new_message.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    def send():
        message = new_message.get().strip()
        if message:
            if "no_messages" in text_area.tag_names("1.0"):
                text_area.delete("1.0", "end")
            s_manager.send_message(user_name, friend, message)
            sent_time = datetime.now().strftime("%H:%M")
            text_area.insert("end", f"Me: {sent_time} : {message}\n", "mee")
            new_message.delete(0, "end")

    send_button = tk.Button(entry_frame, text="Send", command=send,**button_style)
    send_button.pack(side="right", padx=10)

def open_comments(s_manager, post, user_name):
    new_window = tk.Toplevel()
    new_window.title(f"Comments on Post {post['post_id']}")
    new_window.geometry("500x500")

    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    label_style = {"font": ("Arial", 12, "bold"), "bg": "#F5F5DC", "anchor": "w", "justify": "left"}
    comment_frame = tk.Frame(new_window)
    comment_frame.pack(pady=20, fill=tk.BOTH, expand=True)
    tk.Label(comment_frame, text=f"Comments on {post['type']} by {post['author']}",font=("Times New Roman", 16, "bold", "italic"), fg="#301934").pack(pady=10)
    canvas = tk.Canvas(comment_frame)
    scrollbar = tk.Scrollbar(comment_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    comments = post['comments']
    if comments:
        for comment in comments:
            comment_display = tk.Frame(scrollable_frame, bd=1, relief="solid", padx=10, pady=5, bg="#F5F5DC")
            comment_display.pack(fill=tk.X, pady=5)
            tk.Label(comment_display, text=f"{comment['user']}: {comment['comment']}", **label_style).pack(fill=tk.X)
    else:
        tk.Label(scrollable_frame, text="No comments available.", fg="gray", bg="#F5F5DC").pack(pady=10)

    comment_entry = tk.Entry(new_window, font=("Arial", 12))
    comment_entry.pack(fill=tk.X, padx=20, pady=(10, 0))
    submit_button = tk.Button(new_window, text="Add Comment", command=lambda: add_comment(), **button_style)
    submit_button.pack(pady=10)

    def add_comment():
        comment_text = comment_entry.get()
        if comment_text:
            s_manager.comment_on_post(post, comment_text, user_name)
            comment_display = tk.Frame(scrollable_frame, bd=1, relief="solid", padx=10, pady=5, bg="#F5F5DC")
            comment_display.pack(fill=tk.X, pady=5)
            tk.Label(comment_display, text=f"{user_name}: {comment_text}", **label_style).pack(fill=tk.X)
            comment_entry.delete(0, tk.END)

def quick_sort_notifications(notifications):
    if len(notifications) <= 1:
        return notifications
    pivot = notifications[len(notifications) // 2]
    pivot_time = datetime.strptime(pivot['time'], "%Y-%m-%d %H:%M:%S")
    left = [x for x in notifications if datetime.strptime(x['time'], "%Y-%m-%d %H:%M:%S") > pivot_time]
    middle = [x for x in notifications if datetime.strptime(x['time'], "%Y-%m-%d %H:%M:%S") == pivot_time]
    right = [x for x in notifications if datetime.strptime(x['time'], "%Y-%m-%d %H:%M:%S") < pivot_time]
    return quick_sort_notifications(left) + middle + quick_sort_notifications(right)

def open_notifications(new_window, s_manager, user_name):
    clear(new_window)
    pages_stack.push(lambda: home_page(new_window, s_manager, user_name))
    new_window.title("Notifications Page")
    new_window.geometry("700x700")
    new_window.configure(bg="lavender")
    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    back_button = tk.Button(new_window, text="Back",command=back,**button_style)
    back_button.place(relx=0.0, rely=0.0, anchor="nw")

    tk.Label(new_window, text="Notifications", font=("Times New Roman", 16, "bold", "italic"),
             fg="black", bg="lavender").pack(pady=20)
    user_posts = s_manager.get_user_posts(user_name)

    if not user_posts:
        tk.Label(new_window, text="No notifications available.", font=("Arial", 14), fg="gray", bg="lavender").pack(pady=20)
        return

    notifications = []

    for post in user_posts:
        for like in post['liked_by']:
            notifications.append({
                'user': like['user'],
                'action': 'liked your post',
                'time': like['time'],
                'post': post
            })

        for comment in post['comments']:
            notifications.append({
                'user': comment['user'],
                'action': 'commented on your post',
                'time': comment.get('time', None),
                'post': post
            })

    sorted_notifications = quick_sort_notifications(notifications)
    notif_frame = tk.Frame(new_window, bg="lavender")
    notif_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    button_style = {"font": ("Times New Roman", 13, "bold"), "fg": "white", "bg": "#9B59B6"}

    for notif in sorted_notifications:
        post_notif_frame = tk.Frame(notif_frame, bg="white", pady=5)
        post_notif_frame.pack(fill=tk.X, pady=5)

        notification_text = f"{notif['user']} {notif['action']} at {notif['time']}"
        tk.Label(post_notif_frame, text=notification_text, font=("Arial", 12), fg="purple", bg="white").pack(side=tk.LEFT)
        tk.Button(post_notif_frame, text="View", **button_style, command=lambda p=notif['post']: open_post_view(new_window, p, s_manager)).pack(side=tk.RIGHT)

def open_post_view(post_window, post, s_manager):
    clear(post_window)
    pages_stack.push(lambda: open_notifications(post_window,s_manager,post['author']))
    post_window.title(f"Post by {post['author']}")
    post_window.geometry("700x700")
    post_window.configure(bg="lavender")
    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    back_button = tk.Button(post_window, text="Back",command=back,**button_style)
    back_button.place(relx=0.0, rely=0.0, anchor="nw")
    tk.Label(post_window, text=f"Post by {post['author']}", font=("Times New Roman", 16, "bold"), bg="lavender").pack(
        pady=10)
    if post['type'] == "text":
        tk.Label(post_window, text=post['content'], font=("Arial", 12), bg="lavender").pack(pady=10)
    elif post['type'] == "image":
        image = Image.open(post['image_path'])
        image = image.resize((400, 300))
        photo = ImageTk.PhotoImage(image)
        tk.Label(post_window, image=photo, bg="lavender").image = photo
        tk.Label(post_window, image=photo, bg="lavender").pack(pady=10)

    likes_count = len(post['liked_by'])
    tk.Label(post_window, text=f"Likes: {likes_count}", font=("Arial", 12), bg="lavender").pack(pady=5)

    comments = post['comments']
    tk.Label(post_window, text="Comments:", font=("Arial", 12, "bold"), bg="lavender").pack(pady=10)

    comment_frame = tk.Frame(post_window, bg="lavender")
    comment_frame.pack(pady=5)

    if comments:
        for comment in comments:
            tk.Label(comment_frame, text=f"{comment['user']}: {comment['comment']}", bg="lavender").pack(anchor="w",
                                                                                                          padx=10,
                                                                                                          pady=2)
    else:
        tk.Label(comment_frame, text="No comments yet.", bg="lavender").pack(anchor="w", padx=10)

def save_post(s_manager, post, user_name):
    s_manager.save_post_for_user(user_name, post)

def open_saved_posts(new_window, s_manager, user_name):
    clear(new_window)
    pages_stack.push(lambda: home_page(new_window, s_manager, user_name))
    new_window.title("Saved Posts")
    new_window.geometry("700x700")
    new_window.configure(bg="lavender")

    tk.Label(new_window, text="Saved Posts", font=("Times New Roman", 16, "bold", "italic"), fg="black", bg="lavender").pack(pady=20)
    button_style = {"font": ("Times New Roman", 13, "italic"), "fg": "white", "bg": "#9B59B6"}
    back_button = tk.Button(new_window, text="Back",command=back,**button_style)
    back_button.place(relx=0.0, rely=0.0, anchor="nw")
    posts_frame = tk.Frame(new_window, bg="purple")
    posts_frame.pack(fill="both", expand=True, pady=20)

    canvas = tk.Canvas(posts_frame, bg="lavender")
    scrollbar = ttk.Scrollbar(posts_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="lavender")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    def refresh_saved_posts():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        saved_posts = s_manager.get_saved_posts(user_name)

        if not saved_posts:
            tk.Label(scrollable_frame, text="No saved posts available.", font=("Arial", 14), fg="gray", bg="lavender").pack(pady=20)
            return

        button_style = {"font": ("Times New Roman", 13, "bold"), "fg": "white", "bg": "#9B59B6"}

        for post in saved_posts:
            post_frame = tk.Frame(scrollable_frame, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="lavender")
            post_frame.pack(fill="x", pady=10)

            post_author = post['author']
            post_content = post.get('content', '')

            author_label = tk.Label(post_frame, text=f"Post by: {post_author}", font=("Arial", 12, "bold"), bg="lavender")
            author_label.pack(anchor="w")

            if post['type'] == "text":
                content_label = tk.Label(post_frame, text=post_content, font=("Arial", 11), bg="lavender")
                content_label.pack(anchor="w", pady=5)
            elif post['type'] == "image":
                image = Image.open(post['image_path'])
                image = image.resize((400, 300))
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(post_frame, image=photo, bg="lavender")
                image_label.image = photo
                image_label.pack(anchor="w", pady=5)

            like_button = tk.Button(post_frame, text=f"Like ({post['likes']})",
                                    command=lambda p=post: toggle_like(p, user_name, refresh_saved_posts), **button_style)
            like_button.pack(side="left", padx=10)

            comment_button = tk.Button(post_frame, text="Comments",
                                       command=lambda p=post: open_comments(s_manager, p, user_name), **button_style)
            comment_button.pack(side="left", padx=10)

    refresh_saved_posts()


def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

SMM = SocialMediaManager()

login()