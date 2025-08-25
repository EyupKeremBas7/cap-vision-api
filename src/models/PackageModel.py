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
    value: str
    type: Literal["string"] = "string"
    class Config:
        title = "Detection"


class VisionAPIInputs(Inputs):
    inputImage: InputImage

class StorageSource(Config):
    """
        Is corresponds to path of the video.
    """
    name: Literal["storageSource"] = "storageSource"
    value: int
    type: Literal["number"] = "number"
    field: Literal["filePicker"] = "filePicker"

    class Config:
        json_schema_extra = {
            "class": "portalium\\storage\\widgets\\FilePicker",
            "options": {
                "multiple": 0,
                "returnAttribute": [
                    "name"
                ],
                "name": "app::logo_wide"
            }
        }
        title = "Storage Source"

class ConfigStorage(Config):
    name: Literal["ConfigStorage"] = "ConfigStorage"
    storageSource: StorageSource
    value: Literal["ConfigStorage"] = "ConfigStorage"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Storage"

class StoragePath(Config):
    name: Literal["StoragePath"] = "StoragePath"
    value: str
    type: Literal["string"] = "string"
    field: Literal["filePicker"] = "filePicker"
    class Config:
        title = "Storage Path"
class ConfigPath(Config):
    """
        Put your client_secret.json file to your local applications storage
    """
    name: Literal["ConfigPath"] = "ConfigPath"
    storagePath: StorageSource
    value: Literal["ConfigPath"] = "ConfigPath"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Storage"

class TokenSelection(Config):
    """
        Controls whether frames follow the flow sequence.
    """
    name: Literal["TokenSelection"] = "TokenSelection"
    value: Union[ConfigPath,ConfigStorage ]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Flow Rate"


class VisionApiConfigs(Configs):
    TokenSelection: TokenSelection


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
