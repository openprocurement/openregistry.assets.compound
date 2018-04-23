# -*- coding: utf-8 -*-
from openregistry.assets.core.adapters import AssetConfigurator
from openregistry.assets.core.constants import STATUS_CHANGES

from openprocurement.api.utils import error_handler

from openregistry.assets.compound.utils import (
    change_asset,
    create_asset,
    get_document,
    add_document,
    patch_document,
    put_document,
    get_all_documents
)

from openregistry.assets.core.validation import (
    validate_patch_asset_data,
    validate_data_by_model,
    validate_asset_data,
    validate_document_operation_in_not_allowed_asset_status,
    validate_asset_document_update_not_by_author_or_asset_owner,

)
from openprocurement.api.validation import (
    validate_change_status,
    validate_file_upload,
    validate_document_data,
    validate_patch_document_data,

)

patch_asset_validators = (
    validate_patch_asset_data,
    validate_change_status,
    validate_data_by_model
)
add_document_validators = (
    validate_file_upload,
    validate_document_operation_in_not_allowed_asset_status
)
put_documet_validators = (
    validate_document_data,
    validate_document_operation_in_not_allowed_asset_status,
    validate_asset_document_update_not_by_author_or_asset_owner
)
patch_document_validators = (
    validate_patch_document_data,
    validate_document_operation_in_not_allowed_asset_status,
    validate_asset_document_update_not_by_author_or_asset_owner
)


class CompoundAssetConfigurator(AssetConfigurator):
    """ BelowThreshold Tender configuration adapter """

    name = "Compound Asset configurator"
    available_statuses = STATUS_CHANGES


class AssetCompoundManagerAdapter(object):
    name = "Asset Manager for compound asset"
    context = None
    create_validation = (validate_asset_data, )
    change_validation = patch_asset_validators

    document_add_validation = add_document_validators
    document_patch_validation = patch_document_validators
    document_put_validation = put_documet_validators

    def __init__(self, context):
        self.context = context

    def _validate(self, request, validators):
        kwargs = {'request': request, 'error_handler': error_handler}
        for validator in validators:
            validator(**kwargs)

    def change_asset(self, request):
        self._validate(request, self.change_validation)
        return change_asset(request, self.context)

    def create_asset(self, request, db, server_id):
        self._validate(request, self.create_validation)
        return create_asset(request, self.context, db, server_id)

    def get_asset_documents(self, request):
        return get_all_documents(request, self.context)

    def get_asset_document(self, request):
        return get_document(request)

    def add_asset_document(self, request):
        self._validate(request, self.document_add_validation)
        return add_document(request, self.context)

    def patch_asset_document(self, request):
        self._validate(request, self.document_patch_validation)
        return patch_document(request)

    def put_asset_document(self, request):
        self._validate(request, self.document_put_validation)
        return put_document(request)
