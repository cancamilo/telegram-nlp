import websocket
import time
import rel
import json
# from kafka import KafkaProducer

# Define the WebSocket URL and Kafka topic name
WEBSOCKET_URL = "wss://ws-feed.exchange.coinbase.com"                
KAFKA_TOPIC = "my-topic"

subscription_message = '{"type": "subscriptions", "channels": [{"name": "ticker","product_ids": ["ETH-USD"]}]}'
subscription_message = '{"type": "subscribe", "product_ids": ["ETH-USD"], "channels": ["ticker"]}'

# Connect to Kafka
# producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Define a callback function to handle incoming WebSocket messages

class EventHandler():

    def __init__(self, max_count) -> None:
        self.counter = 0
        self.max_count = max_count

    def on_message(self, ws, message):
        # Convert the message to bytes and send it to Kafka
        # producer.send(KAFKA_TOPIC, bytes(message, 'utf-8'))
        if self.counter < self.max_count:            
            self.counter +=1
            return
        
        self.counter = 0
        print("=====================================================")
        print(message)

    # Define a callback function to handle the WebSocket connection opening
    def on_open(self, ws):
        # Send the subscription message to the server
        print("opening websocket...")
        ws.send(subscription_message)
        print("subscription message sent.")

    def on_close(self, ws):
        print("closing websocket...")
        close_message = {
            "type": "unsubscribe",
            "channels": [
                "level2"
                "heartbeat",
                "ticker"
            ]
        }

        ws.send(close_message)

    def on_error(self, ws, error):
        print("error occurred.....")

if __name__ == "__main__":
    counter = 0
    # websocket.enableTrace(True)
    handler = EventHandler(10)
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL, 
        on_message=handler.on_message,
        on_open=handler.on_open,
        on_close=handler.on_close,
        on_error=handler.on_error,     
    )

    websocket.setdefaulttimeout(5)

    # Start the WebSocket connection and wait for incoming messages
    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
