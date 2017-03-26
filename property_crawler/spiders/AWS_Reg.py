#!/usr/bin/env python

from argparse import ArgumentParser
import boto3
import json
from os import environ
import os

def get_client(endpoint):
    # key_id = environ.get('ASIAIWGKCYTDHD5N5NIQ')
    # secret_key = environ.get('73WaSuhDQ7bvGVpEVf5zTMH7GgCP9gIbeBEsVz8O')
    # token = environ.get('FQoDYXdzEN///////////wEaDI35HO8OQQ0G5VC9KyKsAYJdLxJTqYSXDnDzhoTl+n86KsEgqv+dR2xQd1drX6k6av2ngJTcjG2h4HGJnjfH10u9N8SmWQzSlOeRgC14fDs8T7Pn6Pqi+0sNq/m435YkdZmRDsZo545U6X5qUWYgC+CCU7vfRkXH6dTltINN2SfpaioJC/t3CFIofSSmJSZxkd1Fb05DqWz65f7tyF1unBvHDPE5X03FrPffTeK1zs7M1JPx+H5sYxY86j4oytXbxgU=')
    # if not key_id or not secret_key or not token:
    #     raise Exception('Missing AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, or AWS_SESSION_TOKEN')
    client = boto3.client('rekognition', region_name='us-west-2', endpoint_url=endpoint, verify=False,
                          aws_access_key_id='ASIAIWGKCYTDHD5N5NIQ', aws_secret_access_key='73WaSuhDQ7bvGVpEVf5zTMH7GgCP9gIbeBEsVz8O', aws_session_token='FQoDYXdzEN///////////wEaDI35HO8OQQ0G5VC9KyKsAYJdLxJTqYSXDnDzhoTl+n86KsEgqv+dR2xQd1drX6k6av2ngJTcjG2h4HGJnjfH10u9N8SmWQzSlOeRgC14fDs8T7Pn6Pqi+0sNq/m435YkdZmRDsZo545U6X5qUWYgC+CCU7vfRkXH6dTltINN2SfpaioJC/t3CFIofSSmJSZxkd1Fb05DqWz65f7tyF1unBvHDPE5X03FrPffTeK1zs7M1JPx+H5sYxY86j4oytXbxgU=')
    return client

def get_args():
    parser = ArgumentParser(description='Call index faces')
    parser.add_argument('-e', '--endpoint')
    parser.add_argument('-i', '--image')
    parser.add_argument('-c', '--collection')
    return parser.parse_args()

if __name__ == '__main__':
    # args = get_args()
    PATH = "/Volumes/Data/WORKSPACE/git/bagiks/property_crawler/property_crawler/spiders/images/full_iphone"
    CLEAN_PATH = "/Volumes/Data/WORKSPACE/git/bagiks/property_crawler/property_crawler/spiders/images/full_iphone_clean"
    DIRTY_PATH = "/Volumes/Data/WORKSPACE/git/bagiks/property_crawler/property_crawler/spiders/images/full_iphone_dirty"
    endpoint = 'https://rekognition.us-west-2.amazonaws.com'
    img = '/Volumes/Data/Dropbox (Personal)/phone/ebay da loc/phone_22 copy/ff437b51fa03c01add2d74e48c9d02d5bed9ea00.jpg'
    collection = 'MaxLabels'
    client = get_client(endpoint)
    print client

    with open('results.txt', 'a') as myfile:
        for j in os.listdir(PATH):
            if "jpg" not in j:
                continue
            img = os.path.join(PATH, j)
            with open(img, 'rb') as image:
                response = client.detect_labels(Image={'Bytes': image.read()})
                z = []
                for i in response['Labels']:
                    z += str(i['Name']).lower().split(" ")

                names = [str(i['Name']).lower() for i in response['Labels']]
                myfile.write(j + "-" + ",".join(names) + "\n")


                if 'phone' in z or 'screen' in z or 'lcd' in z or 'tablet' in z:
                    os.rename(img, os.path.join(CLEAN_PATH, j))
                else:
                    os.rename(img, os.path.join(DIRTY_PATH, j))
                    print j, z

    myfile.close()

            # names = [ str(i['Name']).lower() for i in response['Labels']]

            # if "phone"  in " ".join(names) or 'tablet' in " ".join(names):
            #     os.rename(img, os.path.join(CLEAN_PATH, j))