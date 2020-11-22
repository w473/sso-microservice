
def forApiAsDict(docList):
    ret = {}
    for doc in docList:
        ret[str(doc.id)] = doc.publicKey
    return ret