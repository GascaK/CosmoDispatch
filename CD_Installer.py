#!/usr/bin/env python
import os

class CDUpdate():
    def __init__(self, update_file):
        location = '/'
        updated_text = []
        with open(update_file, 'r') as u_file:
            for line in u_file:
                if line[:4] == '[FL]':
                    location = line[4:]
                    try:
                        os.remove(location[:-1])
                    except FileNotFoundError:
                        continue
                    continue #skip the location line
                self.run_update(location[:-1], line)

    def run_update(self, location, line):
        try:
            up_file = open(location, 'a')
        except FileNotFoundError:
            result = location.find('\\')
            if not os.path.exists(location[:result]):
                print(f'Creating Directory: {location[:result]}')
                os.makedirs(location[:result])
            up_file = open(location, 'w')
        up_file.write(line)
        up_file.close()


if __name__ == '__main__':
    cdi = CDUpdate('CD_update.txt')