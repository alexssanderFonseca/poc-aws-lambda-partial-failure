import logging
from random import randint

logging.basicConfig(level=logging.INFO, force=True)


def lambda_handler(event, context):
    messages_to_reprocess = []
    batch_failures_response = {}
    records = event['Records']
    logging.info(f"Batch size : {len(records)}")
    for record in records:
        payload = record["body"]
        logging.info(f"Message {payload} received")
        try:
            simulate_api_request_random_failure(record)
            logging.info("Message processed")
        except Exception:
            logging.info("Failed to process the message")
            messages_to_reprocess.append({"itemIdentifier": record["messageId"]})
    logging.info(f"Messages to reprocess: {messages_to_reprocess} ")
    batch_failures_response["batchItemFailures"] = messages_to_reprocess
    return batch_failures_response


def simulate_api_request_random_failure(record):
    number = randint(1, 3)
    receivecount = int(record["attributes"]["ApproximateReceiveCount"])
    logging.info(f"This message was received {receivecount} time")
    if receivecount < 3 and number % 2 != 0:
        raise Exception("The api requested is having some problems at the moment")
