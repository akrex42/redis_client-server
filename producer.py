import json
import random
import redis
import logging


def create_redis_connection():

    producer_r = redis.StrictRedis(host='localhost', db=0)
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    return producer_r


def publish(prod):

    i = 0
    while True:
        data_set = {"metadata": {"from": str(1000000000 + i),
                                 "to": str(1000000000 + i + 1)},
                    "amount": str(random.randint(-10000000000, 10000000000))}
        logging.info("SENDER: " + data_set["metadata"]["from"] + " RECEIVER: " + data_set["metadata"]["to"])
        i += prod.publish('payload', json.dumps(data_set))
        if i == 10:
            break


if __name__ == "__main__":

    producer = create_redis_connection()
    publish(producer)
