import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Post, Comment, PostLike, CommentLike
from graphql_jwt.decorators import login_required

User = get_user_model()

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = '__all__'

class PostLikeType(DjangoObjectType):
    class Meta:
        model = PostLike
        fields = '__all__'

class CommentLikeType(DjangoObjectType):
    class Meta:
        model = CommentLike
        fields = '__all__'


# class ShareType(DjangoObjectType):  ##### Future implementation ######
#     class Meta:
#         model = Share
#         fields = '__all__'

class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.ID(required=True))
    comments = graphene.List(CommentType, post_id=graphene.ID(required=True))
    comments_count = graphene.Int(post_id=graphene.ID(required=True))
    likes_post = graphene.List(PostLikeType, post_id=graphene.ID(required=True))
    like_count = graphene.Int(post_id=graphene.ID(required=True))
    likes_comment = graphene.List(CommentLikeType, comment_id=graphene.ID(required=True))
    like_count_comment = graphene.Int(comment_id=graphene.ID(required=True))
    # shares = graphene.List(ShareType, post_id=graphene.ID(required=True)) ##### Future implementation ######


    # get all posts
    @login_required
    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

    # get a single post
    @login_required
    def resolve_post(self, info, id):
        return Post.objects.get(pk=id)

    # get comments for a post
    @login_required
    def resolve_comments(self, info, post_id):
        return Comment.objects.filter(post__id=post_id)
    
    # get comment count for a post
    @login_required
    def resolve_comments_count(self, info, post_id):
        return Comment.objects.filter(post__id=post_id).count()

    # get likes for a post
    @login_required
    def resolve_likes_post(self, info, post_id):
        return PostLike.objects.filter(post__id=post_id)
    
    # get like count for a post
    @login_required
    def resolve_like_count(self, info, post_id):
        return PostLike.objects.filter(post__id=post_id).count()
    
    # get likes for a comment
    @login_required
    def resolve_likes_comment(self, info, comment_id):
        return CommentLike.objects.filter(comment__id=comment_id)
    
    # get like count for a comment
    @login_required
    def resolve_like_count_comment(self, info, comment_id):
        return CommentLike.objects.filter(comment__id=comment_id).count()


    # @login_required
    # def resolve_shares(self, info, post_id): ##### Future implementation ######
    #     return Share.objects.filter(post__id=post_id)
    
class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        media_url = graphene.String()
    
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, title, content, media_url=None):
        user = info.context.user
        post = Post(title=title, content=content, author=user, media_url=media_url)
        post.save()
        return CreatePost(post=post, success=True, message="Post created successfully.")
    
class DeletePost(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        post_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        try:
            post = Post.objects.get(pk=post_id, author=user)
            post.delete()
            return DeletePost(success=True, message="Post deleted successfully.")
        except Post.DoesNotExist:
            return DeletePost(success=False, message="Post not found or you do not have permission to delete it.")


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, post_id, content):
        user = info.context.user
        post = Post.objects.get(pk=post_id)
        comment = Comment(post=post, author=user, content=content)
        comment.save()
        return CreateComment(comment=comment, success=True, message="Comment added successfully.")
    
class DeleteComment(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        comment_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, comment_id):
        user = info.context.user
        try:
            comment = Comment.objects.get(pk=comment_id, author=user)
            comment.delete()
            return DeleteComment(success=True, message="Comment deleted successfully.")
        except Comment.DoesNotExist:
            return DeleteComment(success=False, message="Comment not found or you do not have permission to delete it.")
        
class CreateCommentComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        parent_comment_id = graphene.ID(required=True)
        content = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, parent_comment_id, content):
        user = info.context.user
        parent_comment = Comment.objects.get(pk=parent_comment_id)
        comment = Comment(post=parent_comment.post, author=user, content=content)
        comment.save()
        return CreateCommentComment(comment=comment, success=True, message="Comment added successfully.")
    
class DeleteCommentComment(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        comment_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, comment_id):
        user = info.context.user
        try:
            comment = Comment.objects.get(pk=comment_id, author=user)
            comment.delete()
            return DeleteCommentComment(success=True, message="Comment deleted successfully.")
        except Comment.DoesNotExist:
            return DeleteCommentComment(success=False, message="Comment not found or you do not have permission to delete it.")

    
class CreateLikePost(graphene.Mutation):
    like = graphene.Field(PostLikeType)

    class Arguments:
        post_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    
    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        post = Post.objects.get(pk=post_id)
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        if not created:
            return CreateLikePost(success=False, message="You have already liked this post.")
        
        return CreateLikePost(like=like, success=True, message="Post liked successfully.")
    
class UnlikePost(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        post_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, post_id):
        user = info.context.user
        try:
            like = PostLike.objects.get(post__id=post_id, user=user)
            like.delete()
            return UnlikePost(success=True, message="Post unliked successfully.")
        except PostLike.DoesNotExist:
            return UnlikePost(success=False, message="You have not liked this post.")
    
class CreateLikeComment(graphene.Mutation):
    like = graphene.Field(CommentLikeType)

    class Arguments:
        comment_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, comment_id):
        user = info.context.user
        comment = Comment.objects.get(pk=comment_id)
        like, created = CommentLike.objects.get_or_create(comment=comment, user=user)
        if not created:
            return CreateLikeComment(success=False, message="You have already liked this comment.")
        
        return CreateLikeComment(like=like, success=True, message="Comment liked successfully.")
    
class UnlikeComment(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        comment_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, comment_id):
        user = info.context.user
        try:
            like = CommentLike.objects.get(comment__id=comment_id, user=user)
            like.delete()
            return UnlikeComment(success=True, message="Comment unliked successfully.")
        except CommentLike.DoesNotExist:
            return UnlikeComment(success=False, message="You have not liked this comment.")
        
        
    
# class CreateShare(graphene.Mutation): ##### Future implementation ######
#     share = graphene.Field(ShareType)

#     class Arguments:
#         post_id = graphene.ID(required=True)

#     @login_required
#     def mutate(self, info, post_id):
#         user = info.context.user
#         post = Post.objects.get(pk=post_id)
#         share, created = Share.objects.get_or_create(post=post, user=user)
#         if not created:
#             raise Exception("You have already shared this post.")
#         return CreateShare(share=share)
    
class Mutation(graphene.ObjectType):
    # posts
    create_post = CreatePost.Field()
    create_like_post = CreateLikePost.Field()
    unlike_post = UnlikePost.Field()
    delete_post = DeletePost.Field()

    # comments
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()
    create_like_comment = CreateLikeComment.Field()
    unlike_comment = UnlikeComment.Field()   
    create_comment_comment = CreateCommentComment.Field()
    delete_comment_comment = DeleteCommentComment.Field()
    
    
    

    # create_share = CreateShare.Field() ##### Future implementation ######

