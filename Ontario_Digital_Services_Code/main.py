import tkinter as tk
import functions
import classes
import data

root = tk.Tk()
root.geometry('1280x800')
root.title('Ontario Digital Services')

data.all_stored_users = functions.load_users() # store a reference to all of the stored users
# create every menu inside of the data.all_menus list
data.all_menus = [
  classes.StartMenu(root, 'start', 'Ontario Digital Services'),
  classes.LoginMenu(root, 'login', 'start', dict(), 'Login'),
  classes.ApplyMenu(root, 'apply', 'start', data.user_data, 'Apply'),
  classes.HomeMenu(root, 'home', 'Home'),
  classes.LicensePlateMenu(root, 'license_plate', 'home', data.license_plate_data, 'License Plate'),
  classes.DriversLicenseMenu(root, 'drivers_license', 'home', data.driver_license_data, 'Drivers License'),
  classes.HealthCardMenu(root, 'health_card', 'home', data.health_card_data, 'Health Card')
]

functions.show_menu('start') # immidiatly show the start menu
root.mainloop()