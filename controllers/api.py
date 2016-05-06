def rows2json (tablename,rows):
    import datetime
    import json
    def date_handler(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime(str(T('%d/%m/%Y %T')))
        elif isinstance(obj, datetime.date):
            return obj.strftime(str(T('%d/%m/%Y')))
        else:
            return False
    rows = rows.as_list()
    concat = '{ "'+tablename+'": ['
    for row in rows:
        concat = concat + json.dumps(row, default=date_handler)+","
    concat = concat.strip(',')
    concat = concat + ']}'
    return concat

@request.restful()
def wl():
    response.view = 'generic.json'
    def GET():
        provider = db.auth_user.with_alias('provider')
        patient = db.auth_user.with_alias('patient')
        creator = db.auth_user.with_alias('creator')
        editor = db.auth_user.with_alias('editor')
        db.worklist.created_by.readable = db.worklist.modified_by.readable = db.worklist.created_on.readable = db.worklist.modified_on.readable = db.worklist.id_auth_user.readable = True
        rows =  db(db.worklist).select(provider.id, provider.first_name, provider.last_name,
                        patient.id, patient.first_name, patient.last_name,
                        db.worklist.id, db.worklist.id_auth_user, db.worklist.exam2do_OBR4,
                        db.exam2do_OBR4.id, db.exam2do_OBR4.exam_description,
                        db.worklist.receving_facility_MSH6,
                        db.facility.facility_name,
                        db.worklist.status_flag, db.worklist.requested_time_OBR6,
                        db.modality.modality_name,
                        creator.first_name, creator.last_name, editor.first_name, editor.last_name,
                        db.worklist.created_on, db.worklist.modified_on,
                        left = [
                        patient.on(patient.id==db.worklist.id_auth_user),
                        provider.on(provider.id==db.worklist.provider_OBR16),
                        db.exam2do_OBR4.on(db.exam2do_OBR4.id==db.worklist.exam2do_OBR4),
                        db.facility.on(db.facility.id==db.worklist.receving_facility_MSH6),
                        db.modality.on(db.modality.id==db.worklist.modality_dest_OBR24),
                        creator.on(creator.id==db.worklist.created_by),
                        editor.on(editor.id==db.worklist.modified_by)
                        ]
                        )
        data = rows2json('content',rows)
        return  data
    def DELETE(tablename,record_id):
        if tablename=='worklist':
            db(db.worklist.id == record_id).delete()
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
