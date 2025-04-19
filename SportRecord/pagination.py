from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class SportRecordNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'pageSize'
    page_query_param = 'pageNum'
    def get_paginated_response(self, data):
        return Response({
                "currentPage":self.page.number,
                "list":data,
                "totle":self.page.paginator.count
        })