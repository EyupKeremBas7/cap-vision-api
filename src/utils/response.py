
from sdks.novavision.src.helper.package import PackageHelper
from capsules.VisionApi.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, VisionApiOutputs, VisionApiResponse, VisionApiExecutor, OutputDetection


def build_response(context):
    outputImage = OutputDetection(value=context.image)
    Outputs = VisionApiOutputs(outputImage=outputImage)
    packageResponse = VisionApiResponse(outputs=Outputs)
    packageExecutor = VisionApiExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel