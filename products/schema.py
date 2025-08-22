import graphene
from graphene_django import DjangoObjectType, DjangoListField,DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from .models import Products,Category
from decimal import Decimal


# usando relay, para la implementacion de filtros:

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        fields = ("id", "name")
        interfaces = (graphene.relay.Node,)

class ProductType(DjangoObjectType):
    class Meta:
        model = Products
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'],
            'price': ['exact', 'gte', 'lte'],
            'category__name': ['exact', 'icontains']
        }
        interfaces = (graphene.relay.Node,)
        fields = ('id','title','description','price','category','image')

class Query(graphene.ObjectType):
    all_products = DjangoFilterConnectionField(ProductType)  # 🔹 aquí
    product = graphene.relay.Node.Field(ProductType) 

    all_categories = DjangoFilterConnectionField(CategoryType)
    category = graphene.relay.Node.Field(CategoryType)

# Mutacion, Crud Products

class CreateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        price = graphene.Float(required=True)
        description = graphene.String()
        category = graphene.ID(required=True)

    # definimos un campo para pasar el ProductType
    product = graphene.Field(ProductType)

    def mutate(self,info,title,price,category,description=None):
        category_obj = Category.objects.get(pk=category)
        product = Products.objects.create(title=title,price=Decimal(str(price)), description=description,category=category_obj)
        CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        price = graphene.Float()
        description = graphene.String()
        category = graphene.ID()

    product = graphene.Field(ProductType)

    def mutate(self,info,id,title=None,price=None, description=None,category=None):
        product = Products.objects.get(pk=id)
        if title is not None:
            product.title = title
        if price is not None:
            product.price = Decimal(str(price))  # <-- conversión a Decimal
        if description is not None:
            product.description = description
        if category is not None:
            category_obj = Category.objects.get(pk=category)
            product.category = category_obj
        product.save()
        return UpdateProduct(product=product)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    ok = graphene.Boolean()
    def mutate(self,info,id):
        try:
            product = Products.objects.get(pk=id)
            product.delete()
            return DeleteProduct(ok=True)
        except Products.DoesNotExist:
            return DeleteProduct(ok=False)
        
 


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
