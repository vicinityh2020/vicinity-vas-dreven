import falcon
import json
import os
from falcon import HTTPBadRequest, HTTPNotFound, HTTP_200, HTTP_201, HTTP_204


PATH_TO_THING_DESCRIPTION = './objects'
THING_DESCRIPTION_NAME = 'thing_description.json'

class ThingDescriptionResource():
    """
    API Resource to interact with Thing description model. This resource exposes
    an only a GET method called from Agent.All methods translate keystone URI
    to internal URI.
    """

    def on_get(self, req, resp):
        """
        [GET] - /objects
        Endpoint that answers to Vicinity agent and retrieves thing description
        to Active discovery
        :return:
            200 OK - returns thing description
        """

        with open(os.path.join(PATH_TO_THING_DESCRIPTION, THING_DESCRIPTION_NAME)) as json_file:
            data = json.load(json_file)

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(data)