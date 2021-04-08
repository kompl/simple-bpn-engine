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
    def update_out_model_object(out_model, **extra_fields):
        for output_model_field, include_extra_model in extra_fields.items():
            setattr(out_model, output_model_field, include_extra_model)
        return out_model

    @abstractmethod
    def create_db_model_object(self, input_model_object, **extra_fields):
        pass

    @abstractmethod
    def create_output_short_model_object(self, raw_data, **extra_fields):
        pass

    @abstractmethod
    def create_output_model_object(self, raw_data, **extra_fields):
        pass

    @abstractmethod
    def create_output_list_model_object(self, raw_data, **extra_fields):
        pass
