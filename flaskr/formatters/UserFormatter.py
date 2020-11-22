
def forApiAsDict(docList):
    ret = {}
    for doc in docList:
        ret[str(doc.id)] = {
            'id': doc.id,
            'username': doc.username,
            'email': doc.email,
            'name': doc.name,
            'locale': doc.locale,
            'roles': doc.roles,
            'create': doc.create,
            'isEnabled': doc.isEnabled
        }
    return ret