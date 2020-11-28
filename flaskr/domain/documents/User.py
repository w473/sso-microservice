import uuid
import logging
logger = logging.getLogger( __name__ )

class User:

    def __init__(self, doc, id = None):
        self.id = id
        self.username = doc.get('username')
        self.email = doc.get('email')
        self.publicName = doc.get('publicName')
        self.locale = doc.get('locale')
        self.password = doc.get('password')
        self.roles = ['USER']
        self.create = doc.get('create')
        self.isActive = doc.get('isActive')
        self.activationCode = doc.get('activationCode')
    
    def id(self) -> str:
        return str(self.id)

    def setRoles(self, roles: list) -> None:
        self.roles = roles

    def addRole(self, role: str) -> None:
        self.roles.append(role)
    
    def hasRole(self, role: str) -> bool:
        if role in self.roles:
            return True
        else:
            return False

    def setId(self, id) -> None:
        self.id = id

    def setCreate(self, create) -> None:
        self.create = create

    def setActive(self, active) -> None:
        if active == True:
            self.activationCode = None
        elif self.isActive!=active:
            self.activationCode = str(uuid.uuid4())
        self.isActive = active

    def setPassword(self, password) -> None:
        self.password = password

    def toDictResponse(self) -> dict:
        return {
            'username': self.username,
            'email': self.email,
            'publicName': self.publicName,
            'locale': self.locale,
            'roles': self.roles,
            'create': self.create.strftime("%m/%d/%Y, %H:%M:%S"),
            'isActive': self.isActive
        }

    def toDict(self):
        ret = self.toDictResponse()
        ret['password'] = self.password
        ret['activationCode'] = self.activationCode
        ret['create'] = self.create

        if self.id != None:
            ret['_id'] = self.id
        return ret