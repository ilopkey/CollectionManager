import os
from DEFAULTS import *

# Returns a list of all current collection paths stored
def view_collections():
    # List all current collections
    collections = open(collection_list_path, 'r')
    raw_collection_list = collections.readlines()
    collections.close()

    list = []

    # Every entry takes up 3 lines with the second line containing the name
    # of the collection, so 2, 5, 8 etc... are the lines we need.
    # Get the number of lines and divide by 3
    # Then we need 1 = 2, 2 = 5, 3 = 8, 4 = 11, 5 = 14. 
    # n = 2n + n-1
    for i in range(0, int( len(raw_collection_list) / 3) ):
        x = (i+1) * 2 + i
        list.append(raw_collection_list[x-1])
    
    return list

# When passed a list containing collection paths will print
# out the name of the collections
def print_collections(list):
    for i in range(1, len(list)+1):
            x = len(list[i-1])
            print('%i: '  % i + list[i-1][:x-5])

# User input handling to ensure that a collection choice is 
# a valid integer choice from the given list.
def int_choice_input(list=[]):
    # Loop to ensure that the option selected is valid
    while True:
            try:
                int_choice = int(input('Enter option: '))
            except ValueError:
                print(error_text['not_int'])
                continue
            
            if list != [] and int_choice > len(list):
                print(error_text['invalid'])
                continue
            else:
                break
    return int_choice

# Get the list of fields stored in the given collection file
def get_fields(collection_path):
   
    # Get the first line stored in the collection
    file = open(collection_path, 'r')
    fields = file.readline()
    file.close()
    
    # Remove the newline char
    fields = fields[:len(fields)-1]
    
    # Return a list of the fields
    return fields.split(',')
    
# Get the list of all items stored in the give colleciton file
def get_items(collection_path, num_of_fields):
    
    # Get the data from the collection file
    file = open(collection_path, 'r')
    collection_contents = file.readlines()
    file.close()
    
    current_item = []
    all_items = []
    
   # From collection_contents get the fields split by the connection
    
    for i in collection_contents:
    
        if i == collection_contents[0]:
            continue
           
        else:
            # Create a list for all fields of an item
            # Then add that list to a list of all items
            current_item.append(i[:len(i)-1])
            
            if len(current_item) == num_of_fields:
                all_items.append(current_item)
                current_item = []
                
    return all_items
    
# Print out the items from a collection, 2nd input determines 
# if it has the # border or is numbered
def print_items(collection_path):

    # Get the Fields and Items from the collection
    fields = get_fields(collection_path)
    items = get_items(collection_path, len(fields))
    
    # A list to store the longest length of a value in every given field
    field_char_len = []
    
    # Set the initial longest length to the length of the field names
    for field in fields:
        field_char_len.append(len(field))
    
    # Loop through each fields of every item to find the longest length used
    # in each field
    for i in range(0,len(fields)):
        for item in items:
            if len(item[i]) > field_char_len[i]:
                field_char_len[i] = len(item[i])
    
    # Print a line of # at the start of the collection
    for i in field_char_len:
        print('#' * (i + 3), end = '')
    print('#\n', end = '')
    
    # Print out the fields using the length predetermined
    for i in range(0,len(fields)):
        remaining = field_char_len[i] - len(fields[i])
        
        if i == 0:
            print('# ' + fields[i], end='')
        else:
            print(fields[i], end='')
        
        if i != len(fields)-1:
            print(' ' * remaining, end = ' # ')
        else:
            print(' ' * remaining, end = ' #')
            
    print()
    
    # Leave a line of # between the fields and the items
    for i in field_char_len:
        print('#' * (i + 3), end = '')
    print('#\n', end = '')
    
    # Print out the items using the same length
    for item in items:
        for i in range(0,len(fields)):
            remaining = field_char_len[i] - len(item[i])
            
            if i == 0:
                print('# ' + item[i], end='')
            else:
                print(item[i], end='')
            
            if i != len(item)-1:
                print(' ' * remaining, end = ' # ')
            else:
                print(' ' * remaining, end = ' #')
        print()
    
    # Print a line of # at the end of the collection
    for i in field_char_len:
        print('#' * (i + 3), end = '')
    print('#\n', end = '')
    
    print('\n')


# Begin by checking if collection_list already exists
# If it exists display a welcome message
# Otherwise create the file then display a welcome message
if os.path.exists(collection_list_path):
    print(welcome_text[0])
else:
    collections = open(collection_list_path, 'w')
    collections.close()
    print(welcome_text[1])
print()

# Set the Control Loop options, should be obvious
exit = 0
option = 0

