# -*- coding: utf-8 -*-
from zope.interface import (
    Attribute, Interface
)


class IAssetManager(Interface):
    name = Attribute('Asset name')

    def change_asset(request, context, logger):
        raise NotImplementedError

    def create_asset(request, context, logger, db, server_id):
        raise NotImplementedError


class IAssetDocumentManager(Interface):
    name = Attribute('Asset name')

    def get_all_documents(request, context):
        raise NotImplementedError

    def get_document(request):
        raise NotImplementedError

    def add_document(request, logger):
        raise NotImplementedError

    def put_document(request, logger):
        raise NotImplementedError

    def patch_document(request, logger):
        raise NotImplementedError
