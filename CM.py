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
# a valid integer choice from the given list. Also usable
# to check if the input is an interger without requiring a list.
# Also adding possibility of passing a preselected value
# that will be checked before attempting to request a new
# value if the value is invalid.
def int_choice_input(list=[], int_choice = -1):
    # Loop to ensure that the option selected is a 
    # integer valid
    while True:
            if int_choice == -1:
                try:
                    int_choice = int(input(general_input['option']))
                except ValueError:
                    print(error_text['not_int'])
                    continue
            
            # If a list was given then check that the integer
            # does not exceed the length of the list
            # Then set it to -1 before reattempting the loop
            if list != [] and int_choice > len(list):
                print(error_text['invalid'])
                int_choice = -1
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
    
    # Add the Field POS to fields and then add the numerical
    # position, beginning at 1, to each item.
    fields.insert(0, 'POS')
    
    for x in range(0, len(items)):
        items[x].insert(0, str(x+1))
    
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
        if os.path.exists(collection_path) or collection_path == collection_list_path:
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
        
        # Check if there are any items in the collection
        collection = open(collection_path, 'r')
        
        # Display the name of the collection
        print(view_collection['view_collection'] % collection_path[:len(collection_path)-4])
        
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
        
        # User Input handling
        collection_choice = int_choice_input(list)
        
        # Get the collection list
        collection_path = list[collection_choice-1]
        collection_path = collection_path[:len(collection_path)-1]
        
        # Ask if user wants to view the collection before selecting
        # the item
        view = input(remove_item['view_collection'] % collection_path)
        if view.lower() == 'y':
            print_items(collection_path)
        
        # Get the list of items
        fields = get_fields(collection_path)
        items = get_items(collection_path, len(fields))
        
        # Get a list of the items that are to be removed
        # have user enter a non integer to exit
        item_choice = []
        print(remove_item['item_entry'])
        
        while True:
            # Initial input
            choice = input(remove_item['pos_entry'])
            
            # Attempt to convert the choice to an int 
            try:
                choice = int(choice)
                
                if choice in item_choice:
                    print('You have already selected this item.')
                    continue
                
                item_choice.append(int_choice_input(items, choice))
                
            except ValueError:
                # Check if the user wants to stop entering items by 
                # inputting finish
                if choice.lower() == remove_item['finish_entry']:
                    print(remove_item['confirm_entry'])
                    break
                else:
                    print(error_text['invalid'])

        
        
        # Convert the numerical choice to the actual values 
        # that are in the items list.
        item_choice_values = []
        
        for choice in item_choice:
            item_choice_values.append(items[choice - 1])
        
        # Remove the items
        for choice in item_choice_values:
            items.remove(choice)
        
        # Variable to hold the text of the updated collection
        collection_text = ''
        
        # Add the fields
        collection_text += ','.join(fields)
        collection_text += '\n'
        
        
        # Add the items
        for item in items:
            collection_text += '\n'.join(item) + '\n'
        
        
        # Write the updated collection to it's file
        collection = open(collection_path, 'w')
        collection.write(collection_text)
        collection.close()
        
        print(remove_item['confirmation'] % collection_path[:len(collection_path)-4])
    
    # Remove a collection
    elif option == 5:
        #print('IN PROGRESS')
        #continue
        # Get collection to remove
        
        # Get a list of all collection paths, then print out and ask
        # user to select the collection they want to remove
        list = view_collections()
        if len(list) == 0:
            print(error_text['no_collections'])
            continue
        print(remove_collection['collection_entry'])
        print_collections(list)
        
        # Get the collection to remove from the user.
        collection_choice = int_choice_input(list)
        
        
        choice = list[collection_choice-1]
        choice_path = choice[:len(choice)-1]
        choice_name = choice[:len(choice)-5]
        
        
        print(choice + ' ' + choice_path + ' ' + choice_name)
        
        # Get confirmation of removal
        confirm = input(remove_collection['confirm_removal'] % choice_name)
        
        # If confirmed then attempt to remove the file
        if confirm.lower() == 'y':
            
            # Remove the File
            os.remove(choice_path)
            
            # Check if the file has been removed
            if os.path.exists(choice_path):
                
                # If the file has not been removed for some reason
                # then don't remove the collection from the list
                print(remove_collection['not_removed'] % choice_name)
                
                # Otherwise begin removing from the list
            else:
                print(remove_collection['removed'] % choice_name)
                
                # Remove the collection from collection_list.txt
                
                # Get all the collection lines from collection_list.txt in a list
                list = view_collections()
                print(list)
                
                # Remove the collection path from this list
                list.remove(choice)
                
                # Set the variable to use for writing the collection_id
                collection_id = 0
                str_id = ''
                
                # Open collection_list.txt to begin writing to
                collections = open(collection_list_path, 'w')
                
                # Now create the collection information to write
                # to collection_list.txt
                for collection_path in list:
                    
                    # Create a collection_id of format @C0000
                    str_id = str(collection_id)
                    while len(str_id) < 4:
                        str_id = '0' + str_id
                    str_id = '@C' + str_id
                    
                    # Increment the collection_id
                    collection_id += 1
                    
                    # Write the collection info lines 
                    collections.write(str_id + '\n' + collection_path + '\n')
                
                # Close collection_list.txt
                collections.close()
            
        else:
            print(remove_collection['not_removed'] % choice_name)
        
        
        
    else:
        print(error_text['invalid'])
    