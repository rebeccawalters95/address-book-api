from .serializers import AddressSerializer, RegisterSerializer
from .models import Address

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import GenericAPIView


class RegisterAPIView(GenericAPIView):
    """
    This allows new users to register (POST). They can then login and logout using the login/logout buttons
    at the top right of the api page.

    Users are not able to use the same email address twice to register!

    Currently, there is an issue that, while users have to be authenticated to view and add to the database, there is
    only one database with all users addresses. New users can also add addresses associated with other users. This will
    be a problem if this API is to be used by a variety of clients. I think that I will have to change the permissions
    of users to make it so that they only have permission to view and manipulate data associated with their login,
    but I was not sure how exactly to implement this here.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # Adding HTTP status updates to make it easier to see when things have gone wrong
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressViewSet(viewsets.ModelViewSet):
    """
    Using viewsets.ModelViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Only authenticated users can view and manipulate the address book!

    Examples:
        GET /addresses/1/ : should return the address associated with id 1 (i.e. the first address added). The
        user is also able to DELETE the address and PUT (update the address fields)
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    # If user is not authenticated then they cannot add to the address book OR read the content.
    # Users can become authenticated by registering, at http://127.0.0.1:8000/register and then logging in
    # at http://127.0.0.1:8000/api-auth/login/?next=/addresses/
    permission_classes = [permissions.IsAuthenticated]

    # We add a filter option where the users can filter the address data based on the fields
    # the filter option can be accessed either by the button Filters (top right)
    # or by the using the url as follows:
    # EXAMPLE:
    #   to filter by the first id (id 1):
    #   http://127.0.0.1:8000/addresses/?id=1&address_line_1=&address_line_2=&city_or_town=&country=&postcode=&user=

    # I have made the assumption that the user will input the fields EXACTLY as they were created
    # i.e. it is case sensitive, whitespace sensitive etc. If I had more time I would try and make it
    # not case sensitive and would implement a test for this.
    filter_fields = ('id', 'address_line_1', 'address_line_2', 'city_or_town', 'country', 'postcode', 'user')




