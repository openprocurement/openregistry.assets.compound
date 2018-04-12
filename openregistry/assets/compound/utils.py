# -*- coding: utf-8 -*-
from openregistry.assets.core.utils import (
    save_asset, apply_patch,
)
from openregistry.assets.core.events import AssetInitializeEvent

from openprocurement.api.utils import (
    get_now,
    generate_id,
    set_ownership,
)

from openregistry.assets.core.utils import (
    generate_asset_id
)


def change_asset(request, context):
    asset = context
    if asset.status == 'active' and request.validated['data'].get('status') == 'pending':
        request.validated['data']['relatedLot'] = None
        request.validated['asset'].relatedLot = None
    return asset


def create_asset(request, context, db, server_id):
    asset_id = generate_id()
    context.id = asset_id
    if not context.get('assetID'):
        context.assetID = generate_asset_id(get_now(), db, server_id)
    context.request.registry.notify(AssetInitializeEvent(context))
    if request.json_body['data'].get('status') == 'draft':
        context.status = 'draft'
    acc = set_ownership(context, request)
    request.validated['asset'] = context
    request.validated['asset_src'] = {}
    return context, acc


def add_document(request, context):
    document = request.validated['document']
    document.author = request.authenticated_role
    context.documents.append(document)
    return document


def get_all_documents(request, context):
    if request.params.get('all', ''):
        collection_data = [i.serialize("view") for i in context.documents]
    else:
        collection_data = sorted(dict([
            (i.id, i.serialize("view"))
            for i in context.documents
        ]).values(), key=lambda i: i['dateModified'])
    return collection_data


def get_document(request):
    document = request.validated['document']
    document_data = document.serialize("view")
    document_data['previousVersions'] = [
        i.serialize("view")
        for i in request.validated['documents']
        if i.url != document.url
    ]
    return document_data


def patch_document(request):
    pass

def put_document(request):
    document = request.validated['document']
    request.validated['asset'].documents.append(document)
    return document
