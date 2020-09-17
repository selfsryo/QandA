from django.utils.safestring import mark_safe
from markdownx.utils import markdownify
from django import template
from django.conf import settings
from markdown.extensions import Extension
import markdown

register = template.Library()



@register.filter
def markdown_to_html(text):
	return mark_safe(markdownify(text))


class EscapeHtml(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


@register.filter
def markdown_to_html_with_escape(text):
    """マークダウンをhtmlに変換する。
    生のHTMLやCSS、JavaScript等のコードをエスケープした上で、マークダウンをHTMLに変換します。
    公開しているコメント欄等には、こちらを使ってください。
    """
    extensions = settings.MARKDOWNX_MARKDOWN_EXTENSIONS + [EscapeHtml()]
    html = markdown.markdown(text, extensions=extensions)
    return mark_safe(html)

