import uuid

class User:
    # username = None
    # email = None
    # name = None
    # locale = None
    # password = None
    # roles = None
    # create = None
    # activationCode = None


    def __init__(self, doc, id = None):
        self.id = id
        self.username = doc.get('username')
        self.email = doc.get('email')
        self.name = doc.get('name')
        self.locale = doc.get('locale')
        self.password = doc.get('password')
        self.roles = ['USER']
        self.create = doc.get('create')
        self.isActive = doc.get('isActive')
        self.activationCode = doc.get('activation_code')
    
    def id(self) -> str:
        return str(self.id)

    def setRoles(self, roles) -> None:
        self.roles = roles
    
    def hasRole(self, role: str) -> bool:
        if role in self.roles:
            return True
        else:
            return False

    def setId(self, id) -> None:
        self.id = id

    def setCreate(self, create) -> None:
        self.create = create
        self.id = id

    def setActive(self, active) -> None:
        if active == False and self.isActive!=active:
            self.activationCode = str(uuid.uuid4())
        self.isActive = active
    
    def isActive(self) -> bool:
        return self.isActive

    def setPassword(self, password) -> None:
        self.password = password

    def toDictResponse(self) -> dict:
        return {
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'locale': self.locale,
            'roles': self.roles,
            'create': self.create.strftime("%m/%d/%Y, %H:%M:%S"),
            'isActive': self.isActive
        }

    def toDict(self):
        ret = self.toDictResponse()
        ret['password'] = self.password
        ret['activationCode'] = self.activationCode

        if self.id != None:
            ret['_id']: self.id
        return ret