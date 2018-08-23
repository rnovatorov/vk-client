from vk_client import api, models


class VkClient(object):

    def __init__(self, access_token=None, captcha_handler=None):
        self.api = api.create_api(access_token, captcha_handler)

        self.BotsLongPoll = models.BotsLongPollManager(vk=self)
        self.Comment = models.CommentManager(vk=self)
        self.Group = models.GroupManager(vk=self)
        self.GroupEvent = models.GroupEventManager(vk=self)
        self.Message = models.MessageManager(vk=self)
        self.Photo = models.PhotoManager(vk=self)
        self.Post = models.PostManager(vk=self)
        self.User = models.UserManager(vk=self)
