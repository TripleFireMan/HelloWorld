# mixins.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

import json
from logging import getLogger
logger = getLogger('HelloWorld')
class SportRecordResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        # 统一处理所有 ViewSet 的响应
        if isinstance(response, Response):
            # 成功响应
            if 200 <= response.status_code < 300:
                response_data = {
                    "code": 200,  # 自定义成功状态码
                    "message": "请求成功",
                    "data": response.data,
                }
            # 错误响应（如序列化验证失败）
            else:
                # return super().finalize_response(request, response, *args, **kwargs)
                response_data = {
                    "code": 201,  # 自定义错误码
                    "message": self._get_error_message(response.data),
                    "data": None
                }
            response.data = response_data
            response.status_code = 200  # 强制 HTTP 状态码为 200（可选）
        return super().finalize_response(request, response, *args, **kwargs)

    def _get_error_message(self, data):
        # 提取 DRF 默认错误信息（如序列化错误）
        # if isinstance(data, dict):
        #     for key in data.keys():
        #         value = data[key]
        #         if isinstance(value,list):
        #             value.insert(0,ErrorDetail(f'{key}:'))
        #     return next(iter(data.values())) if data else "Unknown error"
        return str(data)
