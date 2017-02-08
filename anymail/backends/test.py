from anymail.exceptions import AnymailAPIError
from anymail.message import AnymailRecipientStatus

from .base import AnymailBaseBackend, BasePayload
from ..utils import get_anymail_setting


class EmailBackend(AnymailBaseBackend):
    """
    Anymail backend that doesn't do anything.

    Used for testing Anymail common backend functionality.
    """

    esp_name = "Test"

    def __init__(self, *args, **kwargs):
        # Init options from Django settings
        esp_name = self.esp_name
        self.sample_setting = get_anymail_setting('sample_setting', esp_name=esp_name,
                                                  kwargs=kwargs, allow_bare=True)
        self.recorded_send_params = get_anymail_setting('recorded_send_params', default=[],
                                                        esp_name=esp_name, kwargs=kwargs)
        super(EmailBackend, self).__init__(*args, **kwargs)

    def build_message_payload(self, message, defaults):
        return TestPayload(backend=self, message=message, defaults=defaults)

    def post_to_esp(self, payload, message):
        # Keep track of the send params (for test-case access)
        self.recorded_send_params.append(payload.params)
        try:
            # Tests can supply their own message.test_response:
            response = message.test_response
            if isinstance(response, AnymailAPIError):
                raise response
        except AttributeError:
            # Default is to return 'sent' for each recipient
            status = AnymailRecipientStatus(message_id=1, status='sent')
            response = {
                'recipient_status': {email: status for email in payload.recipient_emails}
            }
        return response

    def parse_recipient_status(self, response, payload, message):
        try:
            return response['recipient_status']
        except KeyError:
            raise AnymailAPIError('Unparsable test response')


# Pre-v0.8 naming (immediately deprecated for this undocumented test feature)
class TestBackend(object):
    def __init__(self, **kwargs):
        raise NotImplementedError(
            "Anymail's (undocumented) TestBackend has been renamed to "
            "'anymail.backends.test.EmailBackend'")


class TestPayload(BasePayload):
    # For test purposes, just keep a dict of the params we've received.
    # (This approach is also useful for native API backends -- think of
    # payload.params as collecting kwargs for esp_native_api.send().)

    def init_payload(self):
        self.params = {}
        self.recipient_emails = []

    def set_from_email(self, email):
        self.params['from'] = email

    def set_to(self, emails):
        self.params['to'] = emails
        self.recipient_emails += [email.email for email in emails]

    def set_cc(self, emails):
        self.params['cc'] = emails
        self.recipient_emails += [email.email for email in emails]

    def set_bcc(self, emails):
        self.params['bcc'] = emails
        self.recipient_emails += [email.email for email in emails]

    def set_subject(self, subject):
        self.params['subject'] = subject

    def set_reply_to(self, emails):
        self.params['reply_to'] = emails

    def set_extra_headers(self, headers):
        self.params['extra_headers'] = headers

    def set_text_body(self, body):
        self.params['text_body'] = body

    def set_html_body(self, body):
        self.params['html_body'] = body

    def add_alternative(self, content, mimetype):
        self.unsupported_feature("alternative part with type '%s'" % mimetype)

    def add_attachment(self, attachment):
        self.params.setdefault('attachments', []).append(attachment)

    def set_metadata(self, metadata):
        self.params['metadata'] = metadata

    def set_send_at(self, send_at):
        self.params['send_at'] = send_at

    def set_tags(self, tags):
        self.params['tags'] = tags

    def set_track_clicks(self, track_clicks):
        self.params['track_clicks'] = track_clicks

    def set_track_opens(self, track_opens):
        self.params['track_opens'] = track_opens

    def set_template_id(self, template_id):
        self.params['template_id'] = template_id

    def set_merge_data(self, merge_data):
        self.params['merge_data'] = merge_data

    def set_merge_global_data(self, merge_global_data):
        self.params['merge_global_data'] = merge_global_data

    def set_esp_extra(self, extra):
        # Merge extra into params
        self.params.update(extra)
