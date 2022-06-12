FROM python:3.8.9
WORKDIR /server
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8000
EXPOSE 2004