FROM python
LABEL maintainer "Darwin Salinas <salinash2000@gmail.com>"
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r disponibilidad/requirements.txt
CMD ["python", "disponibilidad/app.py"]