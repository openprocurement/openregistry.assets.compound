# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetDocumentResource
from openregistry.assets.core.utils import opassetsresource
from openprocurement.api.utils import (
    json_view,
    get_now,
    generate_id,
    json_view,
    set_ownership,
    context_unpack,
    get_file,
    update_file_content_type
)
from openregistry.assets.core.utils import (
    save_asset,
    asset_serialize,
    generate_asset_id,
    apply_patch,

)
from openregistry.assets.compound.interfaces import (
    IAssetManager
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
        data = self.request.registry.getAdapter(
            self.context,
            IAssetManager
        ).get_asset_documents(self.request)
        return {'data': data}

    @json_view(content_type="application/json", permission='upload_asset_documents')
    def collection_post(self):
        """Asset Document Upload"""
        document = self.request.registry.getAdapter(
            self.context,
            IAssetManager
        ).add_asset_document(self.request)
        if save_asset(self.request):
            self.LOGGER.info('Created asset document {}'.format(document.id),
                             extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_document_create'},
                                                  {'document_id': document.id}))
            self.request.response.status = 201
            document_route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(_route_name=document_route,
                                                                                       document_id=document.id, _query={})
            return {'data': document.serialize("view")}


    @json_view(permission='view_asset')
    def get(self):
        """Asset Document Read"""
        if self.request.params.get('download'):
            return get_file(self.request)
        data = self.request.registry.getAdapter(
            self.request.validated['asset'],
            IAssetManager
        ).get_asset_document(self.request)
        return {'data': data}

    @json_view(content_type="application/json", permission='upload_asset_documents')
    def put(self):
        """Asset Document Update"""
        document = self.request.registry.getAdapter(
            self.request.validated['asset'],
            IAssetManager
        ).put_asset_document(self.request)
        if save_asset(self.request):
            self.LOGGER.info('Updated asset document {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_document_put'}))
            return {'data': document.serialize("view")}

    @json_view(content_type="application/json", permission='upload_asset_documents')
    def patch(self):
        """Asset Document Update"""
        self.request.registry.getAdapter(
            self.request.validated['asset'],
            IAssetManager
        ).patch_asset_document(self.request)

        if apply_patch(self.request, src=self.request.context.serialize()):
            self.LOGGER.info('Updated asset document {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_document_patch'}))
            return {'data': self.request.context.serialize("view")}
