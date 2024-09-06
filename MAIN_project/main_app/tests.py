from django.conf import settings

from os import urandom

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


pswd = b'\xd0\xd0\xeag]\xf4\x94W\xf8\xd7\xbc\x98t\xac\xd0\xb1<\xa1\xd2\xc6kg\xf7\xfd;9\xf2:\rG)\xc6'
iv = b'\x90\xa7z\xde+\xa1]\x11}\xaa\xd8}\xb5\x87\x8b\xd0'


key = bytes('go41_Maks1mum58!', 'utf-8')

obj = AES.new(key, mode=AES.MODE_CBC, iv=iv)
print('pass', unpad(obj.decrypt(pswd), 16).decode('utf-8'))

# def save(self, *args, **kwargs):  # в момент сохранения кодируем пароль
#     school = super(SchoolDB, self)
#     print(type(self.db_password))
#     key = bytes(settings.PASSWORD_SCHOOL, 'ASCII')
#     iv = urandom(16)
#     pass_to_crypt = pad(bytes(str(self.db_password), 'ASCII'), 16)
#     obj = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
#     self.db_password = obj.encrypt(pass_to_crypt)
#     self.iv = iv
#     obj2 = AES.new(key, mode=AES.MODE_CBC, iv=key)
#     print('pass', unpad(obj2.decrypt(self.db_password), 16).decode('ASCII'))
#     school.save()
#     return school

# Create your tests here.
