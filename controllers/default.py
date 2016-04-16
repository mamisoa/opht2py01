# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def home():
    if (request.args(0) == None):
        membership = '2'
    else:
        try:
            check_group= db(db.auth_group.id == request.args(0)).isempty()
        except ValueError:
            membership = '2'
        else:
            if check_group is True:
                membership = '2'
            else:
                membership = str(request.args(0))
    group = (db(db.auth_group.id == membership).select().first()).role
    return locals()

@auth.requires_membership('IT')
def manage():
    grid = SQLFORM.smartgrid(db.auth_user,linked_tables=['auth_membership'])
    return locals()

def rows2json (tablename,rows):
    import datetime
    import json
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, datetime.datetime)
        or isinstance(obj, datetime.date)
        else None
        )
    rows = rows.as_list()
    concat = '{ "'+tablename+'": ['
    for row in rows:
        concat = concat + json.dumps(row, default=date_handler)+","
    concat = concat.strip(',')
    concat = concat + ']}'
    return concat

#@auth.requires_login()
@request.restful()
def api():
    response.view = 'generic.json'
    def GET(tablename,*args,**vars): # GET VALUES
        if tablename =='': raise HTTP(400)
        if request.args(1) == None: # use request.arg(1) to get the arg after tablename;
                                    # request.arg(1) is None if empty, don't use args[1] coz raise exeption error
                if request.vars.search == None:
                    rows =  db(db[tablename]).select()
                    data = rows2json(tablename,rows)
                    return  data
                else :
                    rows = db(db.test.testname.contains(vars['search'])).select()
                    data = rows2json(tablename+' search',rows)
                    return data
        table_id = request.args[1]
        rows =  db(db[tablename]._id==table_id).select()
        data = rows2json(tablename+" hello",rows)
        return data
    def DELETE(tablename,record_id):
        if not tablename=='test': raise HTTP(400)
        db(db.test.id == record_id).delete()
        return '*** Deleted row id : '+record_id+' *** '
    def PUT(tablename,record_id,**vars):
        if not tablename=='test': raise HTTP(400)
        if record_id=='': raise HTTP(400)
        db(db.test._id==record_id).update(**vars)
        return '*** Updated row id: '+record_id+' *** '  # db(db.test._id==record_id).update(**vars)
    def POST(tablename,**vars):
        if not tablename=='test': raise HTTP(400)
        ret = db.test.validate_and_insert(**vars)
        return '*** Added row id: '+ str(ret.id) + ' *** ' + 'Error code : ' + str(ret.errors) + ' *** '
    return locals()

@request.restful()
def api_users():
    response.view = 'generic.json' # or 'generic.' + request.extension
    def GET(*args,**vars):
        patterns = [
            "/user[auth_user]",
            "/user/{auth_user.id}",
            "/user/{auth_user.id}/:field",
            "/membership[auth_membership]",
            "/membership/{auth_membership.group_id}/user[auth_user.id]",  # show user with selected membership
            "/membership/{auth_membership.group_id}/user[auth_user.id]/:field"
            ]
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
        else:
            raise HTTP(400)
    def PUT(tablename,record_id,**vars):
        if tablename == 'auth_user':
            db(db.auth_user._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id: '+record_id+' ***  \r\n'
        elif tablename == 'auth_membership':
            db(db.auth_membership._id==record_id).update(**vars)
            return 'Table: '+ tablename +' *** Updated row id: '+record_id+' ***  \r\n'
        else:
            raise HTTP(400)
    def POST(tablename,**vars):
        if tablename == 'auth_user':
            ret = db.auth_user.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id: '+ str(ret.id) + ' *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        elif tablename == 'auth_membership':
            ret = db.auth_membership.validate_and_insert(**vars)
            return 'Table: '+ tablename +' *** Added row id: '+ str(ret.id) + ' *** ' + 'Error code : ' + str(ret.errors) + ' *** \r\n'
        else:
            raise HTTP(400)
    return locals()

# ****    "CRUD users" ******
def update_user():
    record = db.auth_user(request.args(0)) or redirect(URL('patients'))
    form = SQLFORM(db.auth_user, record)
    if form.process().accepted:
       response.flash = 'form accepted'
       redirect(URL('patients'))
    elif form.errors:
       response.flash = 'form has errors'
    return dict(form=form)

def create_user(): # first arg gives group_id
    group = request.args(0) or redirect(URL('patients'))
    form = SQLFORM(db.auth_user)
    if form.process(onvalidation=check_duplicate).accepted:
        response.flash = 'form accepted'
        db.auth_membership.insert(user_id=form.vars.id,group_id=group)
        redirect(URL('home/'+str(group)))
    elif form.errors:
        response.flash = 'Form has errors'
    return dict(form=form)

def check_duplicate(form):
    form.vars.first_name = form.vars.first_name.capitalize()
    form.vars.last_name = form.vars.last_name.capitalize()
    fname = form.vars.first_name
    lname = form.vars.last_name
    dob = form.vars.dob_pid7
    check = db((db.auth_user.first_name==fname)&(db.auth_user.last_name==lname)&(db.auth_user.dob_pid7==dob)).isempty()
    if check is False: # if user with same first_name last_name dob exist, it is a duplicate
        form.errors.first_name = form.errors.last_name = form.errors.dob_pid7 = "Duplicate exist in database"

# ****  "END CRUD users" ******

def test():
    if (request.args(0) == None):
        membership = 2
    else:
        try:
            check_group= db(db.auth_group.id == request.args(0)).isempty()
        except ValueError:
            membership = 2
        else:
            if check_group is True:
                membership = 2
            else:
                membership = request.args(0)
    group = (db(db.auth_group.id == membership).select().first()).role
    return locals()
