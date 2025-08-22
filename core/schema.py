
import graphene
import products.schema
import accounts.schema

class Query(products.schema.Query,graphene.ObjectType):
    pass


class Mutation(products.schema.Mutation,accounts.schema.Mutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
