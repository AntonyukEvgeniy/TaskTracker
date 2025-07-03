# Use Python 3.11 slim image
FROM python:3.11-slim
# Set working directory
WORKDIR /app
# Install poetry
RUN pip install poetry
# Copy project files
COPY pyproject.toml poetry.lock* ./
# Configure poetry to not create a virtual environment inside container
RUN poetry config virtualenvs.create false
# Install dependencies
RUN poetry install --only main --no-root --no-interaction --no-ansi
# Copy application code
COPY . .
RUN chmod +x entrypoint.sh
# Command to run migrations
CMD ["python", "manage.py", "migrate"]