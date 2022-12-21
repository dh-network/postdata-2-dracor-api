# start by pulling the python image
FROM python:3.9-slim

#set the (default) environment variables
ENV SERVICE_URL="http://localhost"
ENV SERVICE_PORT=5000
ENV SERVICE_DEBUG=FALSE

#create a directory for the api
CMD mkdir /api

# copy the requirements file
COPY ./requirements.txt /api/requirements.txt

# switch working directory
WORKDIR /api

# install the dependencies and packages
RUN pip install -r requirements.txt

# copy local files to container
CMD ls
COPY api.py /api
COPY static /api/static
COPY apidoc.py /api
COPY core.py  /api
COPY queries.py /api

# configure the container to run in an executed manner
ENTRYPOINT [ "python", "/api/api.py" ]