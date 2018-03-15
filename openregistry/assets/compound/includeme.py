# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from openprocurement.api.interfaces import IContentConfigurator
from openregistry.assets.compound.models import Asset, ICompoundAsset
from openregistry.assets.compound.adapters import CompoundAssetConfigurator


def includeme(config):
    config.add_assetType(Asset)
    config.scan("openregistry.assets.compound.views")
    config.scan("openregistry.assets.compound.subscribers")
    config.registry.registerAdapter(CompoundAssetConfigurator,
                                    (ICompoundAsset, IRequest),
                                    IContentConfigurator)
