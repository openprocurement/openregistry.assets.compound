# -*- coding: utf-8 -*-
import unittest

from openregistry.api.tests.base import snitch
from openregistry.api.tests.blanks.mixins import ResourceTestMixin

from openregistry.assets.core.tests.blanks.asset import patch_decimal_item_quantity
from openregistry.assets.core.tests.blanks.mixins import AssetResourceTestMixin

from openregistry.assets.compound.models import Asset as AssetCompound
from openregistry.assets.compound.tests.base import (
    test_asset_compound_data, BaseAssetWebTest
)


class AssetCompoundResourceTest(BaseAssetWebTest, ResourceTestMixin, AssetResourceTestMixin):
    asset_model = AssetCompound
    initial_data = test_asset_compound_data
    initial_status = 'pending'

    test_19_patch_decimal_witt_items = snitch(patch_decimal_item_quantity)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetCompoundResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
