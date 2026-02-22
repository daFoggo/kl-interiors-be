FROM python:slim

WORKDIR /app

# Khởi tạo và sử dụng venv trong Docker
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app

COPY ./requirements.txt /app/requirements.txt

# Cài đặt các requirements bằng pip đã được upgrade
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app/app

# expose port
EXPOSE 8000

# Chạy server
CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]
