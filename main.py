import logging
import base64
import urllib
import HTMLParser
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

class EncodeExtension(Extension):

    def __init__(self):
        logger.info('init Encoding Extension')
        super(EncodeExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        parser = HTMLParser.HTMLParser()

        try:
            base64Text = base64.b64decode(event.get_argument())
        except TypeError:
            base64Text = "Cannot decode input text as base64."

        try:
            urlText = urllib.unquote_plus(event.get_argument())
        except:
            urlText = "Cannot decode input text"

 
        htmlText = parser.unescape(event.get_argument())
        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=base64Text,
                                         description='Base64 Decoded',
                                         highlightable=False,
                                         on_enter=CopyToClipboardAction(base64Text)
                                         ))

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=urlText,
                                         description='URL Decoded',
                                         highlightable=False,
                                         on_enter=CopyToClipboardAction(
                                             urlText)
                                        ))

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=htmlText,
                                           description='HTML Decoded',
                                           highlightable=False,
                                           on_enter=CopyToClipboardAction(
                                               htmlText)
                                           ))

        return RenderResultListAction(items)

if __name__ == '__main__':
    EncodeExtension().run()
