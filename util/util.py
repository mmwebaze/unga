from flask import url_for
import datetime as dt


def generateCleanOutput(item, endpoint):
    items = {}
    for field in item:
        if field == 'id':
            items['uri'] = url_for(endpoint, advert_id=item['id'], _external=True)
        else:
            items[field] = item[field]

    return items

def timeToStr(timeStamp):

    return dt.datetime.fromtimestamp(
        int(timeStamp)
        ).strftime('%Y-%m-%d %H:%M:%S')