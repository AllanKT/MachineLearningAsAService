
FROM python:3.6.8-alpine3.9

LABEL maintainer="AutoIT Stefanini autoit@stefanini.com"

RUN \
  apk update && \
  apk add bash py-pip && \
  apk add --virtual=build gcc libffi-dev musl-dev openssl-dev python-dev make && \
  pip --no-cache-dir install -U pip && \
  pip --no-cache-dir install azure-cli && \
  apk del --purge build

RUN apk add --update \
    supervisor \
    python3-dev \
    build-base \
    linux-headers \
    pcre-dev \
    postgresql-dev \
    gcc 

RUN apk add --no-cache pcre curl

COPY ./requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN mkdir /var/log

EXPOSE 5000

WORKDIR /app
COPY ./app /app

CMD ["python3", "run.py"]

# py run.py -f C:\Users\allan\Desktop\Codes\IESB\TCC\code\app\dataset\prouni-2016-clean.csv -s , -c TIPO_BOLSA
# py run.py -f C:\Users\allan\Desktop\Codes\IESB\TCC\code\app\dataset\iris.csv -s , -c species
# py run.py -f C:\Users\allan\Desktop\Codes\Stefanini\MLaaS\TCC\script\code\app\dataset\titanic.csv -s , -c Survived
