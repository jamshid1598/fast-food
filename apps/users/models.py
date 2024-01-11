import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from users.manager import UserManager


class UserType(models.TextChoices):  
    RIVER = 'driver', _('Driver')
    CLIENT = 'client', _('Client')


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    phone = PhoneNumberField(_("phone"), max_length=100, unique=True, help_text=_('phone number must be required'))
    user_type = models.CharField(_("user type"), max_length=20, choices=UserType.choices, default=UserType.CLIENT)
    two_step_password = models.BooleanField(_("two step password"), default=False, help_text=_("is active two step password?"))

    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)

    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    class Meta:
        ordering = ('created_at', 'updated_at')
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return "/user/%i/" % (self.pk)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey('users.Users', blank=True, null=True, editable=False,
                                    on_delete=models.SET_NULL, related_name='created_%(model_name)ss')
    updated_by = models.ForeignKey('users.Users', blank=True, null=True, editable=False,
                                    on_delete=models.SET_NULL, related_name='updated_%(model_name)ss')

    @property
    def class_name(self):
        return self.__class__.__name__

    class Meta:
        abstract = True
        ordering = ['id']


class SMSToken(BaseModel):
    token = models.CharField(_('token'), max_length=1200)
    is_valid = models.BooleanField(_('is valid'), default=True)

    class Meta:
        db_table = 'user_smstoken'
        verbose_name = _('sms token')
        verbose_name_plural = _('sms tokens')

    def __str__(self):
        return "%s - %s" % (self.created_at, self.updated_at)


class OTPStatus(BaseModel):
    message_id = models.CharField(_('message id'), max_length=255, blank=True, null=True)
    status = models.CharField(_('status'), max_length=255, blank=True, null=True)
    status_date = models.DateTimeField(_('status date'), blank=True, null=True)
    message = models.CharField(_('message'), max_length=255, blank=True, null=True)

    user_sms_id = models.CharField(_('message id'), max_length=255, blank=True, null=True)
    country = models.CharField(_('message id'), max_length=255, blank=True, null=True)
    phone = PhoneNumberField(_('Phone Number'), blank=True, null=True)
    sms_count = models.PositiveSmallIntegerField(_('message id'), default=0)

    class Meta:
        db_table = 'user_otp_status'
        verbose_name = _('otp status')
        verbose_name_plural = _('otp status')

    def __str__(self):
        return "%s - %s" % (self.status, self.phone)
