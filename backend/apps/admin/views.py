from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import FAQModel, PrivacyPolicyModel, TermsAndConditionsModel, SupportMessageModel
from .serializers import FAQSerializer, PrivacyPolicySerializer, TermsAndConditionsSerializer, SupportMessageSerializer

class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser

# Base view for singletons (FAQ, Privacy, Terms)
class BaseSingletonView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSuperUserOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_object(self):
        return self.model.objects.first()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"detail": "Content not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if self.model.objects.exists():
            return Response(
                {"detail": "Content already exists. Use PATCH to update."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FAQView(BaseSingletonView):
    model = FAQModel
    serializer_class = FAQSerializer

class PrivacyPolicyView(BaseSingletonView):
    model = PrivacyPolicyModel
    serializer_class = PrivacyPolicySerializer

class TermsAndConditionsView(BaseSingletonView):
    model = TermsAndConditionsModel
    serializer_class = TermsAndConditionsSerializer

# Support Message View (User POSTs)
class SupportMessageCreateView(generics.CreateAPIView):
    queryset = SupportMessageModel.objects.all()
    serializer_class = SupportMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

# Support Message List View (Admin GETs)
class SupportMessageListView(generics.ListAPIView):
    queryset = SupportMessageModel.objects.all().order_by('-created_at')
    serializer_class = SupportMessageSerializer
    permission_classes = [permissions.IsAdminUser]