from authorization.application_layer.interfaces import UserIn, UserOut, TokenOut
from authorization.domain.models import UserDB


class UserInterfacesFactory:
    def __init__(self):
        self.db_model = UserDB
        self.out_model = UserOut
        self.in_model = UserIn

    def create_db_model(self, **extra_fields):
        return self.db_model(**extra_fields)
