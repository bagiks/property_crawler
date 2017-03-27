#!/usr/bin/env python

from argparse import ArgumentParser
import boto3
import os
from Queue import Queue
from threading import Thread
import time

num_fetch_threads = 8
enclosure_queue = Queue()

PATH = "/Volumes/Data/WORKSPACE/git/bagiks/property_crawler/property_crawler/spiders/images/full_crack"
CLEAN_PATH = "/Volumes/Data/WORKSPACE/git/bagiks/property_crawler/property_crawler/spiders/images/full_crack_clean"
DIRTY_PATH = "/Volumes/Data/WORKSPACE/git/bagiks/property_crawler/property_crawler/spiders/images/full_crack_dirty"
endpoint = 'https://rekognition.us-west-2.amazonaws.com'
collection = 'MaxLabels'


def get_client(endpoint):
    client = boto3.client('rekognition', region_name='us-west-2', endpoint_url=endpoint, verify=False,
                          aws_access_key_id='ASIAIWGKCYTDHD5N5NIQ', aws_secret_access_key='73WaSuhDQ7bvGVpEVf5zTMH7GgCP9gIbeBEsVz8O', aws_session_token='FQoDYXdzEN///////////wEaDI35HO8OQQ0G5VC9KyKsAYJdLxJTqYSXDnDzhoTl+n86KsEgqv+dR2xQd1drX6k6av2ngJTcjG2h4HGJnjfH10u9N8SmWQzSlOeRgC14fDs8T7Pn6Pqi+0sNq/m435YkdZmRDsZo545U6X5qUWYgC+CCU7vfRkXH6dTltINN2SfpaioJC/t3CFIofSSmJSZxkd1Fb05DqWz65f7tyF1unBvHDPE5X03FrPffTeK1zs7M1JPx+H5sYxY86j4oytXbxgU=')
    return client

def getLabels(index, q):
    while True:
        print '%s: Looking for the next enclosure' % index
        img_path = q.get()
        print '%s: Downloading:' % index, img_path
        time.sleep(index + 2)
        img = os.path.join(PATH, img_path)
        with open('results.txt', 'a') as myfile:
            with open(img, 'rb') as image:
                response = client.detect_labels(Image={'Bytes': image.read()})
                z = []
                for i in response['Labels']:
                    z += str(i['Name']).lower().split(" ")

                names = [str(i['Name']).lower() for i in response['Labels']]
                myfile.write(img_path + "-" + ",".join(names) + "\n")

                if 'phone' in z or 'screen' in z or 'lcd' in z or 'tablet' in z:
                    os.rename(img, os.path.join(CLEAN_PATH, img_path))
                else:
                    os.rename(img, os.path.join(DIRTY_PATH, img_path))
                    print img_path, z

        myfile.close()
        q.task_done()

client = get_client(endpoint)


for i in range(num_fetch_threads):
    worker = Thread(target=getLabels, args=(i, enclosure_queue,))
    worker.setDaemon(True)
    worker.start()


    # with open('results.txt', 'a') as myfile:
for img in os.listdir(PATH):
    if "jpg" not in img:
        continue
    enclosure_queue.put(img)

print '*** Main thread waiting'
enclosure_queue.join()
print '*** Done'
