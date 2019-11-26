welcome_text = ['Welcome back to Collection Manager',
                         'Welcome to Collection Manager']
                         
collection_list_path = 'collection_list.txt'

mloop_options = ['1: Create a new collection',
                       '2: Add a new item',
                       '3: View a collection',
                       '9: Exit program']

exit_text = 'Exiting Program\nInput ANY key to continue\n'

general_input = {
    'name': 'Enter Name: ',
    'field': 'Enter Field: '
}

create_collection = {
    'name_entry': '\nPlease enter the name for your new collection:\n',
    'created': 'Collection Created: ',
    'field_entry': 'Please enter in fields for this collection, e.g. name.\nEnter 0 to finish.',
    'field_added': 'Added %s to %s collection.'
    }

add_item = {
    'collection_entry': '\nPlease select the collection you want to add too.\n',
    'field_entry': 'Please enter the %s for the new item: ',
    'added ': 'added to collection'
    }
    
view_collection = {
    'collection_entry': '\nPlease select the collection you want to view.\n',
    'view_collection': '\nViewing: '
    }
    
remove_item = {
    'collection_entry': '\nPlease select the collection you want to remove from.\n'
    }

error_text = {
    'no_collections': 'You have not created any collections yet.\n',
    'no_fields': 'You have not created any fields yet.\n',
    'not_int': 'Please enter an INTEGER.\n',
    'already_exists': 'This collection already exists.\n',
    'invalid': 'Invalid Option, please try again.\n'
    }
    
