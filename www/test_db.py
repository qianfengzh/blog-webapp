#/usr/bin/env python
# -*- coding: utf-8 -*-

from models import User, Blog, Comment
from transwrap import mydb
from transwrap.orm import Field

mydb.create_engine('root', 'password', 'blogdb')

u = User(name='test', email='test@example.com', password='1234567890', image='about:blank')


r = u.insert()
print type(r), r

print 'new user id: ', u.id

u1 = User.find_first('where email=?', 'test@example.com')
print 'find user\'s name:', u1.name
print type(u1)

u1.delete()

u2 = User.find_first('where email=?', 'test@example.com')
print 'find user\'s name:', u2


# import time, uuid
# print '%05d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)
