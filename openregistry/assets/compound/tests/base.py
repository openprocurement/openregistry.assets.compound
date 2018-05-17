# -*- coding: utf-8 -*-
import os
from copy import deepcopy

from openregistry.assets.core.tests.base import (
    BaseAssetWebTest as BaseAWT,
    test_asset_compound_data,
    test_asset_compound_data_341,
    test_asset_compound_data_060
)


class BaseAssetWebTest(BaseAWT):
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)

    def setUp(self):
        self.initial_data = deepcopy(test_asset_compound_data)
        asset_type = os.environ.get('ASSET_TYPE', 'compound')
        self.initial_data['assetType'] = asset_type
        super(BaseAssetWebTest, self).setUp()


class AssetContentWebTest(BaseAssetWebTest):
    init = True
    initial_status = 'pending'
