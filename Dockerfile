FROM python:3.8

WORKDIR /src/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD [ "python3.8", "/src/controller.py" ]

