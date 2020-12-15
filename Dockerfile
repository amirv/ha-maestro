ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache python3

COPY ./get-pip.py ./get-pip.py
RUN python3 get-pip.py

copy ./requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt && rm ./requirements.txt

COPY ./musa ./musa
CMD [ "python3", "musa" ]
