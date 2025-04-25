from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from core.models import User
from rest_framework.views import APIView
from rest_framework import serializers

# ------------------------------
# 1. Custom Exception Classes
# ------------------------------
class CustomAPIException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'
    default_code = 'server_error'

class BadRequestException(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request.'
    default_code = 'bad_request'

class NotFoundException(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
    default_code = 'not_found'

class UnauthorizedException(CustomAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized access.'
    default_code = 'unauthorized'

class PermissionDeniedException(CustomAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Permission denied.'
    default_code = 'permission_denied'

# ------------------------------
# 2. Custom Exception Handler
# ------------------------------
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomAPIException):
        return Response(
            {
                'error': {
                    'message': str(exc.detail),
                    'code': exc.default_code
                }
            },
            status=exc.status_code
        )

    return response

# ------------------------------
# 3. Views Using the Custom Exceptions
# ------------------------------
class UserView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['user_id'])
        except User.DoesNotExist:
            raise NotFoundException("User not found.")
        return Response({"user": user.username}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if 'username' not in request.data or 'password' not in request.data:
            raise BadRequestException("Username and password are required.")
        
        user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
        return Response({"message": "User created successfully", "user": user.username}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['user_id'])
        except User.DoesNotExist:
            raise NotFoundException("User not found.")

        if not user.is_active:
            raise UnauthorizedException("Cannot delete inactive users.")
        
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# ------------------------------
# 4. Example Serializer with Custom Exception
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise BadRequestException("Username already exists.")
        return value
