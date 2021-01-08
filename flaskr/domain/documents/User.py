class User:

    def __init__(self, doc):
        self.id = doc.get('id')
        self.longName = doc.get('longName')
        self.email = doc.get('email')
        self.username = doc.get('username')
        self.locale = doc.get('locale')
        self.roles = doc.get('roles')
        self.isActive = doc.get('isActive')

    def id(self) -> str:
        return str(self.id)

    def hasRole(self, role: str) -> bool:
        if role in self.roles:
            return True
        else:
            return False

    def toDict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'longName': self.longName,
            'locale': self.locale,
            'roles': self.roles,
            'isActive': self.isActive
        }
