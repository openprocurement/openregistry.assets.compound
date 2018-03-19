# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openregistry.assets.core.events import AssetInitializeEvent
from openprocurement.api.utils import get_now


@subscriber(AssetInitializeEvent, assetType="compound")
def tender_init_handler(event):
    """ initialization handler for compound assets """
    event.asset.date = get_now()
