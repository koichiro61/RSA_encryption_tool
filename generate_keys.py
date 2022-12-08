# many thanks to https://magazine.techacademy.jp/magazine/34155

from Crypto.PublicKey import RSA

# 秘密鍵の生成
private_key = RSA.generate(2048)
with open("private.pem", "w") as f:
	tmp = private_key.exportKey(passphrase='fakepass', pkcs=8).decode('utf-8')
	#print(tmp)
	f.write(tmp)
	
# 秘密鍵から公開鍵を生成
public_key = private_key.publickey()
with open("receiver.pem", "w") as f:
	tmp = public_key.exportKey().decode('utf-8')
	#print(tmp)
	f.write(tmp)
