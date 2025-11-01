class Repository:
    model = None

    def __init__(self, session):
        self.session = session

    def get(self, id):
        return self.session.get(self.model, id)

    def create(self, **data):
        obj = self.model(**data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
