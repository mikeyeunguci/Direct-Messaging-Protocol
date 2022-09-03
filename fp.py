# Rio Suzuki
# rios@uci.edu
# 78627374

# Michael Yeung
# myeung2@uci.edu
# 71598323

import tkinter as tk
from tkinter import ttk, filedialog
from Profile import Profile, RecipientNotFound
from ds_messenger import DirectMessage, DirectMessenger
import time


class EditBody(tk.Frame):
    """
    Creating the username/password body
    """
    def __init__(self, root, profile:Profile):
        tk.Frame.__init__(self, root)
        self.root = root
        self.profile = profile
        
        tk.Label(self.root, text='Username').grid(row=0)
        tk.Label(self.root, text='Password').grid(row=1)

        self.inputUsername = tk.Entry(self.root)
        self.inputPassword = tk.Entry(self.root)
        self.inputUsername.grid(row=0, column=1)
        self.inputPassword.grid(row=1, column=1)

        #import data from profile
        self.inputUsername.insert(10, profile.username)
        self.inputPassword.insert(10, profile.password)

class EditWindow(tk.Toplevel):
    """
    Creating the settings window for editing username/password
    """
    def __init__(self, root, profile:Profile):
        super().__init__(root)
        self.root = root
        self.title("Edit Profile")
        self.profile = profile

        self.body = EditBody(self, self.profile)

        button = tk.Button(self, text='Done', command=self.on_close)
        button.grid(row=3, column=1)

    def on_close(self):
        if self.profile.username in self.profile.chats and not self.profile.username == self.body.inputUsername.get():
            self.profile.chats.pop(self.profile.username)
        self.profile.username = self.body.inputUsername.get()
        self.profile.password = self.body.inputPassword.get()
        self.profile.save_profile(self.root._profile_filename)
        self.root.ds = DirectMessenger(self.root.dsuserver, self.body.inputUsername.get(), self.body.inputPassword.get())
        self.root.footer.set_status(f"Welcome {self.profile.username} to ICS Messenger ")
        if not self.profile.username in self.profile.chats:
            self.profile.chats[self.profile.username] = []
        self.destroy()

class BioBody(tk.Frame):
    """
    Creating the edit bio body
    """
    def __init__(self, root, profile:Profile):
        tk.Frame.__init__(self, root)
        self.root = root
        self.profile = profile

        tk.Label(self.root, text='Bio').grid(row=0)

        self.inputBio = tk.Text(self.root)
        self.inputBio.grid(row=1, column=0)

        #import data from profile
        self.inputBio.insert(0.0, profile.bio)

class BioWindow(tk.Toplevel):
    """
    Creating the settings window for changing bio
    """
    def __init__(self, root, profile:Profile):
        super().__init__(root)
        self.root = root
        self.title("Edit Bio")
        self.profile = profile
        self.geometry('700x450')

        self.body = BioBody(self, self.profile)

        button = tk.Button(self, text='Done', command=self.on_close)
        button.grid(row=3, column=1)

    def on_close(self):
        self.profile.bio = self.body.inputBio.get(0.0, 'end')
        self.profile.save_profile(self.root._profile_filename)
        self.destroy()

class AddUser(tk.Frame):
    """
    Creating the body to add a user to talk to
    """
    def __init__(self, root, profile:Profile):
        tk.Frame.__init__(self, root)
        self.root = root
        self.profile = profile
        
        tk.Label(self.root, text='Recipient').grid(row=0)

        self.inputRecipient = tk.Entry(self.root)
        self.inputRecipient.grid(row=0, column=1)

class AddWindow(tk.Toplevel):
    """
    Creating a window to add user in the settings
    """
    def __init__(self, root, profile:Profile):
        super().__init__(root)
        self.root = root
        self.title("Add Recipient")
        self.profile = profile

        self.body = AddUser(self, self.profile)

        button = tk.Button(self, text='Add', command=self.on_close)
        button.grid(row=3, column=1)

    def on_close(self):
        self.profile.chats[self.body.inputRecipient.get()] = []
        self.root.body.set_dms(self.profile.chats, self.profile.username)
        self.profile.save_profile(self.root._profile_filename)
        self.destroy()

