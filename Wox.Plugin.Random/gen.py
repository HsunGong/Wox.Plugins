import uuid
import random

# defaults
B32_SPACE = '[^ABCDEFGHIJKLMNOPQRSTUVWXYZ234567]+'
B32_LEN = 26

def gen_uuid(name=''):
    """ uuid3:md5 uuid5:sha-1"""
    from time import gmtime, strftime
    return uuid.uuid5(namespace=uuid.NAMESPACE_DNS,
                    name=strftime("%Y-%m-%d-%H:%M:%S", gmtime()) + name)



def gen_uuid_base(start_word='wox', length=B32_LEN, name_len=24):
    """
    youd import from https://github.com/t-mart/youd/blob/master/youd.py\n
    Generate a random base32-encoded uuid (A-Z,2-7) with an optional readable word in the beginning.\n
    If you provide a string as the first argument to this script, it will replace the first characters of this otherwise random uuid.
    Only characters of the word that are in the (A-Z, 2-7) space will be placed. Lower cased letters that are provided are
    converted to upper case.
    Why? Sometimes, you're writing tests or documentation and you need a uuid, but also want it to be readable and meaningful. What's
    going to convey more to users? RPRKIRYJSVMWSOY64XS3CIL3OO or SPECIALUUID6JIHP5RKUQBPDQI ?
    The second uuid there was created by running the script like this:
    $ youd "special uuid"
    """
    import re
    u = re.sub(B32_SPACE, '', start_word.upper())[:name_len]  # max name len
    import base64
    real_uuid = base64.b32encode(uuid.uuid4().bytes)[:length]
    return u + str(real_uuid[:(length - len(u))], encoding="utf-8")

def gen_passwd(size=12, sign=False):
    """
    import from https://github.com/sectool/Python-Random-Password-Generator/blob/master/source/rpg.py
    """
    import string
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    if sign:
        chars += chars + string.punctuation
    chars += string.digits
    return ''.join(random.choice(chars) for x in range(0, size))
