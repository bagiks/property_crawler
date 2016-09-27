# import pymongo
#
# class S3Downloader(object):
#     AWS_ACCESS_KEY_ID = None
#     AWS_SECRET_ACCESS_KEY = None
#     MONGODB_SERVER = "52.26.39.74"
#     MONGODB_PORT = 27017
#     MONGODB_DB = "bagiks"
#     MONGODB_COLLECTION= "property_full"
#
#     POLICY = 'private'
#
#     HEADERS = {
#         'Cache-Control': 'max-age=172800'
#     }
#
#     def __init__(self):
#         dbConnection = pymongo.MongoClient(
#             self.MONGODB_SERVER,
#             self.MONGODB_PORT
#         )
#         db = dbConnection[self.MONGODB_DB]
#         self.collection = db[self.MONGODB_COLLECTION]
#
#
# if __name__ == '__main__':
#     downloader = S3Downloader()
#     print downloader.collection.count()

import pymongo
import boto3
import os

if __name__ == '__main__':
    conn = pymongo.MongoClient('52.26.39.74', 27017)
    db = conn['bagiks']
    collection = db['property_full']
    print collection.count()

    categories = [
        # "Microwaves",
        # "Appliances",
        # "Blenders, Juicers & Food processors",
        # "Coffee Machines",
        # "Washing Machines & Dryers",
        # "Cooktops & Rangehoods",
        # "Ovens",
        # "Dishwashers",
        # "Vacuum Cleaners",
        # "Air Conditioning & Heating",
        # "Sewing Machines",
        # "Fridges & Freezers",
        # "Small Appliances",
        # "Other Appliances",
        # "TVs",
        # "Home Theatre Systems",
        # "TV Accessories",
        # "Other TV & DVD Players",
        # "DVD Players",
        # "TV & DVD players",
        # "Table & Desk Lamps",
        # "Ceiling Lights",
        # "Floor Lamps",
        # "Other Lighting",
        # "Outdoor Lighting",
        # "Lighting",
        # "Computer Speakers",
        # "Laptops",
        # "Printers & Scanners",
        # "Desktops",
        # "Computer Accessories",
        # "Monitors",
        # "Modems & Routers",
        # "Other Computers & Software",
        # "Computers & Software",
        # "iPods & MP3 Players",
        # "Radios & Receivers",
        # "Speakers",
        # "Stereo Systems",
        # "Headphones & Earphones",
        # "Other Audio",
        #                                                                                                                                                                                            Top
        # "Washing Machines & Dryers",
        # "Cooktops & Rangehoods",
        # "Ovens",
        # "Dishwashers",
        # "Vacuum Cleaners",
        # "Air Conditioning & Heating",
        # "Sewing Machines",
        # "Fridges & Freezers",
        # "Small Appliances",
        # "Other Appliances",
        # "TVs",
        # "Home Theatre Systems",
        # "TV Accessories",
        # "Other TV & DVD Players",
        # "DVD Players",
        # "TV & DVD players",
        # "Table & Desk Lamps",
        # "Ceiling Lights",
        # "Floor Lamps",
        # "Other Lighting",
        # "Outdoor Lighting",
        # "Lighting",
        # "Computer Speakers",
        # "Laptops",
        # "Printers & Scanners",
        # "Desktops",
        # "Computer Accessories",
        # "Monitors",
        # "Modems & Routers",
        # "Other Computers & Software",
        # "Computers & Software",
        # "iPods & MP3 Players",
        # "Radios & Receivers",
        "Speakers"
        # "Stereo Systems",
        # "Headphones & Earphones",
        # "Other Audio",
        # "Other Books, Music & Games",
        # "Audio"
    ]

    s3 = boto3.client('s3')
    for category in categories:
        for i in collection.find({'category': category}).limit(10):
            path = i['category'][0]
            print path
            if not os.path.isdir(path):
                os.mkdir(path)
            for image in i['images']:
                s3.download_file('3giks-property','gumtree-au/'+image['path'], os.path.join(path, image['path'][5:]))