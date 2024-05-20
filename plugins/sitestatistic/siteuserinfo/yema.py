# -*- coding: utf-8 -*-
import json
from typing import Optional, Tuple

from app.plugins.sitestatistic.siteuserinfo import ISiteUserInfo, SITE_BASE_ORDER, SiteSchema
from app.utils.string import StringUtils


class TYemaSiteUserInfo(ISiteUserInfo):
    schema = SiteSchema.Yema
    order = SITE_BASE_ORDER + 60

    @classmethod
    def match(cls, html_text: str) -> bool:
        return '<title>YemaPT</title>' in html_text

    def _parse_site_page(self, html_text: str):
        """
        获取站点页面地址
        """
        self._user_traffic_page = None
        self._user_detail_page = None
        self._user_basic_page = "api/consumer/fetchSelfDetail"
        self._user_basic_params = {}
        self._sys_mail_unread_page = None
        self._user_mail_unread_page = None
        self._mail_unread_params = {}
        self._torrent_seeding_page = None
        self._torrent_seeding_headers = {}
        self._addition_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
        }

    def _parse_logged_in(self, html_text):
        """
        判断是否登录成功, 通过判断是否存在用户信息
        暂时跳过检测，待后续优化
        :param html_text:
        :return:
        """
        return True

    def _parse_user_base_info(self, html_text: str):
        """
        解析用户基本信息，这里把_parse_user_traffic_info和_parse_user_detail_info合并到这里
        """
        if not html_text:
            return None
        detail = json.loads(html_text)
        if not detail or not detail.get("success"):
            return
        user_info = detail.get("data", {})
        self.userid = user_info.get("id")
        self.username = user_info.get("name")
        self.user_level = user_info.get("level")
        self.join_at = StringUtils.unify_datetime_str(user_info.get("registerTime"))

        self.upload = user_info.get('uploadSize')
        self.download = user_info.get('downloadSize')
        self.ratio = round(self.upload / (self.download or 1), 2)
        self.bonus = user_info.get("bonus")
        self.message_unread = 0

    def _parse_user_traffic_info(self, html_text: str):
        """
        解析用户流量信息
        """
        pass

    def _parse_user_detail_info(self, html_text: str):
        """
        解析用户详细信息
        """
        pass

    def _parse_user_torrent_seeding_info(self, html_text: str, multi_page: bool = False) -> Optional[str]:
        """
        解析用户做种信息
        """
        pass

    def _parse_message_unread_links(self, html_text: str, msg_links: list) -> Optional[str]:
        """
        解析未读消息链接，这里直接读出详情
        """
        pass

    def _parse_message_content(self, html_text) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        解析消息内容
        """
        pass
