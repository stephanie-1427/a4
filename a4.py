# Stephanie Lee
# stephl25@uci.edu
# 79834162

# TODO: look at todo's in code
# TODO: take out comments when done
# TODO: debug
# TODO: style check
# TODO: remove unused stuff from checker.py
# TODO: streamline design

import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from typing import Text
from ds_messenger import DirectMessenger
from Profile import Profile, Message
import checker as c
from pathlib import Path


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)
    
    def clear_text_entry(self):
        self.message_editor.delete(1.0, tk.END)

    def clear_entry_editor(self):
        self.entry_editor.delete(1.0, tk.END)
    
    def clear_contact_tree(self):
        to_delete = self.posts_tree.get_children()
        for tree_child in to_delete:
            self.posts_tree.delete(tree_child)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.config(command=self.send_click)
        '''# You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.'''
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry['show'] = '*'
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()

class NewFileDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, path=None, file_name=None):
        self.root = root
        self.path = path
        self.file_name = file_name
        super().__init__(root, title)

    def body(self, frame):
        self.path_label = tk.Label(frame, width=30, text="Directory to create the new file in")
        self.path_label.pack()
        self.path_entry = tk.Entry(frame, width=50)
        self.path_entry.insert(tk.END, self.path)
        self.path_entry.pack()

        self.file_name_label = tk.Label(frame, width=30, text="File Name")
        self.file_name_label.pack()
        self.file_name_entry = tk.Entry(frame, width=30)
        self.file_name_entry.insert(tk.END, self.file_name)
        self.file_name_entry.pack()

    def apply(self):
        self.path = self.path_entry.get()
        self.file_name = self.file_name_entry.get()

