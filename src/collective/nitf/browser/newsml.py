# -*- coding: utf-8 -*-
from collective.nitf.browser import View


class NewsML(View):

    """Shows News Article in NewsML format."""

    def version(self):
        """Returns news article revision number."""
        # TODO: get revision number
        return 1

    def nitf_size(self):
        """Returns size of the News Article."""
        # TODO: calculate size
        return 1000

    ITEM_REF = """
<itemRef href="%s/@@nitf" size="%s"
   contenttype="application/nitf+xml" format="fmt:nitf">
    <title>%s</title>
</itemRef>"""

    def get_related_items(self):
        """Returns an itemRef tag for each related item (only News Articles).
        """
        items = getattr(self.context, 'relatedItems', None)
        if items is not None:
            related_items = []
            for i in items:
                href = i.to_object.absolute_url()
                size = self.nitf_size()
                title = i.to_object.Title()
                item_ref = self.ITEM_REF % (href, size, title)
                related_items.append(item_ref)
            return related_items
