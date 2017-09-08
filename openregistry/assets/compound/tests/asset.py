# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import BaseWebTest, snitch
from openregistry.api.tests.blanks.mixins import ResourceTestMixin

from openregistry.assets.core.tests.blanks.mixins import AssetResourceTestMixin

from openregistry.assets.compound.tests.base import (
    test_asset_compound_data, BaseAssetWebTest
)
from openregistry.assets.compound.tests.asset_blanks import (
    # AssetTest
    simple_add_asset
)


class AssetCompoundTest(BaseWebTest):
    initial_data = test_asset_compound_data
    relative_to = os.path.dirname(__file__)

    test_simple_add_asset = snitch(simple_add_asset)


class AssetCompoundResourceTest(BaseAssetWebTest, ResourceTestMixin, AssetResourceTestMixin):
    initial_status = 'pending'


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetCompoundResourceTest))
    tests.addTest(unittest.makeSuite(AssetCompoundTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
