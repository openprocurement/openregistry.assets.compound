# -*- coding: utf-8 -*-
import unittest

from uuid import uuid4

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

    def test_09_asset_concierge_patch(self):
        asset = self.create_resource()

        response = self.app.get('/{}'.format(asset['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], asset)

        # Move status from Draft to Pending
        response = self.app.patch_json('/{}'.format(asset['id']),
                                       headers=self.access_header,
                                       params={'data': {'status': 'pending'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'pending')

        self.app.authorization = ('Basic', ('concierge', ''))

        # Move status from pending to verification
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'verification'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'verification')

        # Move status from verification to Pending
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'pending'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'pending')

        # Move status from pending to verification
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'verification'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'verification')

        # Move status from verification to Active without relatedLot
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'active'}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['description'][0], 'This field is required.')

        # Move status from verification to Active
        relatedLot = uuid4().hex
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'active', 'relatedLot': relatedLot}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'active')
        self.assertEqual(response.json['data']['relatedLot'], relatedLot)

        # Move status from Active to Draft
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'draft'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

        # Move status from Active to Deleted
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'deleted'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (active) status")

        # Move status from Active to Pending
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'pending'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'pending')
        self.assertNotIn('relatedLot', response.json['data'])

        # Move status from Pending to Deleted
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'deleted'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

        # Move status from Pending to Draft
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'draft'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

        # Move status from Pending to Complete
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'complete'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

        # Move status from pending to verification
        response = self.app.patch_json('/{}'.format(asset['id']),
                                       headers=self.access_header,
                                       params={'data': {'status': 'verification'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'verification')

        # Move status from verification to active
        relatedLot = uuid4().hex
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'active', 'relatedLot': relatedLot}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'active')
        self.assertEqual(response.json['data']['relatedLot'], relatedLot)

        # Move status from Active to Complete
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'complete'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['status'], 'complete')

        # Move status from Complete to Draft
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'deleted'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

        # Move status from Complete to Pending
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'deleted'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

        # Move status from Complete to Active
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'deleted'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

        # Move status from Complete to Deleted
        response = self.app.patch_json('/{}'.format(
            asset['id']), {'data': {'status': 'deleted'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['name'], u'data')
        self.assertEqual(response.json['errors'][0]['location'], u'body')
        self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetCompoundResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
