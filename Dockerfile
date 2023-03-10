FROM public.ecr.aws/lambda/python:3.8 as base

FROM base

COPY requirements.txt .
RUN  pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY app.py "${LAMBDA_TASK_ROOT}"
COPY tagger.py "${LAMBDA_TASK_ROOT}"

ENV PYTHONPATH="${LAMBDA_TASK_ROOT}"

CMD ["app.lambda_handler"]