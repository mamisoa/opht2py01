db.define_table('address',
    Field('id_auth_user', 'reference auth_user', writable = False, readable = False),
    Field('address1', 'string'),
    Field('address2', 'string'))

db.define_table('test',
    Field('testname','string'),
    Field('testvalue','string'))
