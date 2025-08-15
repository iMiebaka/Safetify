from django.utils import timezone
from django.db.models import Q, QuerySet
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _



class UserQueryset(QuerySet):
    def verified(self):
        return self.filter(~Q(verified_at=None))
 
    def unverified(self):
        return self.filter(verified_at=None)

    def active(self):
        return self.filter(is_active=True)


class UserManager(BaseUserManager):
    def get_queryset(self) -> QuerySet:
        return UserQueryset(self.model, using=self._db)

    def verified(self) -> QuerySet:
        return self.get_queryset().verified()

    def unverified(self) -> QuerySet:
        return self.get_queryset().unverified()

    def active(self) -> QuerySet:
        return self.get_queryset().active()

    def users(self) -> QuerySet:
        """This filter returns users with account type and profile of passengers or driver"""
        return self.get_queryset().users()

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.update({"is_superuser": True, "is_staff": True})
        extra_fields.update({"verified_at": timezone.now()})

        user = self.create_user(email, password, **extra_fields)
        user.save(using=self._db)
        return user