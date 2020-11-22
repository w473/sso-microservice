class RefreshToken:
    def __init__(self, userId, token):
        """
        docstring
        """
        self.userId = userId
        self.token = token

    def toDict(self):
        return {
            '_id': self.token,
            'userId': self.userId
        }
