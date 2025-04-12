from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse,JsonResponse
from rest_framework_jwt.settings import api_settings
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
class JwtAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):

        white_list = ['/SportRecord/login','/SportRecord/jwt_test','/SportRecord/search'] # 请求白名单
        path = request.path

        if path.startswith('/media') or path.startswith('/static'):
            print('不需要token验证')
            return None
        
        
        if path not in white_list and path.startswith('/SportRecord'):
            token = request.META.get('HTTP_AUTHORIZATION')
            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                return JsonResponse({'code':300,'message':'Token 过期，请重新登录'})
            except InvalidTokenError:
                return JsonResponse({'code':301,'message':'Token验证失败'})
            except PyJWTError:
                return JsonResponse({'code':302,'message':'Token验证异常'})
            print('要进行token验证')
        else:
            print('不需要token验证')
            return None