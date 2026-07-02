import tkinter as tk
import random
import functions
import data
import config

# Menus
class Menu():
  '''
    A parent class for all of the menus
    Every instance is created in the data.all_menus array and can be displayed using functions.show_menu(id)
  '''
  def __init__(self, root, id, name):
    self.frame = tk.Frame(root, bg = config.BACKGROUND_COLOUR, width=1280, height=800)
    self.id = id
    self.__header_frame = tk.Frame(self.frame)
    self.__header_label = tk.Label(self.__header_frame, text = name, font = config.MENU_NAME_FONT, bg = config.MENU_HEADER_COLOUR, width=100, height=2) # makes the header text

    self.frame.pack_propagate(False)
    self.__header_frame.pack(side=tk.TOP, pady=(0, 15))
    self.__header_label.pack(side=tk.TOP)

  # used to show and hide the menu when needed
  def show(self):
    self.frame.pack()
  def hide(self):
    self.frame.pack_forget()

class ServiceMenu(Menu):
  '''
    The menus used for all input storage
    Takes in an external dictionary to write their Input Field data to
    Has return, submit, and renew buttons. The return button menu is set through the return_id parameter
  '''
  def __init__(self, root, id, return_id, service_dictionary, name):
    super().__init__(root, id, name)
    self.input_field_frame = tk.Frame(self.frame, bg = config.BACKGROUND_COLOUR)
    self.result_frame = tk.Frame(self.frame, bg = config.BACKGROUND_COLOUR)
    self.__button_frame = tk.Frame(self.frame, bg = config.BACKGROUND_COLOUR)
    self.all_fields = [] # stores all of the created Input Fields for easy bulk access
    self.service_dictionary = service_dictionary # store a reference to the external data dictionary

    # create the buttons and labels
    self.__error_label = tk.Label(self.input_field_frame, fg = config.TEXT_INVALID_COLOUR, highlightbackground = config.TEXT_INVALID_COLOUR, highlightthickness = 1)
    self.__return_button = tk.Button(self.__button_frame, text = 'Return', command = lambda : functions.show_menu(return_id), **config.BUTTON_VISUALS)
    self.__submit_button = tk.Button(self.__button_frame, text = 'Submit', command = self.__submit, **config.BUTTON_VISUALS)
    self.__renew_button = tk.Button(self.__button_frame, text = 'Renew', command = self.on_renew, **config.BUTTON_VISUALS)

    # pack the buttons and lables so they show up
    self.__button_frame.pack(side=tk.BOTTOM)
    self.__return_button.pack(side=tk.LEFT)
    self.__submit_button.pack(side=tk.LEFT)

  def __submit(self):
    '''
      A private function called by __submit_button
      Verifies the input fields have been filled before calling the on_submit function, which can be modified by child classes
    '''
    all_fields_stored = True # automatically assume all fields have been entered
    for field in self.all_fields:
      field.store_value() # stores the value inputted to the field's respective service dictionary
      if not field.value_is_set:
        field.change_colour(config.TEXT_INVALID_COLOUR) # change the text to the invalid colour
        all_fields_stored = False # if a single field is empty, tell the program that it cannot be submitted
      else:
        field.change_colour(config.TEXT_VALID_COLOUR) # change the text to the valid colour

    if all_fields_stored == False:
      return

    self.on_submit() # call the function that can be modified by the child classes
  
  def on_submit(self):
    '''
      A function used by ServiceMenu child classes to dictact what they do on submission
      Usually called last when overridden, so the values are not saved prematurley
    '''
    self.service_dictionary['set'] = True # tells the menu to act like the user has submitted their values
    self.input_field_frame.pack_forget() # get rid of the Input Fields
    self.__submit_button.pack_forget() # get rid of the submit buttom
    self.result_frame.pack(side=tk.TOP) # show the result of the inputs
    self.__renew_button.pack(side=tk.LEFT) # allow the user to renew the result
    self.__return_button.pack(side=tk.LEFT) # make sure the return button is showing (if the user has submitted through renewing)
    functions.save() # save all of the data

  def on_renew(self):
    '''
      The function called by the __renew_button
      Determines what the menu does when the user wants to renew it
    '''
    self.service_dictionary['set'] = False # allow automatic values to reset and let the menu to act like the user hasn't entered anything yet
    self.result_frame.pack_forget() # get rid of the result frame
    self.__renew_button.pack_forget() # get rid of the renew button
    self.__return_button.pack_forget() # get rid of the return button to force the user to override the values (stops odd behaviour)
    self.__submit_button.pack(side=tk.LEFT) # show the submit button
    self.input_field_frame.pack(side=tk.TOP) # show the Input Fields
    for field in self.all_fields:
      field.input_entry.delete(0, tk.END) # empty all the entry widgets from the previous input

  def show(self):
    '''
      A function used to show the service menu
      Runs any code that needs to go before a service is shown
    '''
    if data.is_user_logged_in and self.service_dictionary['set']: # if the user has data
      self.__submit_button.pack_forget() # don't show the submit button
      self.input_field_frame.pack_forget() # don't show the input fields
      self.on_submit() # submit all of the stored data in the data.py file so the menu shows the result
    else: # if the user is new or hasn't applyed for the service yet
      self.__renew_button.pack_forget() # get rid the of renew button
      self.input_field_frame.pack(side=tk.TOP) # show the input field
    super().show() # run the base function

  def show_error(self, message):
    '''
      A function used to log an error to the user
      Takes in a message, than presents it
    '''
    self.__error_label.config(text = message)
    self.__error_label.pack(side=tk.TOP, padx = 20, pady = 20) # give the error padding for extra impact
  def hide_error(self):
    '''
      Simply gets rid of the error message
    '''
    self.__error_label.pack_forget()
    
  def create_input_field(self, header_text, description_text, value_key):
    '''
      A function to create the input fields of the service menu
    '''
    new_input_field = InputField(self.input_field_frame, header_text, description_text, self.service_dictionary, value_key)
    self.all_fields.append(new_input_field) # add the field to the all_fields list for easy modification
    return new_input_field

