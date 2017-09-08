# -*- coding: utf-8 -*-
from schematics.types import StringType
from zope.interface import implementer

from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset,
)


class ICompoundAsset(IAsset):
    """ Marker interface for compound assets """


@implementer(ICompoundAsset)
class Asset(BaseAsset):
    assetType = StringType(default="compound")
