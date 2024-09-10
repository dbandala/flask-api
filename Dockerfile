FROM python:3.12
EXPOSE 5000
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Copy the current directory contents into the container at /app - cache layer
COPY . .
#COPY requirements.txt requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]