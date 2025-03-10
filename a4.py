# Stephanie Lee
# stephl25@uci.edu
# 79834162

# TODO: keep debugging

import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from typing import Text
from ds_messenger import DirectMessenger
from Profile import Profile, Message, DsuFileError, DsuProfileError
import checker as c
from pathlib import Path


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback

        self._draw()

    def node_select(self, event):
        if self.posts_tree.selection():
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

    def insert_user_message(self, message: str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text, 'make-it-pretty')

    def clear_text_entry(self):
        self.message_editor.delete(1.0, tk.END)

    def clear_entry_editor(self):
        self.entry_editor.delete(1.0, tk.END)

    def clear_contact_tree(self):
        to_delete = self.posts_tree.get_children()
        for tree_child in to_delete:
            self.posts_tree.delete(tree_child)

    def _draw(self):
        posts_frame = tk.Frame(master=self, bg='#063f02', width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="#063f02")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="#063f02", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="#063f02")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.tag_configure('make-it-pretty', foreground='#063f02', font=('Mincho', 10, 'bold'))
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=5, pady=5)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right', background='#c98a3e', font=('Mincho', 10, 'bold'))
        self.entry_editor.tag_configure('entry-left', justify='left', background='#eeab50', font=('Mincho', 10, 'bold'))
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=5, pady=5)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=2, pady=2)


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
        save_button = tk.Button(master=self, text="Send", width=20, fg='#063f02', bg='#c98a3e', font=('Mincho', 10, 'bold'))
        save_button.config(command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.", fg='#063f02', font=('Mincho', 10, 'bold'))
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

    def configure_file(self):
        try:
            c.check_connection(self.is_connected)
            self.close_file()
            create_file = NewFileDialog(self.root, "Configure New File",
                                        self.path, self.file_name)
            c.check_cancel(create_file.path)
            c.check_cancel(create_file.file_name)
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
                self.path = file_path

            self.profile.load_profile(self.path)
            c.check_match(self.profile, self.username, self.password)
            self._load_contacts()
            self.check_new()
            self.body.set_text_entry('File opened.')
            self.is_loaded = True
        except c.NotConnected:
            self.body.set_text_entry('Please load a profile.')
        except c.CancelledEvent:
            self.body.set_text_entry('Cancelled creating a new file.')
        except c.Mismatched:
            self.body.set_text_entry('Failed to open file. File info must match the current profile.')
        except FileNotFoundError:
            self.body.set_text_entry('Could not find file/directory. Check the correctness of the directory.')
        finally:
            self.body.after(3000, self.body.clear_text_entry)

    def open_file(self):
        try:
            self.close_file()
            self.path = filedialog.askopenfilename()

            c.check_cancel(self.path)
            c.check_suffix(self.path)
            c.check_existence(self.path)

            self.profile.load_profile(self.path)

            c.check_match(self.profile, self.username, self.password)

            self._load_contacts()
            self.check_new()
            self.body.set_text_entry("File opened.")
            self.is_loaded = True
        except c.Mismatched as error_msg:
            self.body.set_text_entry(f'{error_msg}')
        except c.CancelledEvent:
            self.body.set_text_entry('Cancelled opening file')
        except TypeError:
            self.body.set_text_entry('Only .dsu file types are supported.')
        except DsuProfileError:
            self.body.set_text_entry('File must have a Profile stored within it.')
        except DsuFileError:
            self.body.set_text_entry('DSU file does not exist.')
        except FileNotFoundError:
            self.body.set_text_entry('File was not found.')
        finally:
            self.body.after(2000, self.body.clear_text_entry)

    def close_file(self):
        self.body.clear_contact_tree()
        self.body.clear_text_entry()
        self.body.clear_entry_editor()
        self.profile = Profile()
        self.path = ""
        self.file_name = ""
        self.is_loaded = False

    def add_contact(self):
        try:
            c.check_connection(self.is_connected)
            c.check_connection(self.is_loaded)

            new_contact = simpledialog.askstring(title="New Contact", prompt="Enter:",)

            c.check_cancel(new_contact)
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
            self.body.set_text_entry('Please log in then open a file.')
        except c.CancelledEvent:
            self.body.set_text_entry("Cancelled adding contact.")
        except c.AlreadyExistsError:
            self.body.set_text_entry(f"Contact {new_contact} is already listed.")
        except c.InvalidRecipient:
            self.body.set_text_entry("Adding yourself as a contact is not allowed.")
        finally:
            self.body.after(3000, self.body.clear_text_entry)

    def _load_contacts(self):
        friends = self.profile.friends
        self.body.clear_contact_tree()
        for friend in friends:
            self.body.insert_contact(friend)

    def recipient_selected(self, recipient):
        self.recipient = recipient
        self._load_messages()
        self._refresh_messages()

    def _load_messages(self):
        self.check_new()
        self.body.clear_entry_editor()
        all_messages = sorted(self.profile.get_messages(), key=lambda item: item['timestamp'], reverse=True)
        for message in all_messages:
            if message['from_user'] == self.recipient:
                self.body.insert_contact_message(message['entry'])
            elif message['from_user'] == self.username and message['to_user'] == self.recipient:
                self.body.insert_user_message(message['entry'])

    def _refresh_messages(self):
        if self.recipient:
            self._load_messages()
            self.body.after(2000, self._refresh_messages)

    def check_new(self):
        try:
            c.check_connection(self.is_connected)
            inbox = self.direct_messenger.retrieve_new()
            self.save_messages_locally(inbox)
            return inbox
        except c.NotConnected:
            self.body.set_text_entry('Please load a profile. Then load a file to save your messages and contacts.')
            self.body.after(3000, self.body.clear_text_entry)

    def save_messages_locally(self, msg_inbox):
        for message in msg_inbox:
            new_msg = Message(entry=message['message'],
                              timestamp=message['timestamp'],
                              from_user=message['from'])
            self.profile.add_msg(new_msg)
            self.profile.save_profile(self.path)

    def send_message(self):
        try:
            c.check_connection(self.is_loaded)
            c.check_connection(self.is_connected)
            message_to_send = self.body.get_text_entry()
            if c.check_valid_entry(message_to_send):
                if self.publish(message_to_send):
                    new_post = Message(entry=message_to_send,
                                    from_user=self.username,
                                    to_user=self.recipient)
                    self.profile.add_msg(new_post)
                    self.profile.save_profile(self.path)
        except c.InvalidEntry:
            self.body.set_text_entry('Sending empty messages is not allowed.')
        except c.NotConnected:
            self.body.set_text_entry('Connect to a server and select a file to send messages.')
        finally:
            self.body.after(2000, self.body.clear_text_entry)

    def publish(self, message: str) -> bool:
        try:
            if (self.recipient == self.username) or (not self.recipient):
                raise c.InvalidRecipient

            if self.direct_messenger.send(message, self.recipient):
                self.body.entry_editor.insert(tk.END, message + '\n', 'entry-right')
                self.body.set_text_entry('Sent.')
                return True
            else:
                self.body.set_text_entry('Failed to send.')
        except c.InvalidRecipient:
            self.body.set_text_entry('Please select a recipient. Note: Sending messages to yourself is unsupported.')
        return False

    def configure_server(self):
        try:
            ud = NewContactDialog(self.root, "Configure Account",
                                  self.username, self.password, self.server)
            c.check_cancel(ud.user)
            c.check_cancel(ud.pwd)
            c.check_cancel(ud.server)
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server

            self.close_file()

            self.direct_messenger = DirectMessenger(self.server, self.username, self.password)
            welcome_msg = self.direct_messenger.start_session()

            if welcome_msg is False:
                self.body.set_text_entry(f'Wrong password for {self.username}')
            elif welcome_msg is None:
                self.body.set_text_entry('A bad server was entered')
            else:
                self.body.set_text_entry(f'{welcome_msg} Load a file to get started.')
                self.is_connected = True
        except c.CancelledEvent:
            self.body.set_text_entry('Cancelled loading a profile.')
        finally:
            self.body.after(2000, self.body.clear_text_entry)

    def _draw(self):
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

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    main = tk.Tk()

    main.title("We Won't Steal Your Data Messenger ;)")
    main.geometry("720x480")

    main.option_add('*tearOff', False)

    app = MainApp(main)

    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)

    main.mainloop()
