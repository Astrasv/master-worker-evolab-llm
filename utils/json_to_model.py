
from pydantic import BaseModel

from typing import Dict
def json_to_model(json_data: Dict, model_class):

    try:
        return model_class.model_validate(json_data)
    except Exception as e:
        raise ValueError(f"Error parsing JSON to {model_class.__name__}: {e}")