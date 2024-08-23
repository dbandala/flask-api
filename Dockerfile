FROM python:3.12
EXPOSE 5000
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#COPY requirements.txt requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]