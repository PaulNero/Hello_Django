import graphene
from app_blogs.models import Post, Comment, Category, Tags
from graphene_django import DjangoObjectType

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = '__all__'

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'
        
class TagsType(DjangoObjectType):
    class Meta:
        model = Tags
        fields = '__all__'

class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post_id = graphene.Field(PostType, id=graphene.Int())
    post_title = graphene.Field(PostType, title=graphene.String())
    
    comments = graphene.List(CommentType)
    categories = graphene.List(CategoryType)
    tags = graphene.List(TagsType)

    def resolve_posts(self, info):
        return Post.objects.all()
    
    def resolve_post_id(self, info, id):
        try:
            post_id = Post.objects.get(id=id)
            return post_id
        except Post.DoesNotExist:
            return None
    
    def resolve_post_title(self, info, title):
        try:
            post_title = Post.objects.get(title=title)
            return post_title
        except Post.DoesNotExist:
            return None
    
    def resolve_comments(self, info):
        return Comment.objects.all()
    
    def resolve_categories(self, info):
        return Category.objects.all()
    
    def resolve_tags(self, info):
        return Tags.objects.all()

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        category = graphene.Int(required=True)
        tags = graphene.List(graphene.Int)
        
    post = graphene.Field(PostType)
    
    @classmethod
    def mutate(cls, root, info, title, content, category, tags=None):
        try:
            category_obj = Category.objects.get(id=category)
            post = Post.objects.create(
                title=title, 
                content=content, 
                category=category_obj
            )
            if tags:
                tag_objects = Tags.objects.filter(id__in=tags)
                post.tags.set(tag_objects)
            return CreatePost(post=post)
        except Category.DoesNotExist:
            raise Exception(f"Category with id {category} does not exist")
        except Exception as e:
            raise Exception(f"Error creating post: {e}")

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()

