FROM public.ecr.aws/lambda/python:3.8 as base

FROM base

COPY requirements.txt .
RUN  pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY app.py "${LAMBDA_TASK_ROOT}"
COPY ner "${LAMBDA_TASK_ROOT}/ner"

ENV PYTHONPATH="${LAMBDA_TASK_ROOT}"

CMD ["app.lambda_handler"]