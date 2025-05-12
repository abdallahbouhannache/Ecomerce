# Python
import json
# Django
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Django REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status


class GetCommunes(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get_commune_by_wilaya(wilaya_id):
        with open(settings.COMMUNES, 'r') as communes_:
            _communes_ = json.load(communes_)
            communes = _communes_.get(wilaya_id, [])
            if communes:
                filtred_communes = map(lambda x:{'id':x['id'], 'name':x['name'], 'ar_name':x['ar_name']}, communes)
                return filtred_communes
            return communes

    def get(self, request, wilaya_id):
        # Data
        resp = {
            "status_code":"200",
            "data": self.get_commune_by_wilaya(wilaya_id)
        }
        return Response(resp, status=status.HTTP_200_OK)