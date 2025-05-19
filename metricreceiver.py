from is_wire.core import Channel, Subscription, Message
import time
import os

# Permite configurar a URI do broker via variável de ambiente
broker_uri = "amqp://rabbitmq:30000"

# Conecta ao broker
channel = Channel(broker_uri)

# Inscreve-se no padrão genérico para todos os deployments
subscription = Subscription(channel)
subscription.subscribe(topic="Metrics.*")

print("Aguardando mensagens dos tópicos Metrics.*...")

while True:
    try:
        message = channel.consume()
        application = message.reply_to
        parameters = message.metadata

        print("=" * 40)
        print(f"Aplicação: {application}")
        print(f"Recursos recebidos:")
        for key, value in parameters.items():
            print(f"  - {key}: {value}")
        print("=" * 40)
    except KeyboardInterrupt:
        print("Encerrando listener.")
        break
    except Exception as e:
        print(f"Erro ao consumir mensagem: {e}")
    time.sleep(1)
