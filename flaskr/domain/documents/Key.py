class Key:
    id = None
    publicKey = None
    privateKey = None
    algorithm = None

    def __init__(self, publicKey, privateKey, algorithm, id = None):
        """
        docstring
        """
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.algorithm = algorithm
        self.id = id

    def toDict(self):
        return {
            'publicKey': self.publicKey,
            'privateKey': self.privateKey,
            'algorithm': str(self.algorithm)
        }

    def setId(self, id):
        self.id = id