class HomeMenu(Menu):
  def __init__(self, root, id, name):
    super().__init__(root, id, name)
    self.__desc_label = tk.Label(self.frame, text = 'This is the Home Menu.\nYou can apply for, renew, or view all of your information here.', font = config.MENU_DESC_FONT, bg = config.LABEL_BG_COLOUR )
    self.__drivers_license_label = tk.Label(self.frame, text = 'If you wish to apply for a Drivers License, or view your current one, click here.', bg = config.LABEL_BG_COLOUR )
    self.__drivers_license_button = tk.Button(self.frame, text = 'Drivers License', command = lambda : functions.show_menu('drivers_license'), **config.BUTTON_VISUALS, width=15, height=2)

    self.__license_plate_label = tk.Label(self.frame, text = 'If you wish to apply for a License Plate, or view your current one, click here.', bg = config.LABEL_BG_COLOUR )
    self.__license_plate_button = tk.Button(self.frame, text = 'License Plate', command = lambda : functions.show_menu('license_plate'), **config.BUTTON_VISUALS, width=15, height=2)
    
    self.__health_card_label = tk.Label(self.frame, text = 'If you wish to apply for a Health Card, or view your current one, click here.', bg = config.LABEL_BG_COLOUR )
    self.__health_card_button = tk.Button(self.frame, text = 'Health Card', command = lambda : functions.show_menu('health_card'), **config.BUTTON_VISUALS, width=15, height=2)

    self.__drivers_license_button.pack_propagate(False)
    self.__license_plate_button.pack_propagate(False)
    self.__health_card_button.pack_propagate(False)
    
    self.__desc_label.pack(side=tk.TOP)
    self.__drivers_license_label.pack(side=tk.TOP, pady = (30, 0))
    self.__drivers_license_button.pack(side=tk.TOP, pady = (0, 10))
    self.__license_plate_label.pack(side=tk.TOP, pady = (30, 0))
    self.__license_plate_button.pack(side=tk.TOP, pady = (0, 10))
    self.__health_card_label.pack(side=tk.TOP, pady = (30, 0))
    self.__health_card_button.pack(side=tk.TOP, pady = (0, 10))

