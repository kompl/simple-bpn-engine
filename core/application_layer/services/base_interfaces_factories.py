from abc import ABC, abstractmethod


class BaseInterfacesFactory(ABC):

    @property
    @abstractmethod
    def db_model(self):
        return self.db_model

    @property
    @abstractmethod
    def output_model(self):
        return self.output_model

    @property
    @abstractmethod
    def output_short_model(self):
        return self.output_short_model

    @property
    @abstractmethod
    def output_list_model(self):
        return self.output_list_model

    @staticmethod
    def update_out_model_object(out_model, **kwargs):
        for output_model_field, include_extra_model in kwargs.items():
            setattr(out_model, output_model_field, include_extra_model)
        return out_model

    @abstractmethod
    def create_db_model_object(self, input_model_object, *args, **extra_fields):
        pass

    @abstractmethod
    def create_output_short_model_object(self, db_data_object, *args, **kwargs):
        pass

    @abstractmethod
    def create_output_model_object(self, db_data_object, *args, **kwargs):
        pass

    @abstractmethod
    def create_output_list_model_object(self, db_data_object, *args, **kwargs):
        pass