# Control Loop
while exit == 0:
    #  Option Entry
    print('Please select an option:\n')
    for i in mloop_options:
        print(i)
    option = int_choice_input()
    
    # Exit Program Option
    if option == 9:
        # Exit the program, also give option for user to continue using
        # collection manager
        x = input(exit_text)
        if len(x) != 0:
            continue
        exit = 1
    
    # Create New Collection
    elif option == 1:
        # Get name for new collection
        print(create_collection['name_entry'])
        collection_name = input(general_input['name'])
        collection_path = collection_name + '.txt'
        
        # Check if the new collection already exists
        if os.path.exists(collection_path):
            print(error_text['already_exists'])
            continue
        
        # Get a list of fields for the collection
        fields = []
        print(create_collection['field_entry'])
        while True:
            field = input(general_input['field'])
            
            # Handle exiting the field entry. If there are no fields then force
            # user to enter at least one field.
            try:
                if int(field) == 0:
                    if fields == []:
                        print(error_text['no_fields'])
                        continue
                    else:
                        break
            except ValueError:
                fields.append(field)
                print(create_collection['field_added'] % (field, collection_name))
       
        # Create a file to store the new collection
        new_collection = open(collection_path, 'w')
        
        # Store the fields inputted onto the first line of the collection file
        field_text = ''
        for field in fields:
            # Separate the fields by a comma
            if field == fields[len(fields) - 1]:
                field_text += field + '\n'
            else:
                field_text += field + ','
        
        # Write the fields to the top line and then close the new collection
        new_collection.write(field_text)
        new_collection.close()
        
        # Get the current number of collections as a string
        list = view_collections()
        collection_id = str(len(list))
        
        # Create a collection_id of format @C0000
        while len(collection_id) < 4:
            collection_id = '0' + collection_id
        collection_id = '@C' + collection_id
        
        # Update the collections_list with the new collection
        collections = open(collection_list_path, 'a')
        collections.write(collection_id + '\n' + collection_path + '\n\n')
        collections.close()
        print(create_collection['created'] + collection_name + '\n')
    
    # Add item to collection
    elif option == 2:
        
        list = view_collections()
        
        # Now we have a list of all the paths we need
        # If there are no current collections then return to main menu
        if len(list) == 0:
            print(error_text['no_collections'])
            continue
        
        # Print out the names and ask which collection the item will be added too
        print(add_item['collection_entry'])
        print_collections(list)
        
        # User Input handling
        collection_choice = int_choice_input(list)
        collection_choice -= 1
        
        # Open the chosen collection to get the fields used in the collection
        collection_path = list[collection_choice]
        collection = open(collection_path[:len(collection_path)-1], 'r')

        # Get the list of fields stored in this collection
        field_list = collection.readline()
        # Remove the newline from the field list
        field_list = field_list[:len(field_list)-1]
        # Split via comma into to a list for easier usage
        field_list = field_list.split(',')
        
        # Close the collection file so it can be reopened for appending the file.
        collection.close()
        
        # Get the values for the fields
        item_values = []
        for field in field_list:
            value = input(add_item['field_entry'] % field)
            item_values.append(value)
        
        # Open the chosen collection to append the new item
        collection_path = list[collection_choice]
        collection = open(collection_path[:len(collection_path)-1], 'a')
        
        # Write the item's values to the collection then save the file
        item_text = ''
        for value in item_values:
            item_text += value + '\n'
        collection.write(item_text)
        collection.close()
        
        # Output a success message displaying the value given for 
        # the first field for the item.
        print('%s: %s %s %s.\n' % (field_list[0], item_values[0], add_item['added '], collection_path[:len(collection_path)-5]))
    
    # View a collection
    elif option == 3:
        
        # Get a list of all collection paths, then print out and ask
        # user to select the collection they want to view
        list = view_collections()
        if len(list) == 0:
            print(error_text['no_collections'])
            continue
        print(view_collection['collection_entry'])
        print_collections(list)
        
        # User Input handling
        collection_choice = int_choice_input(list)
        
        # Open the chosen collection
        collection_path = list[collection_choice-1]
        collection_path = collection_path[:len(collection_path)-1]
        
        # Display the name of the collection
        print(view_collection['view_collection'] + collection_path[:len(collection_path)-4])
        
        print_items(collection_path)
        
    # Remove an item from a collection
    elif option == 4:
        list = view_collections()
        
        # Now we have a list of all the paths we need
        # If there are no current collections then return to main menu
        if len(list) == 0:
            print(error_text['no_collections'])
            continue
        
        # Print out the names and ask which collection the item will be removed from
        print(remove_item['collection_entry'])
        print_collections(list)
        
        # Get the collection list
        
        
    else:
        print(error_text['invalid'])
    