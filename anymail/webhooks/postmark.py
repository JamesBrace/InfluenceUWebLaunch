import json

from django.utils.dateparse import parse_datetime

from .base import AnymailBaseWebhookView
from ..exceptions import AnymailConfigurationError
from ..signals import tracking, AnymailTrackingEvent, EventType, RejectReason
from ..utils import getfirst


class PostmarkBaseWebhookView(AnymailBaseWebhookView):
    """Base view class for Postmark webhooks"""

    def parse_events(self, request):
        esp_event = json.loads(request.body.decode('utf-8'))
        return [self.esp_to_anymail_event(esp_event)]

    def esp_to_anymail_event(self, esp_event):
        raise NotImplementedError()


class PostmarkTrackingWebhookView(PostmarkBaseWebhookView):
    """Handler for Postmark delivery and engagement tracking webhooks"""

    signal = tracking

    event_types = {
        # Map Postmark event type: Anymail normalized (event type, reject reason)
        'HardBounce': (EventType.BOUNCED, RejectReason.BOUNCED),
        'Transient': (EventType.DEFERRED, None),
        'Unsubscribe': (EventType.UNSUBSCRIBED, RejectReason.UNSUBSCRIBED),
        'Subscribe': (EventType.SUBSCRIBED, None),
        'AutoResponder': (EventType.AUTORESPONDED, None),
        'AddressChange': (EventType.AUTORESPONDED, None),
        'DnsError': (EventType.DEFERRED, None),  # "temporary DNS error"
        'SpamNotification': (EventType.COMPLAINED, RejectReason.SPAM),
        'OpenRelayTest': (EventType.DEFERRED, None),  # Receiving MTA is testing Postmark
        'Unknown': (EventType.UNKNOWN, None),
        'SoftBounce': (EventType.DEFERRED, RejectReason.BOUNCED),  # until HardBounce later
        'VirusNotification': (EventType.BOUNCED, RejectReason.OTHER),
        'ChallengeVerification': (EventType.AUTORESPONDED, None),
        'BadEmailAddress': (EventType.REJECTED, RejectReason.INVALID),
        'SpamComplaint': (EventType.COMPLAINED, RejectReason.SPAM),
        'ManuallyDeactivated': (EventType.REJECTED, RejectReason.BLOCKED),
        'Unconfirmed': (EventType.REJECTED, None),
        'Blocked': (EventType.REJECTED, RejectReason.BLOCKED),
        'SMTPApiError': (EventType.FAILED, None),  # could occur if user also using Postmark SMTP directly
        'InboundError': (EventType.INBOUND_FAILED, None),
        'DMARCPolicy': (EventType.REJECTED, RejectReason.BLOCKED),
        'TemplateRenderingFailed': (EventType.FAILED, None),
        # Postmark does not report DELIVERED
        # Postmark does not report CLICKED (because it doesn't implement click-tracking)
        # OPENED doesn't have a Type field; detected separately below
        # INBOUND doesn't have a Type field; should come in through different webhook
    }

    def esp_to_anymail_event(self, esp_event):
        reject_reason = None
        try:
            esp_type = esp_event['Type']
            event_type, reject_reason = self.event_types.get(esp_type, (EventType.UNKNOWN, None))
        except KeyError:
            if 'FirstOpen' in esp_event:
                event_type = EventType.OPENED
            elif 'DeliveredAt' in esp_event:
                event_type = EventType.DELIVERED
            elif 'From' in esp_event:
                # This is an inbound event
                raise AnymailConfigurationError(
                    "You seem to have set Postmark's *inbound* webhook URL "
                    "to Anymail's Postmark *tracking* webhook URL.")
            else:
                event_type = EventType.UNKNOWN

        recipient = getfirst(esp_event, ['Email', 'Recipient'], None)  # Email for bounce; Recipient for open

        try:
            timestr = getfirst(esp_event, ['DeliveredAt', 'BouncedAt', 'ReceivedAt'])
        except KeyError:
            timestamp = None
        else:
            timestamp = parse_datetime(timestr)

        try:
            event_id = str(esp_event['ID'])  # only in bounce events
        except KeyError:
            event_id = None

        try:
            tags = [esp_event['Tag']]
        except KeyError:
            tags = None

        return AnymailTrackingEvent(
            description=esp_event.get('Description', None),
            esp_event=esp_event,
            event_id=event_id,
            event_type=event_type,
            message_id=esp_event.get('MessageID', None),
            mta_response=esp_event.get('Details', None),
            recipient=recipient,
            reject_reason=reject_reason,
            tags=tags,
            timestamp=timestamp,
            user_agent=esp_event.get('UserAgent', None),
        )
