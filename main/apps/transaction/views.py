from rest_framework import status
from rest_framework.response import Response
from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from rest_framework.views import APIView
from . import serializers
from .service import initialize_transaction
from .helper import CheckTransaction
from .models import TRANSACTIONTYPECHOICES


<<<<<<< HEAD

class InitializePaymentAPIView(MerchantAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
=======
class InitializePaymentAPIView(APIView):
>>>>>>> 13b3a7f7f8a7366d87d97d195f2c6d1379d59348
    serializer_class = serializers.InitializePaymentSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        transaction_type = data.validated_data.get('transaction_type')
        price = data.validated_data.get('price')

        transaction_id = initialize_transaction(request.user, price, transaction_type)

        if transaction_type == TRANSACTIONTYPECHOICES.PAYME:
            # TODO: change success return url
            generated_link = Paycom().create_initialization(price, transaction_id, return_url="https://example.com", )
            # generated_link = "https://example.com"
            print(generated_link)
            return Response(status=status.HTTP_200_OK, data={"generated_link": generated_link})

        if transaction_type == TRANSACTIONTYPECHOICES.CLICK:
            pass


initialize_payment_api_view = InitializePaymentAPIView.as_view()


class AcceptPaymeRequestsView(MerchantAPIView):
    VALIDATE_CLASS = CheckTransaction


accept_payme_request_view = AcceptPaymeRequestsView.as_view()