# -*- coding: utf-8 -*-
from zope.interface import (
    Attribute, Interface
)


class IAssetManager(Interface):
    name = Attribute('Asset name')

    def change_asset(request, context):
        raise NotImplementedError

    def create_asset(request, context, db, server_id):
        raise NotImplementedError

    def get_all_documents(request, context):
        raise NotImplementedError

    def get_document(request):
        raise NotImplementedError

    def add_document(request):
        raise NotImplementedError

    def put_document(request):
        raise NotImplementedError

    def patch_document(request):
        raise NotImplementedError
