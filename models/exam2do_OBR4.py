db.define_table('air_tono',
    Field('id_auth_user', 'reference auth_user', required=True),
    Field('id_worklist', 'reference worklist'),
    Field('air_tonometry','decimal(2,2)'),
    Field('pachymetry','integer'),
    Field('laterality', 'list:string', required=True),
    auth.signature)

db.define_table('topography',
    Field('id_auth_user','reference auth_user', required=True),
    Field('id_worklist','reference worklist'),
    Field('k1','decimal(2,2)'),
    Field('k2','decimal(2,2)'),
    Field('axis1','decimal(2,2)'),
    Field('axis2','decimal(2,2)'),
    Field('laterality','list:string', required=True),
    auth.signature)

db.define_table('capsulotomy',
    Field('id_auth_user','reference auth_user', required=True),
    Field('id_worklist','reference worklist'),
    Field('power_intensity','decimal(2,2)'),
    Field('spot_size','decimal(2,2)'),
    Field('laterality','list:string', required=True),
    auth.signature)

db.air_tono.id_auth_user.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s'+' '+'%(last_name)s')
db.topography.id_auth_user.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s'+' '+'%(last_name)s')
db.air_tono.laterality.requires = IS_IN_SET('right','left')
db.capsulotomy.laterality.requires = IS_IN_SET(('right','left'))
db.topography.laterality.requires = IS_IN_SET(('right','left'))
