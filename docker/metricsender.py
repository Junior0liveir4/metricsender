import time
import random
import yaml
from is_wire.core import Channel, Message

# Caminho fixo onde o ConfigMap será montado no container
CONFIG_PATH = "/config/metricsender.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def create_channel(uri):
    return Channel(uri)

def send_metrics(channel, deployments):
    for deploy in deployments:
        name = deploy["name"]
        metrics = deploy["metrics"]
        topic = f"Metrics.{name}"
        params = {}

        for metric, values in metrics.items():
            params[metric] = f"{random.choice(values)}"

        message = Message()
        message.metadata = params
        message.reply_to = name
        channel.publish(message, topic=topic)
        print(f"Sent to {topic}: {params}")

if __name__ == "__main__":
    config = load_config()
    channel = create_channel(config["connection"]["uri"])

    while True:
        send_metrics(channel, config["deployments"])
        time.sleep(60)
