# -*- coding: utf-8 -*-
from schematics.types.compound import ListType, ModelType
from schematics.types import StringType, MD5Type, ValidationError
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
    relatedLot = MD5Type(serialize_when_none=False)

    def validate_relatedLot(self, data, lot):
        if data['status'] == 'active' and not lot:
            raise ValidationError(u'This field is required.')
