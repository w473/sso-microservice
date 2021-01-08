class RefreshToken:
    def __init__(self, userId, token):
        """
        docstring
        """
        self.userId = userId
        self.token = token

    def toDict(self):
        return {
            'id': self.token,
            'userId': self.userId
        }
