# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetResource
from openregistry.assets.core.utils import opassetsresource

# -*- coding: utf-8 -*-
from openprocurement.api.validation import (
    validate_change_status,
)
from openprocurement.api.utils import (
    json_view
)

from openregistry.assets.core.validation import (
    validate_patch_asset_data,
    validate_data_by_model,
    validate_asset_data
)
from openregistry.assets.compound.interfaces import IAssetManager


patch_asset_validators = (
    validate_patch_asset_data,
    validate_change_status,
    validate_data_by_model
)


@opassetsresource(name='compound:Asset',
                  path='/assets/{asset_id}',
                  assetType='compound',
                  description="Open Contracting compatible data exchange format.")
class AssetCompoundResource(AssetResource):

    @json_view(content_type="application/json", permission='create_asset', validators=(validate_asset_data,))
    def post(self):
        """This API request is targeted to creating new Asset."""
        return self.request.registry.getAdapter(self.context, IAssetManager).create_asset(self.request, self.LOGGER, self.db, self.server_id)


    @json_view(content_type="application/json",
               validators=patch_asset_validators,
               permission='edit_asset')
    def patch(self):
        return self.request.registry.getAdapter(self.context, IAssetManager).change_asset(self.request, self.LOGGER)
