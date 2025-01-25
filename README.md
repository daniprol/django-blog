# BLOG PROJECT

```bash
mkdir src
django-admin startproject mysite src

# Different environment servers:
./manage.py runserver 127.0.0.1:8000 --settings=mysite.settings

``` 
# IMPORTANT:
* Use `request.GET.get("query")` to get *query params*.

# Good practices:
* URLs in templates: `<a href="{% url 'blog:post_detail' post.id}">`

# DJANGO ORM Crash Course
* By default `objects` manager is created. If we create a different manager, then `objects` needs to be explicitly created!

* Get **ONE** object or raise exception (`User.DoesNotExist` and `User.MultipleObjectsReturned`): `User.objects.get(username="admin")`
* Get or create object (returns tuple with boolean!): `user, created = User.objects.get_or_create(username='user2')`
* `Post.objects.all()` is a Queryset that is not executed until necessary! (like evaluating the variable for example)
    * Same applies when creating *Querysets* using filters: `Post.objects.filter(title="first")`
    * **TIP**: use `print(queryset.query)` to get the raw SQL expression
* Field lookups:
    * `title__icontains="django"`
    * `id__in=[1,2]` (you can use another Queryset!)
    * `title__startswith="first"`
    * You can apply multiple filters: `User.objects.filter(...).filter(...)`
    * Exclude from queryset: `User.objects.filter(...).exclude(...)`
* Chained field lookups:
    * `author__username__startswith="admin"`
    * `published__year__gte=2020`
* Use slicing to apply LIMIT and OFFSET: `User.objects.all()[3:5]`, `User.objects.all()[0]
* Check if a result exists: `User.objects.filter(...).exists()`. It returns a boolean.
* Complex lookups apply `Q` with `& | ^ ~`
    * You can use `Q` objects with `filter`, `get`, `exclude`, ... and pass multiple of them
```python
from django.db.models import Q
first_year = Q(published__year=2020)
second_year = Q(published_year=2000)
Posts.objects.filter(first_year | second_year)
```


