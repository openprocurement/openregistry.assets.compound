# -*- coding: utf-8 -*-
from openregistry.assets.core.utils import (
    save_asset, apply_patch,
)
from openregistry.assets.core.events import AssetInitializeEvent

from openprocurement.api.utils import (
    get_now,
    generate_id,
    json_view,
    set_ownership,
    context_unpack,
    get_file,
    update_file_content_type
)

from openregistry.assets.core.utils import (
    save_asset,
    asset_serialize,
    generate_asset_id
)


def change_asset(request, context, logger):
    asset = context
    if asset.status == 'active' and request.validated['data'].get('status') == 'pending':
        request.validated['data']['relatedLot'] = None
        request.validated['asset'].relatedLot = None
    apply_patch(request, src=request.validated['asset_src'])
    logger.info(
        'Updated asset {}'.format(asset.id),
        extra=context_unpack(request, {'MESSAGE_ID': 'asset_patch'})
    )
    return {'data': asset.serialize(asset.status)}


def create_asset(request, context, logger, db, server_id):
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
    if save_asset(request):
        logger.info('Created asset {} ({})'.format(asset_id, context.assetID),
                         extra=context_unpack(logger.request, {'MESSAGE_ID': 'asset_create'},
                                              {'asset_id': asset_id, 'assetID': context.assetID}))
        request.response.status = 201
        request.response.headers[
            'Location'] = request.route_url('{}:Asset'.format(context.assetType), asset_id=asset_id)
        return {
            'data': context.serialize(context.status),
            'access': acc
        }


def add_document(request, context, logger):
    document = request.validated['document']
    document.author = request.authenticated_role
    context.documents.append(document)
    if save_asset(request):
        logger.info('Created asset document {}'.format(document.id),
                         extra=context_unpack(request, {'MESSAGE_ID': 'asset_document_create'},
                                              {'document_id': document.id}))
        request.response.status = 201
        document_route = request.matched_route.name.replace("collection_", "")
        request.response.headers['Location'] = request.current_route_url(_route_name=document_route,
                                                                                   document_id=document.id, _query={})
        return {'data': document.serialize("view")}


def get_all_documents(request, context):
    if request.params.get('all', ''):
        collection_data = [i.serialize("view") for i in context.documents]
    else:
        collection_data = sorted(dict([
            (i.id, i.serialize("view"))
            for i in context.documents
        ]).values(), key=lambda i: i['dateModified'])
    return {'data': collection_data}


def get_document(request):
    if request.params.get('download'):
        return get_file(request)
    document = request.validated['document']
    document_data = document.serialize("view")
    document_data['previousVersions'] = [
        i.serialize("view")
        for i in request.validated['documents']
        if i.url != document.url
    ]
    return {'data': document_data}


def patch_document(request, logger):
    if apply_patch(request, src=request.context.serialize()):
        update_file_content_type(request)
        logger.info('Updated asset document {}'.format(request.context.id),
                         extra=context_unpack(request, {'MESSAGE_ID': 'asset_document_patch'}))
        return {'data': request.context.serialize("view")}


def put_document(request, logger):
    document = request.validated['document']
    request.validated['asset'].documents.append(document)
    if save_asset(request):
        logger.info('Updated asset document {}'.format(request.context.id),
                         extra=context_unpack(request, {'MESSAGE_ID': 'asset_document_put'}))
        return {'data': document.serialize("view")}

