from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        
    class Config:
        title = "Image"


class OutputDetection(Output):
    name: Literal["outputDetection"] = "outputDetection"

    value: list
    type: Literal["list"] = "list"
    class Config:
        title = "Detection"


class VisionAPIInputs(Inputs):
    inputImage: InputImage


class ConfigGoogleToken(Config):
    name: Literal["GoogleToken"] = "GoogleToken"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Google API Token"


class VisionApiConfigs(Configs):
    configGoogleToken: ConfigGoogleToken

class VisionApiOutputs(Outputs):
    outputDetection: OutputDetection


class VisionApiRequest(Request):
    inputs: Optional[VisionAPIInputs]
    configs: VisionApiConfigs
    
    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class VisionApiResponse(Response):
    outputs: VisionApiOutputs


class VisionApiExecutor(Config):
    name: Literal["VisionApi"] = "VisionApi"
    value: Union[VisionApiRequest, VisionApiResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Vision Api"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[VisionApiExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["capsule"] = "capsule"
    name: Literal["VisionApi"] = "VisionApi"
