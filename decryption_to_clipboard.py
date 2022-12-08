'''

Note that I shall not be responsible for any loss, damages and troubles caused by any software published here.

pythonista3 用
選択した暗号文字列を複合するスクリプト

文字列選択状態で「共有」→「pythonista script」→このスクリプトの名前
ファイル選択ダイアログでプライベート証明書ファイルを選択
passphrase ダイアログでプライベート証明書用パスフレーズ入力

正常終了すると「共有」ダイアログが消えて複合結果がクリップボードに入る
'''

import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import appex
import clipboard
import dialogs

def abort(abort_message='script aborted'):
	passphrase = ''
	privatekey = ''
	decipher_rsa = ''
	clipboard.set(abort_message)
	print(abort_message)
	sys.exit()

def get_passphrase():
	fields = []
	field = {'type':'password','key':'passphrase','title':'Enter'}
	fields.append(field) 
	dd = dialogs.form_dialog(title='pass phrase required', fields=fields)

	if dd is not None: 
		return dd['passphrase']
	else:
		abort('passphrase dialog is cancelled')
	
def get_encrypted_text():
	b64_encrypted_text  = appex.get_text()

	try:
		return base64.b64decode(b64_encrypted_text)
	except:
		abort('base64 decode error')
		
def get_private_pem():
	
	pem_file = dialogs.pick_document(types=['public.data'])
	if pem_file is None:
		abort('pem file not selected')
	
	with open(pem_file, 'rb') as f:
		return f.read()
		
def get_private_key(private_pem, passphrase):
	try:
		return RSA.importKey(private_pem,passphrase=passphrase)
	except ValueError:
		abort('pem or passphrase may be invalid')
	
# main routine ----------

encrypted_text = get_encrypted_text()

private_pem = get_private_pem()
passphrase = get_passphrase()

private_key = get_private_key(private_pem, passphrase)
passphrase = ''	# now it's no use, so cleared for sure

decipher_rsa = PKCS1_OAEP.new(private_key)
private_key = ''	# ditto

try:
	decrypted_text  = decipher_rsa.decrypt(encrypted_text).decode("utf-8")
	decipher_rsa = ''	# ditto
except ValueError:
	abort('decryption error')
	
clipboard.set(decrypted_text)
appex.finish()
sys.exit()
