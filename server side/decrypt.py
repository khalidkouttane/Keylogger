from cryptography.fernet import Fernet
import sys

# using the key
with open('filekey.key', 'rb') as filekey:
	key = filekey.read()

# initialize Fernet Object
fernet = Fernet(key)


file_name = ' '.join(sys.argv[1:])
# opening the encrypted file
with open(file_name, 'rb') as enc_file:
    encrypted = enc_file.read()
 
# decrypting the file
decrypted = fernet.decrypt(encrypted)

# opening the file in write mode and
# writing the decrypted data
with open(file_name, 'wb') as dec_file:
    dec_file.write(decrypted)
