# -*- coding: utf-8 -*-
from pyramid.interfaces import IRequest
from openregistry.assets.core.includeme import IContentConfigurator
from openregistry.assets.compound.models import Asset, ICompoundAsset
from openregistry.assets.compound.adapters import CompoundAssetConfigurator


def includeme(config, plugin_config=None):
    config.add_assetType(Asset)
    config.scan("openregistry.assets.compound.views")
    config.scan("openregistry.assets.compound.subscribers")
    config.registry.registerAdapter(CompoundAssetConfigurator,
                                    (ICompoundAsset, IRequest),
                                    IContentConfigurator)