class StartMenu(Menu):
  '''
    The menu shown to the user on start
    Allows the user to apply to ServiceOntario, or Login to their account
  '''
  def __init__(self, root, id, name):
    super().__init__(root, id, name)
    self.__header_label = tk.Label(self.frame, text = 'Welcome to Ontario Digital Services! \n\nApply if you do not have an account. \nLogin if you do have an account.', font = config.MENU_DESC_FONT, bg = config.LABEL_BG_COLOUR, width=50, height=5) # gives instructions to the user
    self.__button_frame = tk.Frame(self.frame)
    self.__apply_button = tk.Button(self.__button_frame, text = 'Apply',  width=20, height=3, command = lambda : functions.show_menu('apply'), **config.BUTTON_VISUALS)
    self.__login_button = tk.Button(self.__button_frame, text = 'Login', width=20, height=3, command = lambda : functions.show_menu('login'), **config.BUTTON_VISUALS)

    # make sure the buttons don't change sizes
    self.__header_label.pack_propagate(False)
    self.__apply_button.pack_propagate(False)
    self.__login_button.pack_propagate(False)
    
    self.__header_label.pack(side=tk.TOP, pady=(50, 5))
    self.__button_frame.pack() # make sure the buttons are below the header
    # pack the buttons side-by-side
    self.__apply_button.pack(side=tk.LEFT)
    self.__login_button.pack(side=tk.LEFT)

# Service Menus
class ApplyMenu(ServiceMenu):
  '''
    The menu used to allow the user to apply to ServiceOntario online services
    Stores the user's name, birthday, dob number, and sin number
  '''
  def __init__(self, root, id, return_id, service_dictionary, name):
     super().__init__(root, id, return_id, service_dictionary, name)
     self.__first_name_field = self.create_input_field('Enter First Name', '', 'first_name')
     self.__last_name_field = self.create_input_field('Enter Last Name', '', 'last_name')    
     self.__birth_date_field = self.create_input_field('Enter Birthday', 'Formatted as: YY/MM/DD', 'dob')     
     self.__sin_number_field = self.create_input_field('Enter SIN Number', '', 'sin')
  
  def on_submit(self):
    '''
     Checks to make sure the user's sin number is unique before submitting
    '''
    if functions.does_user_exist(data.user_data['sin']): # if the sin number already exists
      for field in self.all_fields:
        field.change_colour(config.TEXT_INVALID_COLOUR) # change all fields to the invalid colour
      self.show_error('That SIN already exists.') # log the error
    else:
      for field in self.all_fields:
        field.change_colour(config.TEXT_VALID_COLOUR) # reset all of the field colours
        
      self.hide_error() # get rid of the error
      data.is_user_logged_in = True # helps the program know the user is logged in
      super().on_submit() # save the application data
      functions.show_menu('home') # open the home menu

class LoginMenu(ServiceMenu):
  '''
    The menu that allows the user to login to a stored account
  '''
  def __init__(self, root, id, return_id, service_dictionary, name):
   super().__init__(root, id, return_id, service_dictionary, name)
   self.sin_number_field = self.create_input_field('Enter SIN Number', '', 'sin')
    
  def on_submit(self):
    '''
      Tries to find and retrieve a user of the inputted sin number
    '''
    if len(data.all_stored_users) <= 0: # if there are no users stored
      self.show_error('No Users In Database') # log the error
      return

    for user in data.all_stored_users:
      current_sin = user['user_data']['sin']
      if current_sin == self.sin_number_field.input_entry.get(): # if the sin being checked is the sin entered
        functions.set_current_user(current_sin) # override the data in the data.py file with the found sin data
        self.hide_error() # get rid of an error if there was one
        functions.show_menu('home') # go to the home menu
        
    if data.is_user_logged_in == False: # if the user was not logged in, but there are users stored
      self.show_error('That SIN Does Not Exist.') # log the error
      
