db.define_table('tono',
    Field('id_auth_user', 'reference auth_user', required=True),
    Field('id_worklist', 'reference worklist'),
    Field('tonometry','decimal(2,2)'),
    Field('pachymetry','integer'),
    Field('techno','list:string'),
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

db.tono.id_auth_user.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s'+' '+'%(last_name)s')
db.topography.id_auth_user.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s'+' '+'%(last_name)s')
db.tono.laterality.requires = IS_IN_SET(('right','left'))
db.capsulotomy.laterality.requires = IS_IN_SET(('right','left'))
db.topography.laterality.requires = IS_IN_SET(('right','left'))
db.tono.techno.requires = IS_IN_SET(('air','apla'))

db.define_table ('optotype',
    Field('distance', 'list:string', required=True),
    Field('opto', 'string', required=True),
    auth.signature)

db.optotype.distance.requires = IS_IN_SET(('far','intermediate','close'))

db.define_table('rx',
    Field('id_auth_user','reference auth_user', required=True),
    Field('id_worklist','reference worklist'),
    Field('rx_origin', 'list:string', required=True),
    Field('glass_type', 'list:string'),
    Field('va_far','decimal(2,2)'),
    Field('opto_far','string'),
    Field('sph_far','decimal(2,2)'),
    Field('cyl_far','decimal(2,2)'),
    Field('axis_far', 'integer'),
    Field('opto_int','string'),
    Field('va_int','decimal(2,2)'),
    Field('sph_int','decimal(2,2)'),
    Field('cyl_int','decimal(2,2)'),
    Field('axis_int', 'integer'),
    Field('opto_close','string'),
    Field('va_close','decimal(2,2)'),
    Field('sph_close','decimal(2,2)'),
    Field('cyl_close','decimal(2,2)'),
    Field('axis_close', 'integer'),
    Field('note','string'),
    Field('laterality','list:string', required=True),
    auth.signature)

db.rx.rx_origin.requires = IS_IN_SET(('autorx','glass','trial','cyclo','dil'))
db.rx.laterality.requires = IS_IN_SET(('right','left'))
db.rx.glass_type.requires = IS_IN_SET(('monofocal','progressive','bifocal','degressive'))
