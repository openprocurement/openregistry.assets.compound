# -*- coding: utf-8 -*-
from copy import deepcopy

def create_compound_with_item_schemas(self, test_asset_compound_data):
    response = self.app.post_json('/', {'data': test_asset_compound_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    response = response.json['data']
    self.assertEqual(response['items'][0]['schema_properties']['properties'], test_asset_compound_data['items'][0]['schema_properties']['properties'])
    self.assertEqual(response['items'][0]['schema_properties']['code'][0:2], test_asset_compound_data['items'][0]['schema_properties']['code'][:2])
    self.assertEqual(response['items'][0]['description'], test_asset_compound_data['items'][0]['description'])
    self.assertEqual(response['items'][0]['classification'], test_asset_compound_data['items'][0]['classification'])
    self.assertEqual(response['items'][0]['additionalClassifications'], test_asset_compound_data['items'][0]['additionalClassifications'])
    self.assertEqual(response['items'][0]['address'], test_asset_compound_data['items'][0]['address'])
    self.assertEqual(response['items'][0]['id'], test_asset_compound_data['items'][0]['id'])
    self.assertEqual(response['items'][0]['unit'], test_asset_compound_data['items'][0]['unit'])
    self.assertEqual(response['items'][0]['quantity'], test_asset_compound_data['items'][0]['quantity'])

def bad_item_schemas_code(self, test_asset_compound_data):
    bad_initial_data = deepcopy(test_asset_compound_data)
    bad_initial_data['items'][0]['classification']['id'] = "42124210-6"
    response = self.app.post_json('/', {'data': bad_initial_data},status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'],
                     [{
                         "location": "body",
                         "name": "items",
                         "description": [
                             {u"schema_properties": [u"classification id mismatch with schema_properties code"]},
                             {u"schema_properties": [u"classification id mismatch with schema_properties code"]},
                         ]
                     }])

def delete_item_schema(self, test_asset_compound_data):
    response = self.app.post_json('/', {'data': test_asset_compound_data})
    self.assertEqual(response.status, '201 Created')
    resource = response.json['data']
    self.resource_token = response.json['access']['token']
    self.access_header = {'X-Access-Token': str(response.json['access']['token'])}
    self.resource_id = resource['id']
    self.set_status(self.initial_status)

    response = self.app.patch_json('/{}?access_token={}'.format(
                            self.resource_id, self.resource_token),
                            headers=self.access_header,
                            params={'data': {"items": [{'schema_properties': None}, {'schema_properties': None}]}})
    # TODO add schema props delete
    # self.assertEqual(response.json['data']['items'][0]['schema_properties'], None)