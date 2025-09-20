import graphene
from graphql_auth.schema import UserQuery as AuthUserQuery, MeQuery
from graphql_auth import mutations
from graphql_jwt.refresh_token.models import RefreshToken
from users.schema import UserQuery, Mutation as UserMutation
from posts.schema import Query as PostsQuery, Mutation as PostsMutation




class LogoutUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        refresh_token = graphene.String(required=True)

    def mutate(self, info, refresh_token, **kwargs):
        try:
            token = RefreshToken.objects.get(token=refresh_token)
            token.revoke()  # blacklist token
            return LogoutUser(ok=True)
        except RefreshToken.DoesNotExist:
            return LogoutUser(ok=False)

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field() # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field() # login
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    
    # Custom logout mutation
    logout_user = LogoutUser.Field()

class Query(AuthUserQuery, UserQuery, MeQuery, PostsQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, UserMutation, PostsMutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)