class DriversLicenseMenu(ServiceMenu):
  '''
    The menu used to input data about and create a drivers license
  '''
  def __init__(self, root, id, return_id, service_dictionary, name):
    super().__init__(root, id, return_id, service_dictionary, name)
    # the address and phone field should technically be in the ApplyMenu
    self.address_field = self.create_input_field('Enter Address', '', 'address')
    self.class_field = self.create_input_field('Enter Class', '', 'license_class')
    self.phone_number_field = self.create_input_field('Enter Phone Number', '', 'phone')
    self.drivers_license = DriversLicense(self.result_frame) # create an empty drivers license
     
  def on_submit(self):
    '''
     Verifies the user is old enough to apply for a license, generally 16 years old
     Updates and shows the DriversLicense
    '''
    if functions.user_of_age(data.user_data['dob'], 16): # if the user is older than 16
      super().on_submit() # save the data
      self.drivers_license.update() # set the drivers license using the saved data
      self.drivers_license.show() # show the license
      self.hide_error()
    else: # if the user is younger than 16
      self.show_error('User Is Too Young.') # log the error and do not save

class HealthCardMenu(ServiceMenu):
  '''
    The menu used to input health card data and create the health card
  '''
  def __init__(self, root, id, return_id, service_dictionary, name):
   super().__init__(root, id, return_id, service_dictionary, name)
   # these fields are more for something to add to the menu, these should technically be in the ApplyMenu
   self.address_field = self.create_input_field('Enter Address', '', 'address')
   self.phone_number_field = self.create_input_field('Enter Phone Number', '', 'phone_number')
   self.__health_card = HealthCard(self.result_frame) # create an empty health card
     
  def on_submit(self):
    '''
      Verifies the user has a stored driver's licnese for security verification
      Updates and shows the HealthCard
    '''
    if not data.driver_license_data['set']: # if the user does not have a stored license
      self.show_error('Must Have A Drivers License.') # log the error
      return # don't continue
    else:
      if not data.health_card_data['set']: # generate automatic values if the card is not yet set
        data.health_card_data['number'] = functions.generate_random_number(10)
        data.health_card_data['version_code'] = functions.generate_random_letters(2)
      self.hide_error()
      self.__health_card.update() # set the health card using the data in the data.py file
      self.__health_card.show() # show the card
    super().on_submit() # save the data

class LicensePlateMenu(ServiceMenu):
  '''
    The menu used to input data and create a license plate
  '''
  def __init__(self, root, id, return_id, service_dictionary, name):
     super().__init__(root, id, return_id, service_dictionary, name)
     self.__vehicle_make_field = self.create_input_field('Enter The Make Of Your Vehicle', '', 'make')
     self.__vehicle_model_field = self.create_input_field('Enter The Model Of Your Vehicle', '', 'model')
     self.__vehicle_year_field = self.create_input_field('Enter The Year Of Your Vehicle', '', 'year')
     self.__vehicle_colour_field = self.create_input_field('Enter The Colour Of Your Vehicle', '', 'colour')
     self.__license_plate = LicensePlate(self.result_frame) # create an empty license plate
  
  def on_submit(self):
    '''
      Verifies the user is old enough to apply for a license plate
      Updates and shows the LicensePlate 
    '''
    if functions.user_of_age(data.user_data['dob'], 16): # if the user is old enough, at least 16
      if not data.license_plate_data['set']: # generate the automatic values when submitted
        data.license_plate_data['number'] = functions.get_license_plate_number()
      self.__license_plate.update() # update the license plate from the data.py file
      self.__license_plate.show() # show the license plate
      self.hide_error() # hide any error
      super().on_submit() # save the submited data
    else: # if the user is too young
      self.show_error('User Is Too Young.')
  
