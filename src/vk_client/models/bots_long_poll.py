import requests
from six.moves.urllib import parse
from vk_client import enums, validators
from vk_client.models import base


ACT = "a_check"


class BotsLongPoll(base.Model):

    def __init__(self, vk, server, key, ts, wait=25):
        assert validators.positive(ts)
        assert validators.positive(wait)

        super(BotsLongPoll, self).__init__(vk)

        self.server = server
        self.key = key
        self.ts = ts
        self.wait = wait

    def get_updates(self):
        url = self._make_url()
        response = requests.get(url)
        payload = response.json()
        self.ts = payload["ts"]
        return [
            self._vk.GroupEvent(
                type=enums.GroupEventType(update["type"]),
                object=update["object"]
            )
            for update in payload["updates"]
        ]

    def _make_url(self):
        query = parse.urlencode({
            "act": ACT,
            "key": self.key,
            "ts": self.ts,
            "wait": self.wait
        })
        return "?".join([self.server, query])


class BotsLongPollManager(base.ModelManager):

    _model = BotsLongPoll

    def get(self, group_id):
        cfg = self._vk.api.groups.getLongPollServer(group_id=group_id)
        return self(
            server=cfg["server"],
            key=cfg["key"],
            ts=cfg["ts"]
        )
