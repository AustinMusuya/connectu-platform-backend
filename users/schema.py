import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Profile, Follow
from graphql_jwt.decorators import login_required

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = '__all__'

class FollowType(DjangoObjectType):
    class Meta:
        model = Follow
        fields = '__all__'


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
    
    @login_required
    def resolve_followers(self, info, user_id):
        user = User.objects.get(pk=user_id)
        return user.profile.get_followers()
    
    @login_required
    def resolve_following(self, info, user_id):
        user = User.objects.get(pk=user_id)
        return user.profile.get_following()
    
    def get_following(self):
        return User.objects.filter(followers__follower=self.user)
    
    def get_followers(self):
        return User.objects.filter(following__followed=self.user)
    
class FollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    follower = graphene.Field(UserType)
    followed = graphene.Field(UserType)

    @login_required
    def mutate(self, info, user_id):
        follower = info.context.user
        
        try:
            followed = User.objects.get(pk=user_id)    
            if follower == followed:
                return FollowUser(success=False, message="You cannot follow yourself.")
            
            follow, created = Follow.objects.get_or_create(follower=follower, followed=followed)

            if created:
                follow.save()
                return FollowUser(success=True, follower=follower, followed=followed)
            else:
                return FollowUser(success=False, message="You are already following this user.")
        except User.DoesNotExist:
            return FollowUser(success=False, message="The user you are trying to follow does not exist.")
        
        
class UnfollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    follower = graphene.Field(UserType)
    unfollowed = graphene.Field(UserType)

    @login_required
    def mutate(self, info, user_id):
        follower = info.context.user
        
        try:
            unfollowed = User.objects.get(pk=user_id)    
            if follower == unfollowed:
                return UnfollowUser(success=False, message="You cannot unfollow yourself.")
            
            follow = Follow.objects.filter(follower=follower, followed=unfollowed).first()

            if follow:
                follow.delete()
                return UnfollowUser(success=True, follower=follower, unfollowed=unfollowed)
            else:
                return UnfollowUser(success=False, message="You are not following this user.")
        except User.DoesNotExist:
            return UnfollowUser(success=False, message="The user you are trying to unfollow does not exist.")

class UpdateProfile(graphene.Mutation):
    class Arguments:
        bio = graphene.String()
        location = graphene.String()
        birth_date = graphene.types.datetime.Date()
        profile_pic = graphene.String()

    profile = graphene.Field(ProfileType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, bio=None, location=None, birth_date=None, profile_pic=None):
        user = info.context.user
        profile = user.profile # user profile automatically created upon registration (already guaranteed by the signal)

        if bio is not None:
            profile.bio = bio
        if location is not None:
            profile.location = location
        if birth_date is not None:
            profile.birth_date = birth_date
        if profile_pic is not None:
            profile.profile_pic = profile_pic

        profile.save()

        return UpdateProfile(profile=profile, success=True, message="Profile updated successfully.")   
class Mutation(graphene.ObjectType):
    follow_user = FollowUser.Field()
    unfollow_user = UnfollowUser.Field()
    update_profile = UpdateProfile.Field()
    
