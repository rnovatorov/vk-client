import attr
import requests
from six.moves.urllib import parse
from vk_client.enums import GroupEventType
from vk_client.models.base import Model, ModelManager


ACT = "a_check"


@attr.s
class BotsLongPoll(Model):

    server = attr.ib()
    key = attr.ib()
    ts = attr.ib()
    wait = attr.ib(default=25)

    def get_updates(self):
        url = self._make_url()
        response = requests.get(url)
        payload = response.json()
        self.ts = payload["ts"]
        return [
            self._vk.GroupEvent(
                type=GroupEventType(update["type"]),
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


@attr.s
class BotsLongPollManager(ModelManager):

    _model = BotsLongPoll

    def get(self, group_id):
        cfg = self._vk.api.groups.getLongPollServer(group_id=group_id)
        return self(
            server=cfg["server"],
            key=cfg["key"],
            ts=cfg["ts"]
        )
