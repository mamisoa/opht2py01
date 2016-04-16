db.define_table('address',
    Field('id_auth_user', 'reference auth_user', writable = False, readable = False),
    Field('address1_pid11_1', 'string'),
    Field('address2_pid11_2', 'string'))

db.define_table('test',
    Field('testname','string'),
    Field('testvalue','string'))
