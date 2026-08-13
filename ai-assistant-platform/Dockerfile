FROM python:3.12-slim-trixie

# Python & UV optimization flags
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_DEV=1

# Install uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

WORKDIR /app

# Create non-root user and give ownership of /app
RUN useradd --create-home appuser && chown appuser:appuser /app
USER appuser

# Copy dependency definition files first to leverage Docker layer caching
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Install dependencies without installing the project code yet
RUN uv sync --frozen --no-install-project --no-cache

# Copy the rest of the project source code
COPY --chown=appuser:appuser . .

# Complete synchronization (install the project itself)
RUN uv sync --frozen --no-cache

# Expose port 8001
EXPOSE 8001

CMD ["uv", "run", "uvicorn", "ai_assistant_platform.main:app", "--host", "0.0.0.0", "--port", "8001"]