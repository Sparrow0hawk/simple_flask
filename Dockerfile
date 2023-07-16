FROM python:3.10-slim 

RUN useradd -m app 

USER app

WORKDIR /app
COPY --chown=app . /app

EXPOSE 5000

ENV PATH="/home/app/.local/bin:${PATH}"

RUN python -m pip install .[prod]

RUN flask --app simple_flask init-db

CMD ["gunicorn","-w","4", "--bind", "0.0.0.0:5000", "simple_flask:create_app()"]
