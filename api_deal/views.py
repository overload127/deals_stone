
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class TestView(APIView):
    def get(self, request):
        context = dict()
        context['test'] = 'My test text!'
        return Response(context, status=status.HTTP_200_OK)


# class load_file_for_processing