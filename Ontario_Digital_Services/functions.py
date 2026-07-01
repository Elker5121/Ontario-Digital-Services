import json
from datetime import date
import classes
import data
import random
import config

def show_menu(id):
  '''
    A function that takes in a menu id, and shows the respective menu with the id and closes all others
  '''
  for menu in data.all_menus:
    if menu.id == id:
      menu.show()
    else:
      menu.hide()

def generate_random_number(digits):
  '''
    A function that generates a random digits long number
  '''
  final_number = ''
  for i in range(digits):
    final_number += str(random.randint(0, 9)) # add a random number from 1-9 to the final_number
  return final_number

def generate_random_letters(amount):
  '''
    A function that generates a random string of letter as large as the inputted amount
  '''
  final_letters = ''
  for i in range(amount):
    final_letters += config.LETTERS[random.randint(0, len(config.LETTERS) - 1)] # add a random number from the config.LETTERS list to final_letters
  return final_letters

def get_license_plate_number():
  '''
    A function that generates a random license plate
    Uses generate_random_letters and generate_randon_numbers
  '''
  letters = generate_random_letters(3)
  numbers = generate_random_number(4)
  final_number = f"{letters}-{numbers}" # format the license plate number
  return final_number

# Age
def get_current_year():
  '''
    A function that gets the last 2 digits of the current year (2026 -> 26)
  '''
  year = str(date.today().year)
  current_year = int(year[2:]) # slide the last 2 digits
  return current_year

def get_user_age(birth_date):
  '''
    A function that gets the age of the current user if their dob number was in the correct format (YY/MM/DD)
  '''
  user_birth_year = int(birth_date[:2]) # slide the first 2 digits
  current_year = get_current_year()
  user_age = abs(user_birth_year - current_year) # get the distance of the current year ans user age
  return user_age

def user_of_age(birth_date, target_age):
  '''
    A function that finds out if the user is older than the target_age (returns True if yes)
  '''
  user_age = get_user_age(birth_date)
  return user_age >= target_age

def get_expiry_date(birth_date, expire_time):
  '''
    A function that gets a date expire_time years after the current year
  '''
  user_birth_year = data.user_data['dob']
  return f"{int(get_current_year()) + expire_time}{user_birth_year[2:]}" # format the final date using the user's birthday
                                                    
# Saving
def save():
  '''
    A function that saves all inputted data into the stored_data.json file
  '''
  def is_new_user(user_sin):
    '''
      A function that finds out if the current user has an account or not
    '''
    if len(data.all_stored_users) > 0: # if there are stored users
      for user in data.all_stored_users:
        if user_sin == user['user_data']['sin']: # if the user sin is found in the stored users
          return False
    return True # if the sin number is never found
          
  data_to_save = [] # a container to store all the data to save
  all_current_user_data = dict(user_data=data.user_data, drivers_license=data.driver_license_data, license_plate=data.license_plate_data, health_card=data.health_card_data) # a dictionary compiling all of the current data the user has inputted so far
  is_new_user = is_new_user(data.user_data['sin'])
  
  with open('stored_data.json', 'w') as f: # writes to the stored_data.json file
    if is_new_user:
      if len(data.all_stored_users) < 0: # if the user is new and the first in storage
        data_to_save = all_current_user_data # save the current data directly to create the template for retrieving data
      else: # if there is already data in storage
        data_to_save.append(all_current_user_data) # add the current user data to the data to save
        data_to_save.extend(data.all_stored_users) # extend all of the already stored data in data to save
    else:
      for i in range(len(data.all_stored_users)): # cycle through all the stored use to find the current user
        if data.all_stored_users[i]['user_data']['sin'] == data.user_data['sin']: # if the current user is found
          data.all_stored_users[i] = all_current_user_data # override the old user data with the current one
          data_to_save = data.all_stored_users # update the data to save to the overridden data
          
    json.dump(data_to_save, f, indent=4) # store the data to save

def load_users():
  '''
    A function that returns the stored users in the stored_data.json file
  '''
  with open('stored_data.json', 'r') as f: # read the stored_data.json file
    stored_users = json.load(f) # retrieve and store the data
    return stored_users # return the data

def set_current_user(user_sin):
  '''
    A function to override the current program instance data with the stored data with the user_sin
  '''
  for user in data.all_stored_users:
    if user['user_data']['sin'] == user_sin: # if the found sin is the current sin inputted in the LoginMenu entry widget
      data.is_user_logged_in = True # tell the program the user has logged in
      # override the data (use dict.update() insead of an equal sign to preserve the data instance so the classes write to them still)
      data.user_data.update(user['user_data'])
      data.driver_license_data.update(user['drivers_license'])
      data.license_plate_data.update(user['license_plate'])
      data.health_card_data.update(user['health_card'])

def does_user_exist(user_sin):
  '''
    Finds out if the user with the inputted sin is stored
  '''
  for user in data.all_stored_users:
    if user_sin == user['user_data']['sin']:
      return True
  return False

      





    