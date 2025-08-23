
from sdks.novavision.src.helper.package import PackageHelper
from capsules.VisionApi.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, VisionApiOutputs, VisionApiResponse, VisionApiExecutor, OutputDetection


def build_response(context):
    outputDetection = OutputDetection(value=context.text)
    outputs = VisionApiOutputs(outputDetection=outputDetection)
    packageResponse = VisionApiResponse(outputs=outputs)
    packageExecutor = VisionApiExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
