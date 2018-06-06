from flask import url_for

class Util:
    def generateCleanOutput(self, item, endpoint):

        items = {}
        for field in item:
            if field == 'id':
                items['uri'] = url_for(endpoint, advert_id=item['id'], _external=True)
            else:
                items[field] = item[field]

        return items