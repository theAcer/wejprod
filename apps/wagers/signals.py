from django.dispatch import Signal



wager_request_created = Signal()
wager_request_accepted = Signal()
wager_request_rejected = Signal()
wager_request_canceled = Signal()
wager_request_viewed = Signal()
wager_request_accepted = Signal()
wager_removed = Signal()