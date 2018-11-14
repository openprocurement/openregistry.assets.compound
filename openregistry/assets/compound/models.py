# -*- coding: utf-8 -*-
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType, ValidationError
from zope.interface import implementer

from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset, Item
)


class ICompoundAsset(IAsset):
    """ Marker interface for compound assets """


@implementer(ICompoundAsset)
class Asset(BaseAsset):
    _internal_type = 'compound'
    assetType = StringType(default="compound")
    items = ListType(ModelType(Item))

    def validate_relatedLot(self, data, lot):
        if data['status'] == 'active' and not lot:
            raise ValidationError(u'This field is required.')
