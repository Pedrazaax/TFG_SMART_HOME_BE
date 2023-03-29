import logging
from tuya_connector import TUYA_LOGGER, TuyaOpenPulsar, TuyaCloudPulsarTopic
from properties import ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT

# Enable debug log
TUYA_LOGGER.setLevel(logging.DEBUG)

# Init Message Queue
open_pulsar = TuyaOpenPulsar(
    ACCESS_ID, ACCESS_KEY, MQ_ENDPOINT, TuyaCloudPulsarTopic.PROD
)
# Add Message Queue listener
open_pulsar.add_message_listener(lambda msg: print(f"---\nexample receive: {msg}"))

# Start Message Queue
open_pulsar.start()

input()
# Stop Message Queue
open_pulsar.stop()
