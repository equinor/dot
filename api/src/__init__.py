from pydantic import BaseModel, ConfigDict

from src.common.logger import set_up_logger

set_up_logger(__name__)


class DOTModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    @classmethod
    def convert_api_payload_to_response(cls, data):
        try:
            return cls.model_validate(data.model_dump())
        except Exception as e:
            raise Exception(
                f"Cannot validate the API payload into a data model response: {e}"
            )

    @classmethod
    def convert_list_api_payloads_to_responses(cls, data):
        try:
            return [cls.model_validate(v.model_dump()) for v in data]
        except Exception as e:
            raise Exception(
                f"Cannot validate the API payload into a data model response: {e}"
            )
