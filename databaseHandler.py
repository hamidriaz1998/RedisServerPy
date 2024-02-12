class Database:
    def __init__(self):
        self.DB = {}

    def set(self, key, value):
        self.DB[key] = value

    def get(self, key):
        return self.DB.get(key)

    def delete(self, key):
        if key in self.DB:
            del self.DB[key]
