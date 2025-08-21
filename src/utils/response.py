
from sdks.novavision.src.helper.package import PackageHelper
from capsules.VisionAPI.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, VisionAPIOutputs, VisionAPIResponse, VisionAPI, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    Outputs = VisionAPI(outputImage=outputImage)
    packageResponse = VisionAPIResponse(outputs=Outputs)
    packageExecutor = VisionAPI(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel