# many thanks to https://magazine.techacademy.jp/magazine/34155

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import appex
import clipboard
import base64
import dialogs

def abort(abort_message='script aborted'):
	clipboard.set(abort_message)
	print(abort_message)
	sys.exit()

def get_public_pem():
	pem_file = dialogs.pick_document(types=['public.data'])
	if pem_file is None:
		abort('pem file not selected')
	
	with open(pem_file, 'rb') as f:
		return f.read()
		
def separator(mark, length):
	leader_length = int((length - len(mark))/2)
	return '-' * leader_length + mark + '-' * leader_length

message = appex.get_text()

public_pem = get_public_pem()
	
try:
	public_key = RSA.importKey(public_pem)
except:
	abort('public key import error')

try:	
	cipher_rsa = PKCS1_OAEP.new(public_key)
except:
	abort('invalid puclic key')

try:	
	ciphertext = cipher_rsa.encrypt(message.encode())
except:
	abort('cannot encrypt')

b64ciphertext = base64.b64encode(ciphertext).decode()

sss = f'\n{separator("from here ", 40)}\n{b64ciphertext}\n{separator("to here ", 40)}\n'
clipboard.set(sss)

appex.finish()
