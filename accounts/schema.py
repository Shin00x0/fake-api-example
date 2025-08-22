

# Manejo de JWT GRAPHWQL
''' 
Nota esta implementacion esta separada de la implementacion
de token con djoser es un problema si.

por cosas de timpo lo hice asi.
tengo la implementacion completa aqui.

'''
import graphene 
import graphql_jwt

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(mutation=Mutation)
