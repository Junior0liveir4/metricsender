
# 📊 MetricSender

Microsserviço que simula a emissão de métricas de múltiplas aplicações em um cluster Kubernetes via mensagens publicadas no broker RabbitMQ, com objetivo de facilitar o desenvolvimento e testes de **Operators** que fazem controle automático de recursos.

---

## 📌 Visão Geral

- O `MetricSender` envia, a cada 1 minuto, mensagens para tópicos no formato:
  ```
  Metrics.{nome_da_aplicacao}
  ```
- Cada mensagem representa uma solicitação de alocação de recursos (simulando a saída de uma rede neural).
- As mensagens incluem diversos tipos de métricas personalizadas (ex: CPU, memória, GPU...).
- As configurações de aplicações e recursos são definidas via **ConfigMap no YAML** do Kubernetes.
- Também há um script auxiliar `metricreceiver.py`, que escuta os tópicos e exibe as mensagens recebidas, útil para testes e visualização.

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia     | Função                                       |
|----------------|----------------------------------------------|
| `Python`       | Linguagem de desenvolvimento                 |
| `is-wire`      | Comunicação com o RabbitMQ                   |
| `pyyaml`       | Leitura da configuração YAML                 |
| `six`          | Compatibilidade entre versões de Python      |
| `RabbitMQ`     | Broker de mensagens                          |
| `Kubernetes`   | Orquestração e deploy do serviço             |

---

## 📁 Estrutura Esperada do ConfigMap

```yaml
connection:
  uri: "amqp://user:pass@rabbitmq-host"

deployments:
  - name: app1
    metrics:
      cpu: [0.5, 0.8, 1.0]
      memory: [256, 512, 1024]

  - name: app2
    metrics:
      cpu: [0.2, 0.4]
      gpu: [0, 1]
```

> O arquivo YAML é montado no path `/config/metricsender.yaml` no pod.

---

## 🚀 Como Funciona

### Envio de métricas (metricsender.py)

- Lê a configuração do arquivo `metricsender.yaml` montado no pod.
- A cada 60 segundos, envia uma mensagem com valores aleatórios entre os possíveis listados para cada métrica.
- As mensagens são enviadas com metadados no formato:
  ```
  reply_to = nome_da_aplicacao
  metadata = {
    "cpu": "0.5",
    "memory": "512"
  }
  ```

### Recebimento de métricas (metricreceiver.py)

- Se conecta ao mesmo broker.
- Se inscreve nos tópicos `Metrics.*`.
- Exibe as mensagens recebidas no terminal.

---

## 📦 Deploy no Kubernetes

### ✅ Pré-requisitos

- Cluster Kubernetes funcional
- RabbitMQ acessível pelo endereço informado
- Imagem Docker do `metricsender` construída e publicada
- Arquivo de configuração montado via `ConfigMap`

### 🧪 Comando de deploy

```bash
kubectl apply -f metricsender.yaml
```

> O YAML deve conter o `Pod` ou `Deployment`, `ConfigMap`, e as variáveis de ambiente necessárias.

---

## 🐳 Docker

O `Dockerfile` contido no projeto permite a criação da imagem para uso local ou envio a um registry:

```bash
docker build -t labsea/metricsender:latest .
```

---

## 🛠️ Execução Local

### Executar MetricSender:

```bash
export CONFIG_PATH=metricsender.yaml  # ou monte o arquivo corretamente
python metricsender.py
```

### Executar MetricReceiver:

```bash
python metricreceiver.py
```

> Modifique o URI do broker dentro do `metricreceiver.py` ou configure por variável de ambiente se desejar tornar mais flexível.

---

## 🧪 Exemplo de Saída do Receiver

```
========================================
Aplicação: app1
Recursos recebidos:
  - cpu: 0.8
  - memory: 512
========================================
```

---

## 🧠 Aplicações Futuras

Esse microsserviço foi projetado para:

- Simular cargas e requisições para validação de **autoscalers e operators**
- Testes de sistemas de **provisionamento automático**
- Ambientes de aprendizado de máquina com feedback de consumo

---

## ❗ Possíveis Problemas

| Sintoma                        | Causa provável                          |
|-------------------------------|------------------------------------------|
| Mensagens não aparecem        | URI do broker incorreta ou inacessível  |
| ConfigMap não carregado       | Caminho errado ou arquivo mal formatado |
| Falha no Receiver             | Tópico inexistente ou conexão falhou    |

---

## 📬 Contato

Para dúvidas ou sugestões, entre em contato com o time do **LabSEA**.
