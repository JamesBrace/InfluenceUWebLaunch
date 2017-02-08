import json
from datetime import datetime

from django.utils.timezone import utc

from .base import AnymailBaseWebhookView
from ..signals import tracking, AnymailTrackingEvent, EventType, RejectReason


class SendGridBaseWebhookView(AnymailBaseWebhookView):
    """Base view class for SendGrid webhooks"""

    def parse_events(self, request):
        esp_events = json.loads(request.body.decode('utf-8'))
        return [self.esp_to_anymail_event(esp_event) for esp_event in esp_events]

    def esp_to_anymail_event(self, esp_event):
        raise NotImplementedError()


class SendGridTrackingWebhookView(SendGridBaseWebhookView):
    """Handler for SendGrid delivery and engagement tracking webhooks"""

    signal = tracking

    event_types = {
        # Map SendGrid event: Anymail normalized type
        'bounce': EventType.BOUNCED,
        'deferred': EventType.DEFERRED,
        'delivered': EventType.DELIVERED,
        'dropped': EventType.REJECTED,
        'processed': EventType.QUEUED,
        'click': EventType.CLICKED,
        'open': EventType.OPENED,
        'spamreport': EventType.COMPLAINED,
        'unsubscribe': EventType.UNSUBSCRIBED,
        'group_unsubscribe': EventType.UNSUBSCRIBED,
        'group_resubscribe': EventType.SUBSCRIBED,
    }

    reject_reasons = {
        # Map SendGrid reason/type strings (lowercased) to Anymail normalized reject_reason
        'invalid': RejectReason.INVALID,
        'unsubscribed address': RejectReason.UNSUBSCRIBED,
        'bounce': RejectReason.BOUNCED,
        'blocked': RejectReason.BLOCKED,
        'expired': RejectReason.TIMED_OUT,
    }

    def esp_to_anymail_event(self, esp_event):
        event_type = self.event_types.get(esp_event['event'], EventType.UNKNOWN)
        try:
            timestamp = datetime.fromtimestamp(esp_event['timestamp'], tz=utc)
        except (KeyError, ValueError):
            timestamp = None

        if esp_event['event'] == 'dropped':
            mta_response = None  # dropped at ESP before even getting to MTA
            reason = esp_event.get('type', esp_event.get('reason', ''))  # cause could be in 'type' or 'reason'
            reject_reason = self.reject_reasons.get(reason.lower(), RejectReason.OTHER)
        else:
            # MTA response is in 'response' for delivered; 'reason' for bounce
            mta_response = esp_event.get('response', esp_event.get('reason', None))
            reject_reason = None

        # SendGrid merges metadata ('unique_args') with the event.
        # We can (sort of) split metadata back out by filtering known
        # SendGrid event params, though this can miss metadata keys
        # that duplicate SendGrid params, and can accidentally include
        # non-metadata keys if SendGrid modifies their event records.
        metadata_keys = set(esp_event.keys()) - self.sendgrid_event_keys
        if len(metadata_keys) > 0:
            metadata = {key: esp_event[key] for key in metadata_keys}
        else:
            metadata = None

        return AnymailTrackingEvent(
            event_type=event_type,
            timestamp=timestamp,
            message_id=esp_event.get('smtp-id', None),
            event_id=esp_event.get('sg_event_id', None),
            recipient=esp_event.get('email', None),
            reject_reason=reject_reason,
            mta_response=mta_response,
            tags=esp_event.get('category', None),
            metadata=metadata,
            click_url=esp_event.get('url', None),
            user_agent=esp_event.get('useragent', None),
            esp_event=esp_event,
        )

    # Known keys in SendGrid events (used to recover metadata above)
    sendgrid_event_keys = {
        'asm_group_id',
        'attempt',  # MTA deferred count
        'category',
        'cert_err',
        'email',
        'event',
        'ip',
        'marketing_campaign_id',
        'marketing_campaign_name',
        'newsletter',  # ???
        'nlvx_campaign_id',
        'nlvx_campaign_split_id',
        'nlvx_user_id',
        'pool',
        'post_type',
        'reason',  # MTA bounce/drop reason; SendGrid suppression reason
        'response',  # MTA deferred/delivered message
        'send_at',
        'sg_event_id',
        'sg_message_id',
        'smtp-id',
        'status',  # SMTP status code
        'timestamp',
        'tls',
        'type',  # suppression reject reason ("bounce", "blocked", "expired")
        'url',  # click tracking
        'url_offset',  # click tracking
        'useragent',  # click/open tracking
    }