class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''

        self.direct_messenger = DirectMessenger()
        self.is_connected = False

        self.profile = Profile()
        self.path = ""
        self.file_name = ""
        self.is_loaded = False

        self._draw()
        self.body.insert_contact("studentexw23") # adding one example student.

    def configure_file(self):
        try:
            if not self.is_connected:
                raise c.NotConnected
            self.close_file()
            create_file = NewFileDialog(self.root, "Configure New File",
                                self.path, self.file_name)
            self.path = Path(create_file.path)
            self.file_name = create_file.file_name

            new_file = self.path / self.file_name
            file_path = new_file.with_suffix('.dsu')

            if not file_path.exists():
                file_path.touch()
                self.profile = Profile(self.server, self.username, self.password)
                self.path = file_path
                self.profile.save_profile(self.path)
            else:
                self.body.set_text_entry('File already exists. Opening existing file...')
            self.profile.load_profile(self.path)

            if self.profile.username != self.username or self.profile.password != self.password:
                raise c.Mismatched
            
            self.body.set_text_entry('File opened successfully.')
            self._load_contacts()
            self.check_new() #TODO: implement with after. Make sure messages are automatically being received
            self.is_loaded = True
        except c.NotConnected:
            self.body.set_text_entry('Please load a profile.')
        except c.Mismatched:
            self.body.set_text_entry('Failed to open file. File info must match the current profile.')
        except FileNotFoundError:
            self.body.set_text_entry('Could not find file/directory. Check the correctness of the directory.')
        finally:
            self.body.after(5000, self.body.clear_text_entry)

    def open_file(self):
        try:
            self.close_file()
            self.path = filedialog.askopenfilename()
            self.profile.load_profile(self.path)
            #TODO: exception handling here, not dsu file, profile missing, check its existence
            if self.profile.username != self.username or self.profile.password != self.password:
                raise c.Mismatched
            self._load_contacts()
            self.check_new()
            self.body.set_text_entry("File opened.")
            self.is_loaded = True
        except c.Mismatched:
            self.body.set_text_entry('Failed to open file. File info must match the current profile.')
        finally:
            self.body.after(5000, self.body.clear_text_entry)

    def _load_contacts(self):
        friends = self.profile.friends
        self.body.clear_contact_tree()
        for friend in friends:
            self.body.insert_contact(friend)

    def _load_messages(self):
        all_messages = sorted(self.profile.get_messages(), key=lambda item: item['timestamp'], reverse=True)
        for message in all_messages:
            if message['from_user'] == self.recipient:
                self.body.insert_contact_message(message['entry'])
            elif message['from_user'] == self.username and message['to_user'] == self.recipient:
                self.body.insert_user_message(message['entry'])

    def save_messages_locally(self, msg_inbox):
        for message in msg_inbox:
            new_msg = Message(entry=message['message'], timestamp=message['timestamp'], from_user=message['from'])
            self.profile.add_msg(new_msg)
            self.profile.save_profile(self.path)

    def close_file(self):
        self.body.clear_contact_tree()
        self.body.clear_text_entry()
        self.body.clear_entry_editor()
        self.profile = Profile()
        self.path = ""
        self.file_name = ""
        self.is_loaded = False

    def send_message(self):
        try:
            message_to_send = self.body.get_text_entry()
            if c.check_valid_entry(message_to_send):
                self.publish(message_to_send)
                new_post = Message(entry=message_to_send, from_user=self.username, to_user=self.recipient)
                self.profile.add_msg(new_post)
                self.profile.save_profile(self.path)
        except c.InvalidEntry:
            self.body.set_text_entry('Sending empty messages is not allowed.')
            self.body.after(5000, self.body.clear_text_entry)

    def publish(self, message:str):
        try:
            if (self.recipient == self.username) or (not self.recipient):
                raise c.InvalidRecipient

            if self.direct_messenger.send(message, self.recipient):
                self.body.insert_user_message(message)
                self.body.set_text_entry('Sent.')
            else:
                self.body.set_text_entry('Failed to send.')
        except c.InvalidRecipient:
            self.body.set_text_entry('Please select a recipient. Note: Sending messages to yourself is unsupported.')
        finally:
            self.body.after(5000, self.body.clear_text_entry)

    def add_contact(self):
        try:
            if not self.is_connected:
                raise c.NotConnected

            if not self.is_loaded:
                self.body.set_text_entry('Warning: Adding a contact without loading a file. Changes will not be saved.')

            new_contact = simpledialog.askstring(title="Add Contact", prompt="Enter:",)

            if not new_contact:
                raise c.CancelledEvent
            if new_contact in self.profile.friends:
                raise c.AlreadyExistsError
            if new_contact == self.username:
                raise c.InvalidRecipient
            
            self.body.insert_contact(new_contact)
            if self.is_loaded:
                self.profile.make_friend(new_contact)
                self.profile.save_profile(self.path)
            self.body.set_text_entry(f"New contact entered: {new_contact}")
        except c.NotConnected:
            self.body.set_text_entry('Please log in or sign up with a usernmame a password first.')
        except c.CancelledEvent:
            self.body.set_text_entry("Cancelled adding contact.")
        except c.AlreadyExistsError:
            self.body.set_text_entry(f"Contact {new_contact} is already listed.")
        except c.InvalidRecipient:
            self.body.set_text_entry("Adding yourself as a contact is not allowed.")
        finally:
            self.body.after(3000, self.body.clear_text_entry)

    def recipient_selected(self, recipient):
        self.recipient = recipient
        self._load_messages()

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server

        self.close_file()

        self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
        welcome_msg = self.direct_messenger.start_session()

        self.body.set_text_entry(f'{welcome_msg} Load a file to get started.')
        self.is_connected = True

    def check_new(self):
        try:
            if not self.is_connected:
                raise c.NotConnected
            inbox = self.direct_messenger.retrieve_new()
            self.save_messages_locally(inbox)
            return inbox
        except c.NotConnected:
            self.body.set_text_entry('Please load a profile. Then load a file to save your messages and contacts.')
            self.body.after(5000, self.body.clear_text_entry)


    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.configure_file)
        menu_file.add_command(label='Open...', command=self.open_file)
        menu_file.add_command(label='Close', command=self.close_file)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
