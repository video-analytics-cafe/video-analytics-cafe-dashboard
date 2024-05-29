
FROM python:3.9-slim AS build

# Set the working directory in the container
WORKDIR /usr/src/app


# add and install requirements
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install seaborn
RUN pip install matplotlib
RUN pip install altair


# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Define environment variable
ENV NAME SL_DB

# 



# Run streamlit
CMD python -m streamlit run project/app.py