def worklist():
    grid = SQLFORM.smartgrid(db.worklist)
    return locals()

def exam2do_OBR4():
    grid = SQLFORM.smartgrid(db.exam2do_OBR4)
    return locals()

def all_users():
    grid = SQLFORM.smartgrid(db.auth_user,linked_tables=['auth_membership','address','phone'])
    return locals()

def modality():
    grid = SQLFORM.smartgrid(db.modality)
    return locals()

def facility():
    grid = SQLFORM.smartgrid(db.facility)
    return locals()
