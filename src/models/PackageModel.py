from pydantic import Field,field_validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @field_validator("type", pre=True, always=True)
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


class ConfigGoogleToken(Config):
    """
    Google API token'ı için config ayarı. Bu token, Google servislerine erişim için gereklidir.
    """
    name: Literal["GoogleToken"] = "GoogleToken"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Google API Token"


class ConfigDeviceGPU(Config):
    name: Literal["ConfigDeviceGPU"] = "ConfigDeviceGPU"
    value: Literal["GPU"] = "GPU"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "GPU"


class ConfigDeviceCPU(Config):
    name: Literal["ConfigDeviceCPU"] = "ConfigDeviceCPU"
    value: Literal["CPU"] = "CPU"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "CPU"


class ConfigDevice(Config):
    """
    It refers to whether the model should run on a CPU or a GPU.
    You can select the device type for inference or training process.
    """
    name: Literal["ConfigDevice"] = "ConfigDevice"
    value: Union[ConfigDeviceCPU, ConfigDeviceGPU]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Device"


class VisionAPIConfigs(Configs):
    configGoogleToken: ConfigGoogleToken
    configDevice: ConfigDevice


class VisionAPIOutputs(Outputs):
    outputDetection: OutputDetection


class VisionAPIRequest(Request):
    inputs: Optional[VisionAPIInputs]
    configs: VisionAPIConfigs
    
    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class VisionAPIResponse(Response):
    outputs: VisionAPIOutputs


class VisionAPIExecutor(Config):
    name: Literal["VisionAPI"] = "VisionAPI"
    value: Union[VisionAPIRequest, VisionAPIResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Vision API"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: VisionAPIExecutor
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
    name: Literal["VisionAPI"] = "VisionAPI"
