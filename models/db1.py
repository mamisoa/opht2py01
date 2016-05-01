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

db.define_table('insurance',
    Field('id_auth_user', 'reference auth_user', writable= False, readable= False),
    Field('insurance_name_IN1', 'string', required=True),
    Field('insurance_plan_IN2', 'string'),
    Field('insurance_type_IN3', 'string'),
    auth.signature)

db.insurance.insurance_type_IN3.requires=IS_IN_DB(db,'insurance_sector.sector','%(sector)s')

db.define_table('insurance_sector',
    Field('sector', 'string', default='State'),
    format=lambda r: r.sector or 'State'
)

db.define_table('exam2do_OBR4',
    Field('loinc_code', 'string'),
    Field('exam_description','string'),
    auth.signature)

db.define_table('status',
    Field('id_worklist'),
    Field('status_flag','list:string', required=True),
    auth.signature)

db.status.status_flag.requires=IS_IN_SET(('requested', 'in process', 'done', 'cancelled'))

db.define_table('worklist',
    Field('id_auth_user', 'reference auth_user'),
    Field('sending_app_MSH3','string', default = 'Oph2Py'),
    Field('sending_facility_MSH4','string', default = 'Eye Center'),
    Field('receving_app_MSH5','string', default = 'Receving App'),
    Field('receving_facility_MSH6','string', default = 'Eye Center'),
    Field('message_unique_id_MSH10','string', required=True),
    Field('exam2do_OBR4', 'reference exam2do_OBR4' , required=True),
    Field('provider_OBR16', 'string', required=True),
    Field('requested_time_OBR6', 'datetime', required=True),
    Field('modality_dest_OBR24', 'string'),
    Field('status_flag', 'list:string', required=True),
    auth.signature)

query_sessions = (
(db.auth_user.id == db.auth_membership.user_id)&
(db.auth_membership.group_id == 3)
)

db.worklist.id_auth_user.requires=IS_IN_DB(db,'auth_user.id','%(first_name)s'+' '+'%(last_name)s')
db.worklist.provider_OBR16.requires=IS_IN_DB(db(query_sessions), 'auth_user.id', '%(first_name)s'+' '+'%(last_name)s' )
db.worklist.status_flag.requires=IS_IN_SET(('requested', 'in process', 'done', 'cancelled'))
db.worklist.exam2do_OBR4.requires=IS_IN_DB(db,'exam2do_OBR4.exam_description')

db.define_table('test',
    Field('testname','string'),
    Field('testvalue','string'))