class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_callback=None, app = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self.app = app

        # a list of the dms objects available in the active DSU file
        self.dms = [DirectMessage]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()

    def node_select(self, event):
        """
        Displays message from the selected recipient
        """
        try:
            index = int(self.dms_tree.selection()[0])
            name = self.dms[index]
            self.app.current_recipient = name
        except:
            pass
        self.app.load_messages()

        self.message_editor.configure(state = "normal")
        self.message_editor.delete('1.0', 'end')
        #scrolls to bottom
        self.display.see('end')

    def get_selected_index(self):
        """
        Returns the index of the selected recipient
        """
        if len(self.dms_tree.selection()) > 0:
            return int(self.dms_tree.selection()[0])
        return -1

    def get_text_message(self) -> str:
        """
        Returns the text that is currently displayed in the message_editor widget.
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def add_text_message(self, text:str):
        """
        Add new text to the display box
        """
        # code that deletes all current text in the self.display widget
        # and inserts the value contained within the text parameter.
        self.display.insert('end', text)
        self.display.see('end')

    def set_dms(self, dms:dict, exclude_name:str):
        """
        Populates the tree with the recipient names
        """
        self.dms = []
        self.dms_tree.delete(*self.dms_tree.get_children())

        keys = list(dms.keys())

        for i in range (len(keys)):
            if not keys[i] == exclude_name:
                self.insert_name(str(keys[i]))

    def insert_name(self, name:str):
        """
        Inserts a single recipient name to the dms_tree widget.
        """
        self.dms.append(name)
        id = len(self.dms) - 1 #adjust id for 0-base of treeview widget
        self._insert_names_tree(id, name)

    def reset_ui(self):
        """
        Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DSU file is loaded, for example.
        """
        self.add_text_message("")
        self.dms = []
        for item in self.dms_tree.get_children():
            self.dms_tree.delete(item)

    def _insert_names_tree(self, id, name:str):
        """
        Inserts a user's name into the dms_tree widget.
        """
        self.dms_tree.insert('', id, id, text=name)

    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        dms_frame = tk.Frame(master=self, width=250)
        dms_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.dms_tree = ttk.Treeview(dms_frame)
        self.dms_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.dms_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        
        message_frame = tk.Frame(master=self, bg="")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=message_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=message_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        #chat display
        self.display = tk.Text(editor_frame, height=0, width=0, state='disabled')
        self.display.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=0, pady=0)
        #chat entry box
        self.message_editor = tk.Text(editor_frame, width=0, height=7, state='disabled')
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        message_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.message_editor.yview)
        self.message_editor['yscrollcommand'] = message_editor_scrollbar.set
        message_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, save_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._draw()

    def save_click(self):
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._save_callback is not None:
            self._save_callback()

    def set_status(self, message):
        """
        Updates the text that is displayed in the footer_label widget
        """
        self.footer_label.configure(text=message)

    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        self._img = tk.PhotoImage(file = './cat.png')
        self._img = self._img.subsample(10, 10)

        save_button = tk.Button(master=self, text="Send", width=100, image = self._img)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the Profile class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._is_loaded = False
        self._is_online = False
        self.current_recipient = ""
        self.ds = None
        self.dsuserver = "168.235.86.101"

        # Initialize a new Profile and assign it to a class attribute.
        self._current_profile = Profile()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        filename = tk.filedialog.asksaveasfile(defaultextension='.dsu', filetypes=[('Distributed Social Profile', '*.dsu')])

        # TODO Write code to perform whatever operations are necessary to prepare the UI for
        # a new DSU file.
        # HINT: You will probably need to do things like generate encryption keys and reset the ui.
        if not filename == None:
            self._profile_filename = filename.name
            self._current_profile = Profile()
            self.body.reset_ui()

            self._is_loaded = True
            self.footer.set_status(f"Welcome {self._current_profile.username} to ICS Messenger ")

    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        # TODO: Write code to perform whatever operations are necessary to prepare the UI for
        # an existing DSU file.
        # HINT: You will probably need to do things like load a profile, import encryption keys 
        # and update the UI with dms.
        if not filename == None:
            self.body.reset_ui()
            self._profile_filename = filename.name
            self._current_profile = Profile()
            self._current_profile.load_profile(self._profile_filename)

            self._is_loaded = True
            self.body.set_dms(self._current_profile.chats, self._current_profile.username)
            self.ds = DirectMessenger(self.dsuserver, self._current_profile.username, self._current_profile.password)
            self.footer.set_status(f"Welcome {self._current_profile.username} to ICS Messenger ")

    def load_messages(self):
        """
        Load messages from the selected user
        """
        self.body.display.configure(state = "normal")
        self.body.display.delete('0.0', 'end')

        if self.ds.is_connected:
            self._current_profile.chats[self.current_recipient].clear()

            all_msgs = self.ds.retrieve_all()
            for entry in all_msgs:
                if entry['from'] == self.current_recipient:
                    new_dm = DirectMessage(self._current_profile.username, entry['message'], float(entry['timestamp']))
                    self._current_profile.chats[entry['from']].append(new_dm)

        #get message from recipient
        dm_messages = []
        for message in self._current_profile.chats[self.current_recipient]:
            new_dm = DirectMessage(self.current_recipient, message['message'], message['timestamp'])
            dm_messages.append(new_dm)

        #get message from self to recipient
        if self._current_profile.username in self._current_profile.chats:
            for message in self._current_profile.chats[self._current_profile.username]:
                if message['recipient'] == self.current_recipient:
                    new_dm = DirectMessage(self._current_profile.username, message['message'], message['timestamp'])
                    dm_messages.append(new_dm)

        #sort the combined list
        dm_messages = sorted(dm_messages, key=lambda message: message['timestamp'])

        for message in dm_messages:
            self.body.add_text_message(f"{message['recipient']}: {message['message']}\n\n")
        self.body.display.configure(state = "disabled")

        if self.ds.is_connected:
            self.after(2000, self.check_msg)

    def check_msg(self):
        """
        Checks new messages from the recipient
        """
        new_msg_list = self.ds.retrieve_new()
        for entry in new_msg_list:
            if new_msg_list is not []:
                #save to file
                for message in new_msg_list:
                    new_dm = DirectMessage(message['from'], message['message'], message['timestamp'])
                    if not message['from'] in self._current_profile.chats:
                        self._current_profile.chats[message['from']] = []
                    self._current_profile.chats[message['from']].append(new_dm)
                    if entry['from'] == self.current_recipient:
                        self.load_messages()
                self._current_profile.save_profile(self._profile_filename)
        
        self.after(2000,self.check_msg)

    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked.
        """
        self.root.destroy()

    def edit_profile(self):
        """
        Creates the edit window
        """
        if self._is_loaded:
            edit_window = EditWindow(self, self._current_profile)
            edit_window.grab_set()

    def edit_bio(self):
        """
        Creates the new bio window
        """
        if self._is_loaded:
            bio_window = BioWindow(self, self._current_profile)
            bio_window.grab_set()

    def add_recipient(self):
        """
        Creates the new add recipient window
        """
        if self._is_loaded:
            add_window = AddWindow(self, self._current_profile)
            add_window.grab_set()

    def send_dm(self):
        """
        Sends a new message to the recipient
        """
        if self._is_loaded:
            message = self.body.get_text_message()

            self.ds.send(message, self.current_recipient)
            self.body.display.configure(state = "normal")
            self.body.add_text_message(f"{self._current_profile.username}: {self.body.get_text_message()}\n\n")
            self.body.display.configure(state = "disabled")

            #save to profile
            dms = DirectMessage(self.current_recipient, message, time.time())
            try:
                self._current_profile.add_dm(self._current_profile.username, dms)
            except RecipientNotFound as e:
                print(e, "Recipient not found")
            self._current_profile.save_profile(self._profile_filename)
            #resets message editor
            self.body.message_editor.delete('1.0', 'end')

    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        #create new menu bar
        menu_settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_settings, label = 'Settings')

        #edit username and password menu
        menu_settings.add_command(label='Edit User Data', command=self.edit_profile)

        #edit bio menu
        menu_settings.add_command(label='Edit Bio', command=self.edit_bio)

        #add a user to chat list
        menu_settings.add_command(label = "Add User", command = self.add_recipient)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile, self)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, save_callback=self.send_dm)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
