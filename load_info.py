import json


# Obfuscation of data only. Not a true valid form of data
# privacy. Due to Security unable to download cryptography
# libraries to assist.
def load_data(key_pair):
    filepath = 'config/info.json'
    with open(filepath) as creds:
        data = json.load(creds)
        try:
            if key_pair[-4:] == 'pass':
                return un_obfs(data[key_pair])
            else:
                return data[key_pair]
        except KeyError:
            return 'UnF'
        except ValueError:
            return 'UnF'


def save_data(hot_user, hot_pass, lms_user, lms_pass):
    filepath = 'config/info.json'
    # Allow for empty responses before saving. 
    if not hot_user:
        hot_user = load_data('hot_user')
    if not hot_pass:
        hot_pass = load_data('hot_pass')
    if not lms_user:
        lms_user = load_data('lms_user')
    if not lms_pass:
        lms_pass = load_data('lms_pass')

    with open(filepath, 'w') as creds:
        json.dump({'hot_user': hot_user,
                   'hot_pass': obfs(hot_pass),
                   'lms_user': lms_user,
                   'lms_pass': obfs(lms_pass)}, creds)
        return True


def obfs(value):
    load = []
    saved = list(value)
    for each in saved:
        load.append(ord(each))
    return('.'.join(str(e) for e in load))


def un_obfs(value):
    load = []
    saved = value.split('.')
    for each in saved:
        load.append(chr(int(each)))
    return(''.join(load))