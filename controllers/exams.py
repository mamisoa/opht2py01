# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


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

def topography():
    id_auth_user = request.vars.id_auth_user
    id_worklist = request.vars.id_worklist
    return locals()

def tono():
    id_auth_user = request.vars.id_auth_user
    id_worklist = request.vars.id_worklist
    return locals()

def rx():
    id_auth_user = request.vars.id_auth_user
    id_worklist = request.vars.id_worklist
    opto_far = XML(rows2json('content',db(db.optotype.distance == 'far').select(db.optotype.opto)))
    opto_int = XML(rows2json('content',db(db.optotype.distance == 'intermediate').select(db.optotype.opto)))
    opto_close = XML(rows2json('content',db(db.optotype.distance == 'close').select(db.optotype.opto)))
    return locals()
