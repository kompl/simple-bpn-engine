from authorization.application_layer.interfaces import UserIn, UserOut, TokenOut
from authorization.domain.users_models import UserDB


class UserInterfacesFactory:
    def __init__(self):
        self.db_model = UserDB
        self.out_model = UserOut
        self.in_model = UserIn

    def create_db_model_object(self, **extra_fields):
        return self.db_model(**extra_fields)

    def create_output_model_object(self, **extra_fields):
        return self.out_model(**extra_fields)
