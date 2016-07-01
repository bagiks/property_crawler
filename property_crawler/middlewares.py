from random import choice
from scrapy import signals
from scrapy.exceptions import NotConfigured, IgnoreRequest
import logging


class RotateUserAgentMiddleware(object):
    """Rotate user-agent for each request."""
    def __init__(self, user_agents):
        self.enabled = False
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_CHOICES', [])

        if not user_agents:
            raise NotConfigured("USER_AGENT_CHOICES not set or empty")

        o = cls(user_agents)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)

        return o

    def spider_opened(self, spider):
        self.enabled = getattr(spider, 'rotate_user_agent', self.enabled)

    def process_request(self, request, spider):
        if not self.enabled or not self.user_agents:
            return

        request.headers['user-agent'] = choice(self.user_agents)
        # print "--------------------------" * 5
        # print request.headers['user-agent']



class IgnoreDuplicatesMiddleware(object):
    def __init__(self):
        pass

    def process_response(self, request, response, spider):
        logging.warn("In Middleware " + response.url)
        if response.url == "http://www.achurchnearyou.com//":
            raise IgnoreRequest()
        else:
            return response