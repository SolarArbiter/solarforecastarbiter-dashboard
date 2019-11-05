FROM python:3.7
RUN git clone https://github.com/SolarArbiter/solarforecastarbiter-api.git
WORKDIR solarforecastarbiter-api
RUN pip install -r requirements.txt
RUN pip install .
RUN git clone https://github.com/SolarArbiter/solarforecastarbiter-core.git
WORKDIR solarforecastarbiter-core
RUN pip install -r requirements.txt
RUN pip install .
