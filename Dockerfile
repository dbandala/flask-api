FROM python:3.12
EXPOSE 5000
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install flask
COPY . /app
#COPY requirements.txt requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]