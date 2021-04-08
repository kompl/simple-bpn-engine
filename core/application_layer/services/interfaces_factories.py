from fastapi_async_db_utils.base_interfaces_factories import BaseInterfacesFactory
from core.domain_layer.core_models import BoardDB
from core.application_layer.output_models import BoardOut
from core.application_layer.input_models import BoardIn


class BoardInterfacesFactory(BaseInterfacesFactory):
    db_model = BoardDB
    output_model = BoardOut
    output_short_model = BoardOut
    output_list_model = BoardOut

    def create_db_model_object(self, input_model_object: BoardIn, *args, **extra_fields):
        return self.db_model(**{
            'name': input_model_object.name,
            'description': input_model_object.description
        }, **extra_fields)

    def create_output_short_model_object(self, raw_data, **extra_fields):
        return self.output_model(**{
            "uuid": raw_data["boards.uuid"],  # boards.uuid
            "name": raw_data["boards.name"],  # boards.name
            "description": raw_data["boards.description"],  # boards.description
        })

    def create_output_model_object(self, raw_data, **extra_fields):
        return self.output_model(**{
            "uuid": raw_data["boards.uuid"],  # boards.uuid
            "name": raw_data["boards.name"],  # boards.name
            "description": raw_data["boards.description"],  # boards.description
            "user_uid": raw_data["users.uid"]  # users.uid
        })

    def create_output_list_model_object(self, raw_data, *args, **extra_fields):
        return self.output_model(**{
            "uuid": raw_data["boards.uuid"],  # boards.uuid
            "name": raw_data["boards.name"],  # boards.name
            "description": raw_data["boards.description"],  # boards.description
        })
