from aws_cdk import core
from lambda_stack import LambdaStack

app = core.App()

lambda_stack = LambdaStack(app, id='deep-lambda-stack')

app.synth()