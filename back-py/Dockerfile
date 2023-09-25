FROM python:3.9-slim


RUN mkdir gen
COPY requirements.txt gen/requirements.txt
RUN pip install -r gen/requirements.txt

COPY server.py /gen/server.py
COPY stats.json /gen/stats.json
ADD /src /gen/src


WORKDIR /gen

ENV PORT: 8085

CMD ["python", "-u", "server.py"]