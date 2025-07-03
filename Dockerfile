FROM python:3.9
WORKDIR /app
COPY requirements.txt .
COPY config.py .
COPY fetcher.py .
RUN python -m venv --copies /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt
ENV NIXPACKS_PATH=/opt/venv/bin:$NIXPACKS_PATH
CMD ["/opt/venv/bin/python", "fetcher.py"]
