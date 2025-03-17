FROM public.ecr.aws/lambda/python:3.9

WORKDIR /var/task

COPY src/lambda.py src/requirements.txt ./

RUN pip install -r requirements.txt --target .

CMD ["lambda.lambda_handler"]