from aws_cdk import (
    aws_apigateway as api,
    aws_ecs as ecs,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_lambda,
    core
)
from aws_cdk.aws_lambda import Handler
from aws_cdk.core import Size


class LambdaStack(core.Stack):

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(scope=self,
                           id=f'{id}-vpc',
                           cidr="10.0.8.0/21")

        self.model_bucket = s3.Bucket.from_bucket_name(scope=self,
                                                       id=f'{id}-model-bucket',
                                                       bucket_name='deep-lambda-bucket')

        self.ecs_cluster = ecs.Cluster(self,
                                       id=f'{id}-ecs',
                                       cluster_name='deep-lambda-serving-ecs',
                                       vpc=self.vpc,
                                       container_insights=True)

        ecr_repository = ecr.Repository(scope=self, id=f'deep-lambda-ecr-repo')

        lambda_function = aws_lambda.Function(
            scope=self,
            id='deep-lambda-function',
            vpc=self.vpc,
            runtime=aws_lambda.Runtime.FROM_IMAGE,
            ephemeral_storage_size=Size.gibibytes(2),
            code=aws_lambda.Code.from_ecr_image(repository=ecr_repository),
            handler=Handler.FROM_IMAGE,
            environment={'MODEL_BUCKET_NAME': 'deep-lambda-bucket'}
        )

        self.model_bucket.grant_read(lambda_function)

        rest_api = api.LambdaRestApi(self, "books-api", handler=lambda_function)
        classify = rest_api.root.add_resource("classify")
        classify.add_method("POST")