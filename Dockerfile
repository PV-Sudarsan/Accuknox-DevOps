FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        cowsay \
        fortune-mod \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/games:${PATH}"
ENV PORT="4499"

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY wisecow.sh /app/wisecow.sh

RUN chmod 0755 /app/wisecow.sh \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 4499

CMD ["/app/wisecow.sh"]
