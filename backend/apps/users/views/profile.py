from dj_rest_auth.views import UserDetailsView
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema

class CustomUserDetailsView(UserDetailsView):
    """
    Override UserDetailsView to support MultiPartParser for profile picture uploads.
    """
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Update user profile, including profile picture via multipart/form-data.",
        responses={200: UserDetailsView.serializer_class}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update user profile, including profile picture via multipart/form-data.",
        responses={200: UserDetailsView.serializer_class}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
