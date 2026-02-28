import os, hashlib, binascii, sqlite3

pw='test123'
salt = os.urandom(16).hex()
hash = hashlib.pbkdf2_hmac('sha256', pw.encode(), salt.encode(), 260000)
hashhex = binascii.hexlify(hash).decode()
stored = f"pbkdf2:sha256:260000${salt}${hashhex}"
print('generated hash', stored)
# update db
conn=sqlite3.connect('nuclear_quiz.db')
c=conn.cursor()
try:
    c.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
    print('added column')
except Exception as e:
    print('alter error', e)
c.execute("UPDATE users SET hash=?, is_admin=1 WHERE username=?",(stored,'johnhmoore01@gmail.com'))
conn.commit()
print('rows',c.rowcount)
c.execute("SELECT id,username,is_admin FROM users WHERE username=?",('johnhmoore01@gmail.com',))
print(c.fetchall())
conn.close()
