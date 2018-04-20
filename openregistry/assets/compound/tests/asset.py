# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.assets.core.tests.blanks.asset import patch_decimal_item_quantity
from openregistry.assets.core.tests.blanks.mixins import (
    AssetResourceTestMixin,
    ResourceTestMixin,
    snitch
)

from openregistry.assets.compound.models import Asset as AssetCompound
from openregistry.assets.compound.tests.base import (
    BaseAssetWebTest,
    test_asset_compound_data,
    test_asset_compound_data_060,
    test_asset_compound_data_341
)
from openregistry.assets.compound.tests.blanks.schema import (
    create_compound_with_item_schemas,
    bad_item_schemas_code,
    delete_item_schema
)


test_data = [test_asset_compound_data, test_asset_compound_data_060]

class AssetCompoundResourceTest(BaseAssetWebTest, ResourceTestMixin, AssetResourceTestMixin):
    asset_model = AssetCompound
    initial_data = test_asset_compound_data
    initial_status = 'pending'
    test_19_patch_decimal_witt_items = snitch(patch_decimal_item_quantity)

    def test_create_compound_with_item_schemas(self):
        for i in test_data:
            create_compound_with_item_schemas(self, i)

    def test_bad_item_schemas_code(self):
        for i in test_data:
            bad_item_schemas_code(self, i)

    def test_delete_item_schema(self):
        for i in test_data:
            delete_item_schema(self, i)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetCompoundResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
