# Use a smaller Debian base for reproducible builds
FROM debian:bookworm-slim

# Install necessary packages and clean up apt lists to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    fortune \
    cowsay \
    netcat-openbsd \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Add /usr/games to PATH (fortune/cowsay location on Debian)
ENV PATH="/usr/games:${PATH}"

# Create app user for improved security
RUN useradd -m -d /home/appuser appuser

# Set the working directory
WORKDIR /app

# Copy application files
COPY wisecow.sh /app/wisecow.sh
COPY log_file_analyzer.py /app/log_file_analyzer.py
COPY system_health_monitor.py /app/system_health_monitor.py

# Make the script executable
RUN chmod +x /app/wisecow.sh

# Use non-root user
USER appuser

# Expose the port the server will run on
EXPOSE 4499

# Run the wisecow server
CMD ["/app/wisecow.sh"]
