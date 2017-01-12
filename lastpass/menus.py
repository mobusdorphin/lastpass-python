import pygtk
import gtk
import lastpass

class lastpassGTK:
    
    def __init__(self):
	items = [('pg-ok', '_LOG IN', 0, 0, None),
		('pg-cancel', '_CANCEL', 0, 0, None),
		('pg-drop', '_Drop', 0, 0, None),]

	# We're too lazy to make our own icons, 
	# so we use regular stock icons.
	aliases = [('pg-ok', gtk.STOCK_OK),
		  ('pg-cancel', gtk.STOCK_CANCEL),
		  ('pg-drop', gtk.STOCK_DELETE),]

	gtk.stock_add(items)
	factory = gtk.IconFactory()
	factory.add_default()
	style= window.get_style()
	for new_stock, alias in aliases:
	    icon_set = style.lookup_icon_set(alias)
	    factory.add(new_stock, icon_set)

	# Create the relabeled buttons
	b_create = gtk.Button(stock='pg-create')
	b_alter = gtk.Button(stock='pg-alter')  
	b_drop = gtk.Button(stock='pg-drop')  
        #print('Creating LastPass GTK menu')
        self.username = ''
        self.password = ''
        self.loggedIn = False
        self.menu = gtk.Menu()
	self.sites_menu = gtk.MenuItem("Sites")
	self.secure_notes_menu = gtk.MenuItem("Secure Notes")
	self.logoff_menu = gtk.MenuItem("Log Off")
	menuList = [self.sites_menu, self.secure_notes_menu, self.logoff_menu]
	for x in menuList:
	  self.menu.append(x)
	  x.show()
	  
	## Create Login frame
	self.loginWindow = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
	self.loginWindow.set_decorated(False)
	self.loginVbox = gtk.VBox(False, 0)
	      
	self.userFrame = gtk.Frame(label='Username')
	self.passFrame = gtk.Frame(label='Password')
        self.loginLabelFrame = gtk.Frame()

	self.loginEntry = gtk.Entry()
	self.userFrame.add(self.loginEntry)
	
	self.passEntry = gtk.Entry()
	self.passEntry.set_visibility(False)
	self.passFrame.add(self.passEntry)
      
	self.loginEntry.connect_object("activate", self.loginClicked, self.loginWindow,
				self.loginEntry, self.passEntry)
	self.passEntry.connect_object("activate", self.loginClicked, self.loginWindow, 
				self.loginEntry, self.passEntry)
      
	self.loginButton = gtk.Button(label="Log In", stock='pg-ok')
	self.loginButton.connect_object("clicked", self.loginClicked, self.loginWindow, 
				self.loginEntry, self.passEntry)
	self.cancelButton = gtk.Button(label="Log In", stock='pg-cancel')
	self.cancelButton.connect_object("clicked", self.cancelClicked, self.loginWindow)
	
	self.loginLabel = gtk.Label("Please log in")
	self.loginLabel.set_line_wrap(True)
	self.loginVbox.pack_start(self.loginLabel, True, True, 0)
	self.loginVbox.pack_start(self.userFrame, True, True, 0)
	self.loginVbox.pack_start(self.passFrame, True, True, 0)
      
	self.loginHbox = gtk.HBox(False, 0)
	self.loginHbox.pack_start(self.loginButton, True, True, 0)
	self.loginHbox.pack_start(self.cancelButton, True, True, 0)
	self.loginWindow.add(self.loginVbox)
	self.loginVbox.add(self.loginHbox)
	
	self.loginButton.show()
	self.cancelButton.show()
	self.loginHbox.show()
	self.loginVbox.show()
	self.loginLabel.show()
	self.loginEntry.show()
	self.passEntry.show()
	self.userFrame.show()
	self.passFrame.show()
	  
    def loginClicked(self, widget, loginEntry, passEntry):
        self.username = loginEntry.get_text()
        self.password = passEntry.get_text()
        self.loggedIn = True
        self.cancelClicked(widget)
      
    def cancelClicked(self, widget):
        widget.hide()
    
    def getLogin(self):
        pass
      
    def showLastpass(self, widget, event):
        print(event)
	if event.type == gtk.gdk.BUTTON_PRESS:
	    try:
	      if self.loggedIn == True:
		vault = lastpass.Vault.open_remote(self.username, self.password)
		self.menu.popup(None, None, None, event.button, event.time)
		return 'lastpass'
	      else:
		raise LastPassUnknownUsernameError
	    except:
	      self.loginWindow.set_position(gtk.WIN_POS_MOUSE)
	      self.loginWindow.show()
        
    
    
if __name__ == '__main__':
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title("LASTPASS")
    window.connect("destroy", lambda wid: gtk.main_quit())
    window.connect("delete_event", lambda a1,a2:gtk.main_quit())
    window.set_border_width(10)
    
    button = gtk.Button()
    #image = gtk.Image()
    #image.set_from_file('/usr/local/share/pixmaps/guake/last_pass.png')
    #button.set_image(image)
    window.add(button)
    
    lastPassMenu = lastpassGTK()
    button.connect("event", lastPassMenu.showLastpass)
  
    button.show()
    window.show()
    
    gtk.main()