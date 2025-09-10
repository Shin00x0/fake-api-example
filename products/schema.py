import graphene
from graphene_django import DjangoObjectType, DjangoListField,DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from .models import Products,Category
from decimal import Decimal
from graphql_relay import from_global_id

# usando relay, para la implementacion de filtros:

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        fields = ("id", "name")
        interfaces = (graphene.relay.Node,)

class ProductNode(DjangoObjectType):
    class Meta:
        model = Products
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
            'price': ['exact', 'gte', 'lte'],
            'category__name': ['exact', 'icontains']
        }
        fields = ('id','title','description','price','category','image')
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    all_products = DjangoFilterConnectionField(ProductNode)  
    product = graphene.relay.Node.Field(ProductNode)

    all_categories = DjangoFilterConnectionField(CategoryNode)
    category = graphene.relay.Node.Field(CategoryNode)


# Mutacion, Crud Products
class CreateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        price = graphene.Float(required=True)
        description = graphene.String()
        category = graphene.ID(required=True)
    product = graphene.Field(ProductNode)

    def mutate(self,info,title,price,category,description=None):
        _, category_id = from_global_id(category)
        category_obj = Category.objects.get(pk=category_id)
        product = Products.objects.create(title=title,price=Decimal(str(price)), description=description,category=category_obj)
        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        price = graphene.Float()
        description = graphene.String()
        category = graphene.ID()

    product = graphene.Field(ProductNode)

    def mutate(self,info,id,title=None,price=None, description=None,category=None):
        _, db_id = from_global_id(id)

        product = Products.objects.get(pk=db_id )
        if title is not None:
            product.title = title
        if price is not None:
            product.price = Decimal(str(price))  # <-- conversión a Decimal
        if description is not None:
            product.description = description
        if category is not None:
            _, category_id = from_global_id(category)
            category_obj = Category.objects.get(pk=category_id)
            product.category = category_obj
        product.save()
        return UpdateProduct(product=product)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    ok = graphene.Boolean()
    def mutate(self,info,id):
        try:
            _, db_id = from_global_id(id)
            product = Products.objects.get(pk=db_id)
            product.delete()
            return DeleteProduct(ok=True)
        except Products.DoesNotExist:
            return DeleteProduct(ok=False)
        
 


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
