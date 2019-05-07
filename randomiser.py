import hashlib

msg = input('Type ID: ')

m = hashlib.blake2b(msg.encode('utf-8'), digest_size=1).hexdigest()

print(m)

## hello 
