# -*- coding: utf-8 -*-
import logging

from pyramid.interfaces import IRequest
from openregistry.assets.core.includeme import IContentConfigurator
from openregistry.assets.core.interfaces import IAssetManager
from openregistry.assets.compound.models import Asset, ICompoundAsset
from openregistry.assets.compound.adapters import CompoundAssetConfigurator, CompoundAssetManagerAdapter
from openregistry.assets.compound.constants import DEFAULT_ASSET_COMPOUND_TYPE

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_config=None):
    config.scan("openregistry.assets.compound.views")
    config.scan("openregistry.assets.compound.subscribers")
    config.registry.registerAdapter(CompoundAssetConfigurator,
                                    (ICompoundAsset, IRequest),
                                    IContentConfigurator)
    config.registry.registerAdapter(CompoundAssetManagerAdapter,
                                    (ICompoundAsset, ),
                                    IAssetManager)

    asset_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        asset_types.append(DEFAULT_ASSET_COMPOUND_TYPE)
    for at in asset_types:
        config.add_assetType(Asset, at)

    LOGGER.info("Included openregistry.assets.compound plugin", extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    config.registry.accreditation['asset'][Asset._internal_type] = plugin_config['accreditation']
