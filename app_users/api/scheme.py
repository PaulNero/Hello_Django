import graphene
from app_users.models import Profile
from graphene_django import DjangoObjectType

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields_exclude = ['password']
        
class Query(graphene.ObjectType):
    profiles = graphene.List(ProfileType)
    
    def resolve_profiles(self, info):
        return Profile.objects.all()
    
# class Mutation(graphene.ObjectType):
#     pass