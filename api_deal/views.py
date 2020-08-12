
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser


class TestView(APIView):
    def get(self, request):
        context = dict()
        context['test'] = 'My test text!'
        return Response(context, status=status.HTTP_200_OK)


# class LoadDealsFromFileView(APIView):
class DealLoadCSV(APIView):
    """
    Загрузка сделок из файла
    """
    parser_classes = (MultiPartParser,)

    def post(self, request, format='csv'):
        """ """
        return Response(status=status.HTTP_200_OK)
