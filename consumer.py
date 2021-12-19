import redis
import time
import argparse
import json


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="enter the sender and receiver accounts", type=str)
    args = parser.parse_args()

    if args.e:
        bad_guys = str(args.e).split(",")
    else:
        raise ValueError
    return bad_guys


def print_logs(queue, bad_guys):

    for log in queue:
        for bad_guy in bad_guys:
            if log and log["metadata"]["to"] == bad_guy and int(log["amount"]) >= 0:
                log["metadata"]["to"], log["metadata"]["from"] =\
                    log["metadata"]["from"], log["metadata"]["to"]
        print(log)


def create_queue_log():

    queue = []

    consumer_r = redis.StrictRedis(host='localhost', db=0)
    consumer_p = consumer_r.pubsub(ignore_subscribe_messages=True)
    consumer_p.subscribe('payload')

    time.sleep(1)

    while True:
        new_data = consumer_p.get_message()
        if new_data is not None:
            queue.append(json.loads(new_data["data"].decode("utf-8")))
        if len(queue) == 10:
            break
    return queue


if __name__ == "__main__":

    bad_guys_list = parse_args()
    queue_log = create_queue_log()
    print_logs(queue_log, bad_guys_list)
