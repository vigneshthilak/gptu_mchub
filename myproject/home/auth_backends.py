from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class UserIDOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to match user by user_id first
            user = User.objects.filter(user_id=username).first()
            if not user:
                # If not found by user_id, try username
                user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None
