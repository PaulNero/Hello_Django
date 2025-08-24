import graphene
import app_blogs.api.scheme as blogs_scheme
import app_users.api.scheme as users_scheme

class Query(blogs_scheme.Query, users_scheme.Query, graphene.ObjectType):
    pass

class Mutation(blogs_scheme.Mutation, graphene.ObjectType):
    pass

scheme = graphene.Schema(query=Query, mutation=Mutation)
