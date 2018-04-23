# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetResource
from openregistry.assets.core.utils import opassetsresource

from openprocurement.api.utils import (
    json_view
)

from openregistry.assets.compound.interfaces import IAssetManager
from openregistry.assets.core.utils import (
    save_asset, apply_patch,
)
from openprocurement.api.utils import (
    get_now,
    generate_id,
    json_view,
    set_ownership,
    context_unpack,
    get_file,
    update_file_content_type
)

@opassetsresource(name='compound:Asset',
                  path='/assets/{asset_id}',
                  assetType='compound',
                  description="Open Contracting compatible data exchange format.")
class AssetCompoundResource(AssetResource):

    @json_view(content_type="application/json", permission='create_asset')
    def post(self):
        """This API request is targeted to creating new Asset."""
        asset, acc = self.request.registry.getAdapter(
            self.context,
            IAssetManager
        ).create_asset(self.request, self.db, self.server_id)
        if save_asset(self.request):
            self.LOGGER.info('Created asset {} ({})'.format(asset.id, asset.assetID),
                             extra=context_unpack(self.LOGGER.request, {'MESSAGE_ID': 'asset_create'},
                                                  {'asset_id': asset.id, 'assetID': asset.assetID}))
            self.request.response.status = 201
            self.request.response.headers[
                'Location'] = self.request.route_url('{}:Asset'.format(asset.assetType), asset_id=asset.id)
            return {
                'data': asset.serialize(asset.status),
                'access': acc
            }

    @json_view(content_type="application/json", permission='edit_asset')
    def patch(self):
        asset = self.request.registry.getAdapter(
            self.context,
            IAssetManager
        ).change_asset(self.request)
        apply_patch(self.request, src=self.request.validated['asset_src'])
        self.LOGGER.info(
            'Updated asset {}'.format(asset.id),
            extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_patch'})
        )
        return {'data': asset.serialize(asset.status)}
