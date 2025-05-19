FROM python:3.10-slim

# Instala dependências necessárias
RUN pip install --no-cache-dir is-wire pyyaml six

# Define diretório de trabalho
WORKDIR /app

# Copia o script da aplicação
COPY metricsender.py .

# Comando padrão de execução
CMD ["python3", "metricsender.py"]

