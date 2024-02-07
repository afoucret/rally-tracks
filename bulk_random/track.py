import random
import string

from esrally.track.params import ParamSource


class RandomBulkParamSource(ParamSource):
    def __init__(self, track, params, **kwargs):
        super().__init__(track, params, **kwargs)
        self._bulk_size = params.get("bulk-size", 500)
        self._index_name = params.get("index", track.indices[0].name)

        # * ``body``: containing all documents for the current bulk request.
        # * ``bulk-size``: An indication of the bulk size denoted in ``unit``.
        # * ``unit``: The name of the unit in which the bulk size is provided.
        # * ``action_metadata_present``: if ``True``, assume that an action and metadata line is present (meaning only half of the lines
        # contain actual documents to index)
        # * ``index``: The name of the affected index in case ``action_metadata_present`` is ``False``.
        # * ``type``: The name of the affected type in case ``action_metadata_present`` is ``False``.

    def params(self):
        bulk_data = []
        for _ in range(self._bulk_size):
            bulk_data.append({"index": {"_index": self._index_name}})
            bulk_data.append({"content": "".join(random.choices(string.ascii_lowercase, k=5))})

        return {
            "body": bulk_data,
            "bulk-size": self._bulk_size,
            "action-metadata-present": True,
            "unit": "docs",
            "index": self._index_name,
            "type": "",
        }


def register(registry):
    registry.register_param_source("random-bulk-param-source", RandomBulkParamSource)
