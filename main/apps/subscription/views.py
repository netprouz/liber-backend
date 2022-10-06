from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from main.apps.category.models import CategoryType

from .models import Subscription
from .serializers import SubscriptionCreateSerializer  # noqa
from .serializers import SubscriptionListSerializer, SubscribeSerializer

from rest_framework_simplejwt import authentication
from rest_framework import permissions


import requests
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SubscribeSerializer,CardCreateSerializer,CodeSerializer
from .models import SubscriptionTransaction
from .config import *
from .methods import *


class SubscriptionCreateAPIView(generics.CreateAPIView):
    model = Subscription
    serializer_class = SubscriptionCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return self.model.objects.create_subscription_instance(
            self.request.user,
            serializer.validated_data,
        )


subscription_create_api_view = SubscriptionCreateAPIView.as_view()


class SubscriptionListAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListSerializer
    filterset_fields = ["category", "active"]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


subscription_list_api_view = SubscriptionListAPIView.as_view()


# TODO: remove this function after cronjob has been installed
class SubscriptionAPIView(APIView):
    def get(self, request):
        from .utils import disable_active_subscriptions

        disable_active_subscriptions()
        return Response(200)


subscription_view = SubscriptionAPIView.as_view()



class CardCreateApiView(generics.GenericAPIView):
    serializer_class = CardCreateSerializer
    queryset = SubscriptionTransaction
    def post(self, request,pk):
        serializer = self.get_serializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_create(serializer.validated_data,pk)

        return Response(result)

    def card_create(self, validated_data, pk):
        data = {
            "id": pk,
            "method": "cards.create",
            "params": {
                "card": { "number": validated_data['card_number'], "expire": validated_data['expire']},
                "save": True
            }
        }
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CREATE)
        result = response.json()
        if 'error' in result:
            return result

        token = result['result']['card']['token']
        subscription = Subscription()
        subscription.token_save(token,pk)
        result = self.card_get_verify_code(token)

        return result
    
    def card_get_verify_code(self, token):
        data = dict(
            method=CARD_GET_VERIFY_CODE,
            params=dict(
                token=token
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CREATE)
        result = response.json()
        if 'error' in result:
            return result

        result.update(token=token)
        return result


class CardVerifyApiView(generics.GenericAPIView):
    serializer_class = CodeSerializer
    queryset = SubscriptionTransaction

    def post(self, request,pk):
        serializer = self.get_serializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_verify(serializer.validated_data,pk)

        return Response(result)

    def card_verify(self, validated_data, pk):
        data = {
            "id": pk,
            "method": "cards.verify",
            "params": {
                "token": Subscription.objects.get(id=pk).token_for_register,
                "code": validated_data['code'],
            }
        }
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CREATE)
        result = response.json()
        if 'error' in result:
            return result
        token = Subscription.objects.get(id=pk).token_for_register
        result = self.receipts_create(pk,token)


        subscription = Subscription.objects.filter(id=pk)
        print('subscription', subscription)
        for subs in subscription:
            if subs.status == False:
                subs.status = True
                subs.save()
                print('status',subs.status)
        result = {
            'status':True,
            'message': "Muvaffaqiyatlik to'lov amalga oshirildi!"
        }
        return result


    def receipts_create(self, pk,token):

        data =  {
            "id": pk,
            "method": "receipts.create",
            "params": {
                "amount": Subscription.objects.get(id=pk).price * 100,
                "account": {
                    "order_id": "order_id"
                }

            }}
        response = requests.post(URL, json=data, headers=AUTHORIZATION_RECEIPT)
        result = response.json()
        if 'error' in result:
            return result

        trans_id = result['result']['receipt']['_id']
        trans = SubscriptionTransaction()
        trans.create_transaction(
            trans_id=trans_id,
            request_id=result['id'],
            amount=result['result']['receipt']['amount'],
            account=result['result']['receipt']['account'],
            status=trans.PROCESS,
        )
        result = self.receipts_pay(trans_id,token)
        return result

    def receipts_pay(self, trans_id, token):
        data = dict(
            method=RECEIPTS_PAY,
            params=dict(
                id=trans_id,
                token=token,
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_RECEIPT)
        result = response.json()
        trans = SubscriptionTransaction()

        if 'error' in result:
            trans.update_transaction(
                trans_id=trans_id,
                status=trans.FAILED,
            )
            return result

        trans.update_transaction(
            trans_id=result['result']['receipt']['_id'],
            status=trans.PAID,
        )

        return result
