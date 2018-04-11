# -*- coding: utf-8 -*-
from openregistry.assets.core.adapters import AssetConfigurator
from openregistry.assets.core.constants import STATUS_CHANGES

from openregistry.assets.compound.utils import (
    change_asset,
    create_asset,
    get_document,
    add_document,
    patch_document,
    put_document,
    get_all_documents
)

class CompoundAssetConfigurator(AssetConfigurator):
    """ BelowThreshold Tender configuration adapter """

    name = "Compound Asset configurator"
    available_statuses = STATUS_CHANGES


class AssetCompoundManagerAdapter(object):
    name = "Asset Manager for compound asset"
    context = None

    def __init__(self, context):
        self.context = context

    def change_asset(self, request, logger):
        return change_asset(request, self.context, logger)

    def create_asset(self, request, logger, db, server_id):
        return create_asset(request, self.context, logger, db, server_id)


class AssetCompoundDocumentManager(object):

    def __init__(self, context):
        self.asset = context


    def get_asset_documents(self, request):
        return get_all_documents(request, self.asset)

    def get_asset_document(self, request):
        return get_document(request)

    def add_asset_document(self, request, logger):
        return add_document(request, self.asset, logger)

    def patch_asset_document(self, request, logger):
        return patch_document(request, logger)

    def put_asset_document(self, request, logger):
        return put_document(request, logger)
