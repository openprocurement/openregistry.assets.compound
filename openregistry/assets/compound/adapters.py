# -*- coding: utf-8 -*-
from openregistry.assets.core.adapters import AssetConfigurator
from .constants import STATUS_CHANGES


class CompoundAssetConfigurator(AssetConfigurator):
    """ BelowThreshold Tender configuration adapter """

    name = "Compound Asset configurator"
    available_statuses = STATUS_CHANGES
