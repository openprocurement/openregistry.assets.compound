# -*- coding: utf-8 -*-
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from zope.interface import implementer

from openprocurement.api.registry_models.ocds import Item

from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset,
)


class ICompoundAsset(IAsset):
    """ Marker interface for compound assets """


@implementer(ICompoundAsset)
class Asset(BaseAsset):
    assetType = StringType(default="compound")
    items = ListType(ModelType(Item))
