import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Profile, Follow
from graphql_jwt.decorators import login_required

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    followers = graphene.List(UserType, user_id=graphene.ID(required=True))
    following = graphene.List(UserType, user_id=graphene.ID(required=True))
    
    # Get all users
    @login_required
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    # Get a single user
    @login_required
    def resolve_user(root, info, id):
        return User.objects.get(pk=id)
    