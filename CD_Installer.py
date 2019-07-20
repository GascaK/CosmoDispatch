#!/usr/bin/env python
import os

class CDUpdate():
    def __init__(self, update_file):
        '''CDUpdate(update_file)
            Update the CosmoDispatch app with the following information
            from update_file.
        '''
        # Standard location of local.
        location = ''
        try:
            with open(update_file, 'r') as u_file:
                for line in u_file:
                    # Locate File Load location. Will return 
                    if line[:4] == '[FL]':
                        location = line[4:]
                        try:
                            os.remove(location[:-1])
                        # Catch FileNotFoundError while attempting to delete 
                        # file at location. Continue as this works out.
                        except FileNotFoundError:
                            continue
                        continue #skip the location line
                    # If location is not empty continue. Otherwise skip line assignment.
                    if location is not '':
                        self.run_update(location[:-1], line)
        # Catch FileNotFoundError while attempting to open CD_update.txt
        except FileNotFoundError:
            print('File was not located. Verify CD_update.'\
                  'txt was downloaded correctly')

    def run_update(self, location, line):
        '''run_update(location, line)
            Write line by line to the specific location listed. 
            Point of friction as opening and closing the file seems
            tedious and may need refractoring.
        '''
        try:
            up_file = open(location, 'a')
        # Catch FileNotFoundError, if true then Create file first then write line.
        except FileNotFoundError:
            result = location.find('\\')
            if not os.path.exists(location[:result]):
                print(f'Creating Directory: {location[:result]}')
                os.makedirs(location[:result])
            # Create file
            up_file = open(location, 'w')
        up_file.write(line)
        up_file.close()


if __name__ == '__main__':
    cdi = CDUpdate('CD_update.txt')