FROM python:3.10.6

WORKDIR /torblock
COPY . /torblock/

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "torblock.py"]