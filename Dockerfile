FROM python:3.6

EXPOSE 8000

# TODO add your wit token here:
# ENV WIT_TOKEN <TOKEN>


WORKDIR /lobe

COPY ./ /lobe/

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "--chdir", "app/", "server:application", "-b", ":8000", "--log-file=-"]


