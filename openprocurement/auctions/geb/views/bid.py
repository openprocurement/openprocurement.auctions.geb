# -*- coding: utf-8 -*-
from openprocurement.auctions.core.utils import (
    opresource,
    json_view
)
from openprocurement.auctions.core.views.mixins import AuctionBidResource
from openprocurement.auctions.geb.validation import (
    validate_patch_bid_data
)
from openprocurement.auctions.core.interfaces import (
    IManager
)


@opresource(name='geb:Auction Bids',
            collection_path='/auctions/{auction_id}/bids',
            path='/auctions/{auction_id}/bids/{bid_id}',
            auctionsprocurementMethodType="geb",
            description="Auction bids")
class AuctionBidResource(AuctionBidResource):

    @json_view(content_type="application/json", permission='edit_bid', validators=(validate_patch_bid_data,))
    def patch(self):

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IManager)

        manager.change()

        if manager.save():
            msg = 'Updated auction bid {}'.format(manager.context.id)
            manager.log('auction_bid_patch', msg)
            representation_manager = manager.get_representation_manager()
            return representation_manager.represent()

    @json_view(permission='view_auction')
    def get(self):
        """
        Auction Bid Get
        """
        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IManager)
        representation_manager = manager.get_representation_manager()
        return representation_manager.represent()

    @json_view(permission='edit_bid')
    def delete(self):

        manager = self.request.registry.queryMultiAdapter((self.request, self.context), IManager)

        manager.delete()

        if manager.save():
            msg = 'Delete auction bid {}'.format(manager.context.id)
            manager.log('auction_bid_delete', msg)
            representation_manager = manager.get_representation_manager()
            return representation_manager.represent()
