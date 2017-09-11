# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetResource
from openregistry.assets.core.utils import opassetsresource


@opassetsresource(name='compound:Asset',
                  path='/assets/{asset_id}',
                  assetType='compound',
                  description="Open Contracting compatible data exchange format.")
class AssetCompoundResource(AssetResource):
    pass
