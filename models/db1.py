db.define_table('address',
    Field('id_auth_user', 'reference auth_user', writable = False, readable = False),
    Field('home_num_pid11_1', 'integer', required=True),
    Field('box_num_pid11_2', 'string'),
    Field('address1_pid11_3', 'string', required=True),
    Field('address2_pid11_4', 'string'),
    Field('zipcode_pid11_5', 'string', required=True),
    Field('town_pid11_6', 'string', required=True),
    Field('country_pid11_7', 'string', required=True),
    Field('address_rank','integer'),
    auth.signature)

db.define_table('phone',
    Field('id_auth_user', 'reference auth_user', writable= False, readable= False),
    Field('phone_prefix_pid13_1', 'integer', required=True, default = '32'),
    Field('phone_pid13_2', 'string', required=True),
    Field('phone_origin', 'string', required=True ),
    auth.signature)

db.phone.phone_origin.requires=IS_IN_DB(db,'data_origin.origin','%(origin)s')

db.define_table('data_origin',
    Field('origin', 'string', default='Home'),
    format=lambda r: r.origin or 'Home'
)


db.define_table('test',
    Field('testname','string'),
    Field('testvalue','string'))
