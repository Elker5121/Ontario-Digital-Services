all_menus = [] # stores everu menu for easu access
all_stored_users = [] # a reference to every stored user in stored_data.json
is_user_logged_in = False # tells the program how to act based on if the user is logged in or not

user_data = dict(set=False, first_name=None, last_name=None, dob=None, sin=None) # stores all user related data
driver_license_data = dict(set=False, address=None, license_class=None, phone=None) # stores all drivers license related data
license_plate_data = dict(set=False, make=None, model=None, year=None, colour=None, number=None) # stores all license plate related data
health_card_data = dict(set=False, address=None, phone_number=None, number=None, version_code=None) # stores all health card related data
