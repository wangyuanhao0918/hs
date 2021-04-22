#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Time : 2021/4/20 下午12:21 
# @Author : yuanhao-wang
# @Filename : email.py
from django.core.mail import EmailMessage
import pandas as pd

from django.conf import settings
from utils import Logging


class Email(object):
    @classmethod
    def send_mail(cls, title: str, content: str, user_mail_list: list, attachments: list = None):
        """
        发送邮件
        :param title 邮件标题 str
        :param content 邮件内容 str
        :param user_mail_list 收件人 list
        :param attachments 附件 list
        """
        params = {
            "subject": title,
            "body": content,
            "from_email": settings.EMAIL_HOST_USER,
            "to": user_mail_list
        }
        try:
            msg = EmailMessage(**params)
            if attachments:
                for i in attachments:
                    msg.attach_file(i)
            msg.send()
        except Exception as a:
            Logging.error(
                log_name=title,
                log_info=f'邮箱发送失败-->{a}'

            )
            return

        return

    @classmethod
    def export_table_csv_xlsx(cls, first_line: dict, data_list: list, export_name: str, table_type='csv'):
        """
        导入
        :param first_line: 表头映射
        :param data_all: 数据
        :param export_name: 导出名称
        :param table_type: 文件类型 csv,xlsx
        """

        if not data_list:
            return
        try:
            columns = [first_line.get(k) for k, v in data_list[0].items()]

            result_list = []
            for i in data_list:
                _data_list = []
                for k, v in i.items():
                    _data_list.append(v)
                result_list.append(_data_list)

            dt = pd.DataFrame(result_list, columns=columns)
            if table_type == 'csv':
                dt.to_csv(f"./export_table/{export_name}.csv", index=0)
            else:
                dt.to_excel(f"./export_table/{export_name}.xlsx", index=0)
        except Exception as a:

            Logging.error(
                log_name=export_name,
                log_info=f'导入表格失败-->{a}'
            )
            return

        return

    @classmethod
    def export_table_send_mail(
            cls, first_line: dict, data_list: list, export_name: str,
            title: str, content: str, user_mail_list: list, table_type='csv'):
        """
        导入表格并且发送邮箱
        :param first_line: 字段映射
        :param data_list: 数据
        :param export_name: 表格名称
        :param title: 邮箱标题
        :param content: 邮件内容
        :param user_mail_list: 收件人
        :param table_type: 表格类型 csv or xlsx
        :return:
        """
        if not data_list:
            return

        # 导出数据
        cls.export_table_csv_xlsx(
            first_line=first_line, data_list=data_list,
            export_name=export_name, table_type=table_type
        )

        # 发送邮箱
        cls.send_mail(
            title=title, content=content,
            user_mail_list=user_mail_list,
            attachments=[f"./export_table/{export_name}.{table_type}"]
        )
