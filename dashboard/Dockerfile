FROM python:3.12

RUN apt-get update && apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY aurora_map.py .
COPY azimuth_plot.py .
COPY hold.py .
COPY load_dashboard_data.py .
COPY nasa_pipeline.py .
COPY Homepage.py .
COPY pages ./pages/
COPY images ./images/
COPY shapefile ./shapefile/
COPY extract.py .
COPY api_error.py .

EXPOSE 8501

CMD ["streamlit", "run", "Homepage.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]