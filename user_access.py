#!/usr/bin/python
import pwd, grp

users = pwd.getpwall()
groups = grp.getgrall()

users_len = max([len(user.pw_name)for user in users]) + 1

groups_len = max([len(group.gr_name) for group in groups]) + 1

f = open('test.txt','w');

fmt = '%-*s %4s %s'

print fmt %(users_len, 'Users',
              'GID',
              'Description')

print '-' * users_len, '----', '-' * 30


for user in users:
    print fmt %(users_len, user.pw_name,
              user.pw_gid,
              user.pw_gecos)

print '\n'

fmt = '%-*s %4s %s'

print fmt % (groups_len, 'Groups',
             'GID',
             'Members')

print '-' * groups_len, '----', '-' * 30


for group in groups:
    print fmt % ( groups_len, group.gr_name,
                group.gr_gid,
                ', '.join(group.gr_mem))