# Input Fields
class InputField():
  '''
    A class used to make an input field template
    Takes in an external dictionary and key to modify using the entered value
  '''
  def __init__(self, root, header_text, descriptions_text, service_dictionary, value_key):
    self.field_frame = tk.Frame(root, bg = config.LABEL_BG_COLOUR)
    self.service_dictionary = service_dictionary # store a reference to the external dictionary
    self.value_is_set = False # default to not set
    self.__key = value_key # store the key

    # make the visuals
    self.__header_label = tk.Label(self.field_frame, text = header_text, font = config.INPUT_FIELD_HEADER_FONT, bg = config.LABEL_BG_COLOUR)
    self.__description_label = tk.Label(self.field_frame, text = descriptions_text, font = config.INPUT_FIELD_DESC_FONT, bg = config.LABEL_BG_COLOUR)
    self.input_entry = tk.Entry(self.field_frame, font = config.INPUT_FIELD_TEXT_FONT, width = 25)

    self.__header_label.pack(side=tk.TOP, anchor='w', pady=config.INPUT_FIELD_YPADDING) # add padding for better looks
    if self.__description_label['text']: # if the description has text, show it
      self.__description_label.pack(side=tk.TOP, anchor='w')
    self.input_entry.pack(side=tk.TOP)
    self.field_frame.pack(side=tk.TOP)

  def store_value(self):
    '''
      A function used to set the external dictionary, at the set key, to the entered value in the entry widget
    '''
    self.value_is_set = self.input_entry.get() != '' # make sure the widget has a value in it
    self.service_dictionary[self.__key] = self.input_entry.get() # set the external dictionary at the chosen value to the entry set value

  def change_colour(self, colour):
    '''
      A function used to change the colour of the header (usually due to errors)
    '''
    self.__header_label.config(fg = colour)
    
# Results
class Result():
  '''
    A base class for the menu results
  '''
  def __init__(self):
    self.update()

  def update(self):
    pass

class LicensePlate(Result):
  '''
    The visual license plate
  '''
  def __init__(self, root):
    self.__frame = tk.Frame(root, highlightbackground='black', highlightthickness=2, bg = config.LICENSE_PLATE_BG_COLOUR) # make the frame defined with background
    self.__plate_number_label = tk.Label(self.__frame, font = config.LICENCE_PLATE_FONT, bg = config.LICENSE_PLATE_BG_COLOUR)
    self.__plate_number_label.pack()
    
    super().__init__() # calls update

  def update(self):
    # set the label text to the license_plate_data in the data.py file
    self.__plate_number_label.config(text = data.license_plate_data['number'])

  # shows and hides the licence plate
  def show(self):
    self.__frame.pack()
  def hide(self):
    self._frame.pack_forget()

class DriversLicense(Result):
  '''
    The visual drivers license
  '''
  def __init__(self, root):
    self.__drivers_license_frame = tk.Frame(root, highlightbackground='black', highlightthickness=2, width=450, height=250, bg = config.DRIVERS_LICENSE_BG_COLOUR) # create the main frame at a fixed size
    self.__header_frame = tk.Frame(self.__drivers_license_frame) # creates a header frame
    self.__side_detail_frame = tk.Frame(self.__drivers_license_frame, bg = 'green', width=150, height=175) # a frame used for extra detail / a placeholder where the user's image would be

    # create all of the labels
    self.__header_label = tk.Label(self.__header_frame, text='Ontario Drivers License', font = ('Ariel', 20, 'bold'), bg = config.DRIVERS_LICENSE_BG_COLOUR)
    self.__first_name_label = tk.Label(self.__drivers_license_frame, font = ('Ariel', 12), bg = config.DRIVERS_LICENSE_BG_COLOUR)
    self.__last_name_label = tk.Label(self.__drivers_license_frame, font = ('Ariel', 12), bg = config.DRIVERS_LICENSE_BG_COLOUR)
    self.__address_label = tk.Label(self.__drivers_license_frame, font = ('Ariel', 8), bg = config.DRIVERS_LICENSE_BG_COLOUR)
    self.__dob_label = tk.Label(self.__drivers_license_frame, font = ('Ariel', 12), bg = config.DRIVERS_LICENSE_BG_COLOUR)
    self.__class_label = tk.Label(self.__drivers_license_frame, font = ('Ariel', 10), bg = config.DRIVERS_LICENSE_BG_COLOUR)
    self.__expiry_date_label = tk.Label(self.__drivers_license_frame, font = ('Ariel', 10), bg = config.DRIVERS_LICENSE_BG_COLOUR)

    self.__drivers_license_frame.pack_propagate(False) # make sure the main frame cannot resize
    # place all of the frames and labels
    self.__side_detail_frame.place(relx=0.1, rely=0.25)
    self.__header_frame.place(relx=0.15, rely=0)

    self.__header_label.pack()
    self.__expiry_date_label.place(relx=0.5, rely=0.25)
    self.__last_name_label.place(relx=0.5, rely=0.35)
    self.__first_name_label.place(relx=0.5, rely=0.45)
    self.__address_label.place(relx=0.5, rely=0.55)
    self.__dob_label.place(relx=0.5, rely=0.65)
    self.__class_label.place(relx=0.5, rely=0.75)
    super().__init__() # call the update function
    
  def update(self):
    # set each label's value to it's respective stored data
    self.__last_name_label.config(text = f"LN {data.user_data['last_name']}")
    self.__first_name_label.config(text = f"FN {data.user_data['first_name']}")
    self.__address_label.config(text = f"ADDRESS {data.driver_license_data['address']}")
    self.__dob_label.config(text = f"DOB {data.user_data['dob']}")
    self.__class_label.config(text = f"CLASS {data.driver_license_data['license_class']}")
    if data.user_data['dob'] != None: # this requires a None check for some reason
      self.__expiry_date_label.config(text = f"EXP {functions.get_expiry_date(data.user_data['dob'], 5)}")

  # functions that can show and hide the drivers license
  def show(self):
    self.__drivers_license_frame.pack()
  def hide(self):
    self.__drivers_license_frame.pack_forget()

