# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetDocumentResource
from openregistry.assets.core.utils import opassetsresource
from openprocurement.api.utils import (
    json_view,
)
from openprocurement.api.validation import (
    validate_file_upload,
    validate_document_data,
    validate_patch_document_data,
)
from openregistry.assets.core.validation import (
    validate_document_operation_in_not_allowed_asset_status,
    validate_asset_document_update_not_by_author_or_asset_owner,
)
from openregistry.assets.compound.interfaces import (
    IAssetDocumentManager
)


@opassetsresource(name='compound:Asset Documents',
                  collection_path='/assets/{asset_id}/documents',
                  path='/assets/{asset_id}/documents/{document_id}',
                  assetType='compound',
                  description="Asset related binary files (PDFs, etc.)")
class AssetCompoundDocumentResource(AssetDocumentResource):
    @json_view(permission='view_asset')
    def collection_get(self):
        """Asset Documents List"""
        return self.request.registry.getAdapter(self.context, IAssetDocumentManager).get_asset_documents(self.request)

    @json_view(content_type="application/json", permission='upload_asset_documents',
               validators=(
                    validate_file_upload,
                    validate_document_operation_in_not_allowed_asset_status))
    def collection_post(self):
        """Asset Document Upload"""
        return self.request.registry.getAdapter(self.context, IAssetDocumentManager).add_asset_document(self.request, self.LOGGER)

    @json_view(permission='view_asset')
    def get(self):
        """Asset Document Read"""
        return self.request.registry.getAdapter(self.request.validated['asset'], IAssetDocumentManager).get_asset_document(self.request)

    @json_view(content_type="application/json", permission='upload_asset_documents',
               validators=(
                    validate_document_data,
                    validate_document_operation_in_not_allowed_asset_status,
                    validate_asset_document_update_not_by_author_or_asset_owner))
    def put(self):
        """Asset Document Update"""
        return self.request.registry.getAdapter(self.request.validated['asset'], IAssetDocumentManager).put_asset_document(self.request, self.LOGGER)

    @json_view(content_type="application/json", permission='upload_asset_documents',
               validators=(
                    validate_patch_document_data,
                    validate_document_operation_in_not_allowed_asset_status, validate_asset_document_update_not_by_author_or_asset_owner))
    def patch(self):
        """Asset Document Update"""
        return self.request.registry.getAdapter(self.request.validated['asset'], IAssetDocumentManager).patch_asset_document(self.request, self.LOGGER)