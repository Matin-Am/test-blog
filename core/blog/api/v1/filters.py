import django_filters
from ...models import Post,Category
from accounts.models import User


class PostFilter(django_filters.FilterSet):
    # published_date = django_filters.DateFromToRangeFilter(field_name="published_date",lookup_expr="range")
    # category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    # author = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta: 
        model = Post
        fields = {
            "published_date":["lte","gte"],
            "category":["exact"],
            "author":["exact"]
        }