class HealthCard(Result):
  '''
    The visual health card
  '''
  def __init__(self, root):
    self.__health_card_frame = tk.Frame(root, highlightbackground='black', highlightthickness=2, width=450, height=250, bg = config.HEALTH_CARD_BG_COLOUR) # create the main frame at a set size
    self.__header_frame = tk.Frame(self.__health_card_frame)
    self.__side_detail_frame = tk.Frame(self.__health_card_frame, bg = 'blue', width=150, height=175) # a frame acting as a placeholder for the user image

    # make the labels
    self.__header_label = tk.Label(self.__header_frame, text = 'Ontario Health Card', font = ('Ariel', 20, 'bold'), bg = config.HEALTH_CARD_BG_COLOUR)
    self.__health_card_number_label = tk.Label(self.__health_card_frame, font = ('Ariel', 15), bg = config.HEALTH_CARD_BG_COLOUR)
    self.__name_label = tk.Label(self.__health_card_frame, font = ('Ariel', 15), bg = config.HEALTH_CARD_BG_COLOUR)
    self.__birth_date_label = tk.Label(self.__health_card_frame, font = ('Ariel', 10), bg = config.HEALTH_CARD_BG_COLOUR)
    self.__expiry_date_label = tk.Label(self.__health_card_frame, font = ('Ariel', 10), bg = config.HEALTH_CARD_BG_COLOUR)

    # place the frames and labels
    self.__header_frame.place(relx=0.2, rely=0)
    self.__side_detail_frame.place(relx=0.1, rely=0.25)

    self.__header_label.pack()
    self.__name_label.place(relx=0.5, rely=0.3)
    self.__health_card_number_label.place(relx=0.5, rely=0.4)
    self.__birth_date_label.place(relx=0.5, rely=0.6)
    self.__expiry_date_label.place(relx=0.75, rely=0.6)
    
    super().__init__() # update the health card
    
  def update(self):
    # set each label's value to it's respective stored data
    self.__name_label.config(text = f"{data.user_data['first_name']} {data.user_data['last_name']}")
    self.__health_card_number_label.config(text = f"{data.health_card_data['number']}-{data.health_card_data['version_code']}")
    self.__birth_date_label.config(text = f"BORN\n{data.user_data['dob']}")
    if data.user_data['dob'] != None: # this needs a None check for some reason
      self.__expiry_date_label.config(text = f"EXP\n{functions.get_expiry_date(data.user_data['dob'], 5)}")

  # functions that can show and hide the drivers license
  def show(self):
    self.__health_card_frame.pack()
  def hide(self):
    self.__health_card_frame.pack_forget()