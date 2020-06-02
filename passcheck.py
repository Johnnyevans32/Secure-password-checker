import requests
import hashlib


def request_api(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, Try API AGAIN!!')
    return res


def get_leaked(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_pass(passwords):
    sha1pass = hashlib.sha1(passwords.encode('utf-8')).hexdigest().upper()
    first5_char, rest = sha1pass[:5], sha1pass[5:]
    response = request_api(first5_char)
    return get_leaked(response, rest)



def main(args):
    count = pwned_pass(args)
    if count:
        print(f'''
            Password {args} has been Hacked {count} times...
                    Try a more secure Password!!
        ''')
    else:
        print(f'''
            HOORAY!!! Password {args} Has not been Breached or hacked
                   You can continue with this password!!
        ''')
    return 'Check Complete!!!'



if __name__ == '__main__':
    inp = input('Type in the password you want to check: ')
    exit(main(inp))
