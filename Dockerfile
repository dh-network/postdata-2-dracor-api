# start by pulling the python image
FROM python:3.9-slim

#set the (default) environment variables
ENV SERVICE_URL="http://localhost"
ENV SERVICE_PORT=5000
ENV SERVICE_DEBUG=FALSE

# copy the requirements file
COPY ./requirements.txt /api/requirements.txt

# switch working directory
WORKDIR /api

# install the dependencies and packages
RUN pip install -r requirements.txt

# copy local files to container
COPY ./static /api/static
COPY ./apidoc.py /api/apidoc.py
COPY ./core.py  /api/core.py
COPY ./queries.py /api/queries.py

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["api.py" ]