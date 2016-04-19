db.define_table('address',
    Field('id_auth_user', 'reference auth_user', writable = False, readable = False),
    Field('home_num_pid11_1', 'integer'),
    Field('box_num_pid11_2', 'string'),
    Field('address1_pid11_3', 'string'),
    Field('address2_pid11_4', 'string'),
    Field('zipcode_pid11_5', 'string'),
    Field('town_pid11_6', 'string'),
    Field('country_pid11_7', 'string'),
    Field('address_rank','integer'),
    auth.signature)


db.define_table('test',
    Field('testname','string'),
    Field('testvalue','string'))
