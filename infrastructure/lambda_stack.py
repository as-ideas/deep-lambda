from aws_cdk import (
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_lambda,
    core
)
from aws_cdk.aws_lambda import FunctionUrlAuthType


class LambdaStack(core.Stack):

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(scope=self,
                           id=f'{id}-vpc',
                           cidr='10.0.8.0/21',
                           nat_gateways=1)

        self.model_bucket = s3.Bucket.from_bucket_name(scope=self,
                                                       id=f'{id}-model-bucket',
                                                       bucket_name='deep-lambda')

        self.ecr_repository = ecr.Repository.from_repository_name(scope=self, id='deep-lambda-ecr-repo',
                                                                  repository_name=f'deep-lambda')

        self.lambda_function = aws_lambda.Function(
            scope=self,
            id='deep-lambda-function',
            vpc=self.vpc,
            memory_size=8384,
            runtime=aws_lambda.Runtime.FROM_IMAGE,
            code=aws_lambda.Code.from_ecr_image(self.ecr_repository, cmd=['app.lambda_handler']),
            handler=aws_lambda.Handler.FROM_IMAGE,
            ephemeral_storage_size=core.Size.gibibytes(2),
            timeout=core.Duration.minutes(5),
            environment={'PYTORCH_TRANSFORMERS_CACHE': '/tmp/'},
        )

        self.lambda_function.add_function_url(auth_type=FunctionUrlAuthType.NONE)
        self.model_bucket.grant_read(self.lambda_function)
        self.ecr_repository.grant_pull(self.lambda_function)