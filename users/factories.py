import factory

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        obj = super()._create(model_class, *args, **kwargs)
        if password:
            obj.set_password(password)
        else:
            obj.set_unusable_password()
        obj.save()
        return obj

    class Meta:
        model = User
