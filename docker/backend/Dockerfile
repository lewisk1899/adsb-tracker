FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /data/opensky

# Copy requirements file
COPY backend/ backend/ 

ENTRYPOINT ["python", "backend/get_adsb_data.py"]
#CMD ["sleep", "infinity"]
