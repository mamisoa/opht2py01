def rows2json (tablename,rows):
    import datetime
    import json
    def date_handler(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime(str(T('%Y-%m-%d %T'))) #(str(T('%d/%m/%Y %T')))
        elif isinstance(obj, datetime.date):
            return obj.strftime(str(T('%Y-%m-%d'))) # (str(T('%d/%m/%Y')))
        else:
            return False
    rows = rows.as_list()
    concat = '{ "'+tablename+'": ['
    for row in rows:
        concat = concat + json.dumps(row, default=date_handler)+","
    concat = concat.strip(',')
    concat = concat + ']}'
    return concat

def valid_date(datestring):
    import datetime
    try:
        datetime.datetime.strptime(datestring, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@request.restful()
def wl():
    import datetime
    response.view = 'generic.json'
    def GET(**vars):
        provider = db.auth_user.with_alias('provider')
        patient = db.auth_user.with_alias('patient')
        creator = db.auth_user.with_alias('creator')
        editor = db.auth_user.with_alias('editor')
        sender = db.facility.with_alias('sender')
        receiver = db.facility.with_alias('receiver')
        # date_after = (datetime.datetime.strptime(request.vars.date_after,'"%Y-%m-%d"').date() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if (request.vars.date_before == None) or (request.vars.date_after == None) or (valid_date(request.vars.date_after) == False) or (valid_date(request.vars.date_before) == False):
            date_after = datetime.date.today().strftime('%Y-%m-%d')
            date_before = (datetime.datetime.strptime(date_after,'%Y-%m-%d').date() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            date_after = (request.vars.date_after).translate(None,'"')
            date_before = (request.vars.date_before).translate(None,'"')
        query=((db.worklist.created_on>date_after)&(db.worklist.created_on<date_before))
        db.worklist.created_by.readable = db.worklist.modified_by.readable = db.worklist.created_on.readable = db.worklist.modified_on.readable = db.worklist.id_auth_user.readable = True
        rows =  db(query).select(provider.id, provider.first_name, provider.last_name,
                        patient.id, patient.first_name, patient.last_name,
                        db.worklist.id, db.worklist.id_auth_user,
                        db.worklist.exam2do_OBR4,db.worklist.warning, db.exam2do_OBR4.controller,
                        db.exam2do_OBR4.id, db.exam2do_OBR4.exam_description, db.worklist.laterality,
                        db.exam2do_OBR4.cycle_num, db.exam2do_OBR4.procedure_seq,
                        db.worklist.message_unique_id_MSH10,
                        sender.facility_name, receiver.facility_name,
                        db.worklist.status_flag, db.worklist.requested_time_OBR6,
                        db.modality.modality_name, db.worklist.counter,
                        creator.first_name, creator.last_name, editor.first_name, editor.last_name,
                        db.worklist.created_on, db.worklist.modified_on,
                        left = [
                        patient.on(patient.id==db.worklist.id_auth_user),
                        provider.on(provider.id==db.worklist.provider_OBR16),
                        db.exam2do_OBR4.on(db.exam2do_OBR4.id==db.worklist.exam2do_OBR4),
                        receiver.on(receiver.id==db.worklist.receving_facility_MSH6),
                        sender.on(sender.id==db.worklist.sending_facility_MSH4),
                        db.modality.on(db.modality.id==db.worklist.modality_dest_OBR24),
                        creator.on(creator.id==db.worklist.created_by),
                        editor.on(editor.id==db.worklist.modified_by)
                        ]
                        )
        data = rows2json('content',rows)
        return data
    def DELETE(tablename,record_id):
        if tablename=='worklist':
            db(db.worklist.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id('+record_id+') *** \r\n'
        else:
            raise HTTP(400)
    def PUT(tablename,record_id,**vars):
        if tablename == 'worklist':
            db(db.worklist._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id('+record_id+') ***  \r\n'
        else:
            raise HTTP(400)
    def POST(tablename,**vars):
        if tablename == 'worklist':
            ret = db.worklist.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        else:
            raise HTTP(400)
    return locals()


@request.restful()
def users_list():
    response.view = 'generic.json'
    def GET(mb):
        try:
            query_sessions = (
            (db.auth_user.id == db.auth_membership.user_id)&
            (db.auth_membership.group_id == mb)
            )
            user = db.auth_user.with_alias('user')
            rows =  db(query_sessions).select(
                            user.first_name, user.last_name, user.id, user.dob_pid7, user.gender_pid8,
                            db.gender.sex, db.address.town_pid11_6,
                            groupby= db.auth_user.id,
                            left = [ user.on(user.id==db.auth_membership.user_id),
                                    db.gender.on(db.gender.id == db.auth_user.gender_pid8),
                                    db.address.on(db.address.id_auth_user == db.auth_user.id)
                            ])
            data = rows2json('content',rows)
            return  data
        except ValueError: raise HTTP(400)
    def DELETE(tablename,record_id):
        if tablename=='auth_user':
            db(db.auth_user.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id('+record_id+') *** \r\n'
        else:
            raise HTTP(400)
    return locals()

@request.restful()
def users():
    response.view = 'generic.json' # or 'generic.' + request.extension
    def GET(*args,**vars):
        patterns = [
            "/user[auth_user]",
            "/user/{auth_user.id}",
            "/user/{auth_user.id}/:field",
            "/user/{auth_user.first_name.contains}/{auth_user.last_name.contains}/{auth_user.dob_pid7.eq}",
            "/membership[auth_membership]",
            "/membership/{auth_membership.group_id}/user[auth_user.id]",  # show user with selected membership
            "/membership/{auth_membership.group_id}/user[auth_user.id]/:field",
            "/address[address]",
            "/address/{address.id_auth_user}",
            "/phone[phone]",
            "/phone/{phone.id_auth_user}",
            "/worklist[worklist]",
            "/worklist/{worklist.id}"
            ]
        db.address.created_by.readable = db.address.modified_by.readable = db.address.created_on.readable = db.address.modified_on.readable = db.address.id_auth_user.readable = True
        db.auth_user.created_by.readable = db.auth_user.modified_by.readable = db.auth_user.created_on.readable = db.auth_user.modified_on.readable = True
        db.phone.created_by.readable = db.phone.modified_by.readable = db.phone.created_on.readable = db.phone.modified_on.readable = db.phone.id_auth_user.readable = True
        db.worklist.created_by.readable = db.worklist.modified_by.readable = db.worklist.created_on.readable = db.worklist.modified_on.readable = db.worklist.id_auth_user.readable = True
        db.auth_user.id.represent = lambda auth_id,row: row.first_name+' '+row.last_name
        parser = db.parse_as_rest(patterns, args, vars)
        data = parser.response
        if parser.status == 200:
            return dict(content=data)
        else:
            raise HTTP(parser.status, parser.error)
    def DELETE(tablename,record_id):
        if tablename=='auth_user':
            db(db.auth_user.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id : '+record_id+' *** \r\n'
        elif tablename=='auth_membership':
            db(db.auth_membership.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id : '+record_id+' *** \r\n'
        elif tablename=='address':
            db(db.address.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id('+record_id+') *** \r\n'
        elif tablename=='phone':
            db(db.phone.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id('+record_id+') *** \r\n'
        else:
            raise HTTP(400)
    def PUT(tablename,record_id,**vars):
        if tablename == 'auth_user':
            vars['password']=CRYPT()(vars['password'])[0]
            db(db.auth_user._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id: '+record_id+' ***  \r\n'
        elif tablename == 'auth_membership':
            db(db.auth_membership._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id: '+record_id+' ***  \r\n'
        elif tablename == 'address':
            db(db.address._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id('+record_id+') ***  \r\n'
        elif tablename == 'phone':
            db(db.phone._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id('+record_id+') ***  \r\n'
        elif tablename == 'worklist':
            db(db.worklist._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id('+record_id+') ***  \r\n'
        else:
            raise HTTP(400)
    def POST(tablename,**vars):
        if tablename == 'auth_user':
            ret = db.auth_user.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        elif tablename == 'auth_membership':
            ret = db.auth_membership.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id: '+ str(ret.id) + ' *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        elif tablename == 'address':
            ret = db.address.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        elif tablename == 'phone':
            ret = db.phone.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        elif tablename == 'worklist':
            ret = db.worklist.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        else:
            raise HTTP(400)
    return locals()


@request.restful()
def topo():
    response.view = 'generic.json'
    def GET(**vars):
        patient = db.auth_user.with_alias('patient')
        creator = db.auth_user.with_alias('creator')
        editor = db.auth_user.with_alias('editor')
        db.topography.created_by.readable = db.topography.modified_by.readable = db.topography.created_on.readable = db.topography.modified_on.readable = db.topography.id_auth_user.readable = True
        rows =  db((db.topography.id_auth_user==request.vars.id_auth_user)&(db.topography.id_worklist==request.vars.id_worklist)).select(db.topography.id,
                        db.topography.id_auth_user, db.topography.id_worklist,
                        db.topography.laterality, db.topography.k1, db.topography.k2, db.topography.axis1, db.topography.axis2,
                        db.topography.created_by,db.topography.created_on, db.topography.modified_by,db.topography.modified_on,
                        patient.first_name, patient.last_name, creator.first_name, creator.last_name, editor.first_name, editor.last_name,
                        left=[patient.on(patient.id==db.topography.id_auth_user),
                        creator.on(creator.id==db.topography.created_by),
                        editor.on(editor.id==db.topography.modified_by)
                        ])
        data = rows2json('content',rows)
        return data
    def DELETE(tablename,record_id):
        if tablename=='topography':
            db(db.topography.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id('+record_id+') *** \r\n'
        else:
            raise HTTP(400)
    def PUT(tablename,record_id,**vars):
        if tablename == 'topography':
            db(db.topography._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id('+record_id+') ***  \r\n'
        else:
            raise HTTP(400)
    def POST(tablename,**vars):
        if tablename == 'topography':
            ret = db.topography.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        else:
            raise HTTP(400)
    return locals()

@request.restful()
def tono():
    response.view = 'generic.json'
    def GET(**vars):
        patient = db.auth_user.with_alias('patient')
        creator = db.auth_user.with_alias('creator')
        editor = db.auth_user.with_alias('editor')
        db.tono.created_by.readable = db.tono.modified_by.readable = db.tono.created_on.readable = db.tono.modified_on.readable = db.tono.id_auth_user.readable = True
        rows =  db((db.tono.id_auth_user==request.vars.id_auth_user)&(db.tono.id_worklist==request.vars.id_worklist)).select(db.tono.id,
                        db.tono.id_auth_user, db.tono.id_worklist,
                        db.tono.laterality, db.tono.tonometry, db.tono.pachymetry, db.tono.techno,
                        db.tono.created_by,db.tono.created_on, db.tono.modified_by,db.tono.modified_on,
                        patient.first_name, patient.last_name, creator.first_name, creator.last_name, editor.first_name, editor.last_name,
                        left=[patient.on(patient.id==db.tono.id_auth_user),
                        creator.on(creator.id==db.tono.created_by),
                        editor.on(editor.id==db.tono.modified_by)
                        ])
        data = rows2json('content',rows)
        return data
    def DELETE(tablename,record_id):
        if tablename=='tono':
            db(db.tono.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id('+record_id+') *** \r\n'
        else:
            raise HTTP(400)
    def PUT(tablename,record_id,**vars):
        if tablename == 'tono':
            db(db.tono._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id('+record_id+') ***  \r\n'
        else:
            raise HTTP(400)
    def POST(tablename,**vars):
        if tablename == 'tono':
            ret = db.tono.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        else:
            raise HTTP(400)
    return locals()

@request.restful()
def rx():
    response.view = 'generic.json'
    def GET(**vars):
        patient = db.auth_user.with_alias('patient')
        creator = db.auth_user.with_alias('creator')
        editor = db.auth_user.with_alias('editor')
        db.rx.created_by.readable = db.rx.modified_by.readable = db.rx.created_on.readable = db.rx.modified_on.readable = db.rx.id_auth_user.readable = True
        rows =  db((db.rx.id_auth_user==request.vars.id_auth_user)&(db.rx.id_worklist==request.vars.id_worklist)).select(db.rx.id,
                        db.rx.id_auth_user, db.rx.id_worklist,
                        db.rx.created_by,db.rx.created_on, db.rx.modified_by,db.rx.modified_on,
                        db.rx.glass_type, db.rx.rx_origin, db.rx.laterality,
                        db.rx.sph_far, db.rx.cyl_far, db.rx.axis_far, db.rx.va_far,
                        db.rx.sph_int, db.rx.cyl_int, db.rx.axis_int, db.rx.va_int,
                        db.rx.sph_close, db.rx.cyl_close, db.rx.axis_close, db.rx.va_close, db.rx.note,
                        db.rx.opto_far, db.rx.opto_int, db.rx.opto_close,
                        patient.first_name, patient.last_name, creator.first_name, creator.last_name, editor.first_name, editor.last_name,
                        left=[patient.on(patient.id==db.rx.id_auth_user),
                        creator.on(creator.id==db.rx.created_by),
                        editor.on(editor.id==db.rx.modified_by)
                        ])
        data = rows2json('content',rows)
        return data
    def DELETE(tablename,record_id):
        if tablename=='rx':
            db(db.rx.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id('+record_id+') *** \r\n'
        else:
            raise HTTP(400)
    def PUT(tablename,record_id,**vars):
        if tablename == 'rx':
            db(db.rx._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id('+record_id+') ***  \r\n'
        else:
            raise HTTP(400)
    def POST(tablename,**vars):
        if tablename == 'rx':
            ret = db.rx.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        else:
            raise HTTP(400)
    return locals()

@request.restful()
def consult():
    from datetime import datetime
    response.view = 'generic.json'
    def GET(**vars):
        patient = db.auth_user.with_alias('patient')
        creator = db.auth_user.with_alias('creator')
        editor = db.auth_user.with_alias('editor')
        # dateFrom = datetime.strptime(request.vars.created_on, '%Y-%m-%d %H:%M:%S').replace(hour=0,minute=0,second=0)
        # dateTo = (dateFrom.replace(hour=23,minute=59,second=59)).strftime('%Y-%m-%d %H:%M:%S')
        # dateFrom = dateFrom.strftime('%Y-%m-%d %H:%M:%S')
        dateFrom = datetime.strptime(request.vars.dateFrom,'%Y-%m-%d %H:%M:%S')
        dateTo =  datetime.strptime(request.vars.dateTo,'%Y-%m-%d %H:%M:%S')
        if dateFrom > dateTo:
            raise HTTP(400)
        else:
            dateFrom = dateFrom.strftime('%Y-%m-%d %H:%M:%S')
            dateTo = dateTo.strftime('%Y-%m-%d %H:%M:%S')
        db.tono.created_by.readable = db.tono.modified_by.readable = db.tono.created_on.readable = db.tono.modified_on.readable = db.tono.id_auth_user.readable = True
        db.rx.created_by.readable = db.rx.modified_by.readable = db.rx.created_on.readable = db.rx.modified_on.readable = db.rx.id_auth_user.readable = True
        db.topography.created_by.readable = db.topography.modified_by.readable = db.topography.created_on.readable = db.topography.modified_on.readable = db.topography.id_auth_user.readable = True
        rows_tono = db((db.tono.id_auth_user == request.vars.id_auth_user)&(db.tono.created_on > dateFrom)&(db.tono.created_on <= dateTo) ).select(db.tono.tonometry, db.tono.pachymetry, db.tono.techno, db.tono.laterality,
            creator.first_name, creator.last_name, db.tono.created_on,
            patient.first_name, patient.last_name,
            left=[patient.on(patient.id==db.tono.id_auth_user),
            creator.on(creator.id==db.tono.created_by)
            ])
        rows_topo = db((db.topography.id_auth_user == request.vars.id_auth_user)&(db.topography.created_on > dateFrom)&(db.topography.created_on <= dateTo)).select(db.topography.k1, db.topography.axis1, db.topography.k2, db.topography.axis2, db.topography.laterality,
            creator.first_name, creator.last_name, db.topography.created_on,
            patient.first_name, patient.last_name,
            left=[patient.on(patient.id==db.topography.id_auth_user),
            creator.on(creator.id==db.topography.created_by)
            ])
        rows_rx = db((db.rx.id_auth_user == request.vars.id_auth_user)&(db.rx.created_on > dateFrom)&(db.rx.created_on <= dateTo)).select(db.rx.va_far, db.rx.sph_far, db.rx.cyl_far, db.rx.axis_far, db.rx.opto_far,
            db.rx.va_int, db.rx.sph_int, db.rx.cyl_int, db.rx.axis_int, db.rx.opto_int,
            db.rx.va_close, db.rx.sph_close, db.rx.cyl_close, db.rx.axis_close, db.rx.opto_close,
            db.rx.rx_origin, db.rx.glass_type, db.rx.laterality,
            creator.first_name, creator.last_name, db.rx.created_on,
            patient.first_name, patient.last_name,
            left=[patient.on(patient.id==db.rx.id_auth_user),
            creator.on(creator.id==db.rx.created_by)
            ])
        data = '['+rows2json('tono',rows_tono)+','+rows2json('topo',rows_topo)+','+rows2json('rx',rows_rx)+']'
        return  data
    def DELETE(tablename,record_id):
        if tablename=='consult':
            db(db.consult.id == record_id).delete()
            return 'Table: '+ tablename +' *** Deleted row id('+record_id+') *** \r\n'
        else:
            raise HTTP(400)
    def PUT(tablename,record_id,**vars):
        if tablename == 'consult':
            db(db.consult._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id('+record_id+') ***  \r\n'
        else:
            raise HTTP(400)
    def POST(tablename,**vars):
        if tablename == 'consult':
            ret = db.consult.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id('+ str(ret.id) + ') *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        else:
            raise HTTP(400)
    return locals()
