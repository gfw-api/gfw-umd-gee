"""Router for classifications"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import jsonify, Blueprint

from gfwanalysis.errors import ClassificationError
from gfwanalysis.middleware import get_classification_params
from gfwanalysis.routes.api import error
from gfwanalysis.serializers import serialize_classifier_output
from gfwanalysis.services.analysis.classification_service import ClassificationService

recent_tiles_classifier_v1 = Blueprint('recent_tiles_classifier_v1', __name__)


def analyze(img_id):
    """
    """
    try:
        data = ClassificationService.classify(img_id=img_id)
    except ClassificationError as e:
        logging.error('[ROUTER]: ' + e.message)
        return error(status=500, detail=e.message)
    return jsonify(data=serialize_classifier_output(data, 'recent_tiles_classifier')), 200


@recent_tiles_classifier_v1.route('/', strict_slashes=False, methods=['GET'])
@get_classification_params
def trigger_analysis(img_id):
    """Classify an image by ID depending on Satellite type"""
    logging.info('[ROUTER]: Getting url for tiles for Sentinel')
    return analyze(img_id=img_id)
