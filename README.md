# BLOG PROJECT

```bash
mkdir src
django-admin startproject mysite src

# Different environment servers:
./manage.py runserver 127.0.0.1:8000 --settings=mysite.settings

``` 
# IMPORTANT:
* Use `request.GET.get("query")` to get *query params*.


# Insights:
> Class based views are views implemented as python classes instead of normal functions. Useful to group related functionality as *mixins*.
> **SSL:** While HTTPS originally used SSL, modern HTTPS connections use TLS. The terms SSL and TLS are often used interchangeably, but TLS is the current standard.

Each form field has a default *widget* type that determines how it's rendered in the HTML (e.g., `Charfield --> input type=text`)
Use `<form novalidate>` to avoid the browser default form validation
 
To use custom HTML markup in forms:
```html
{% for field in form %}
<div class="my-div">
{{ field.errors }}
{{ field.label_tag }} {{ field }}
<div class="help-text">{{ field.help_text|safe }}</div>
</div>
{% endfor %}
```

In Django 5.0, the `as_field_group` method allows you to render HTML for the label, field, help text and errors: `form.name.as_field_group` (*no need to call the method!*)

* Filters expression: `{{ variable|my_filter:"foo" }}`, `{{ variable|filter1|filter2 }}`
* Sitemap: in Django admin modify the site name to modify the url that appears in the `sitemap.xml`

* Fixtures: Django tool to load/dump data from database to file.
```bash
./manage.py dumpdata --indent 2 --ouput=db_data.json <blog.Post> <blog.Comment>
./manage.py loaddat db_data.json
```
**IMPORTANT**: *contenttypes* framework contains metadata about your models that is added during migrations, so you may need to exclude it when dumping data:
```
--exclude=contenttypes
```
You may also need to exclude `auth.Permission` since the default CRUD permissions for model are created on migrate



# Good practices:
* URLs in templates: `<a href="{% url 'blog:post_detail' post.id}">`
* Group each app's forms in `forms.py`.

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

* You can create child objects directly from parent object:
```python
new_article = r.article_set.create(...)
new_comment = post.comments.create(...)
```
* Notice that in a *one-to-many* relationship, if you add an existing child object to another parent, it will be removed from the original parent!
```python
r2.article_set.add(new_article2)
```
* `models.ForeignKeyField` are used for a *one-to-many* relationship. Use `model.OneToOneField` for a *one-to-one* relationship


* Check if there are pending migrations to be applied: `showmigrations --plan`

* With Postgres you can use text search:
```python
Post.objects.filter(title__search="something")

### Search multiple fields:
from django.contrib.postgres.search import SearchVector

Post.objects.annotate(search=SearchVector("title", "body")).search("django")
```
> Stemming: reducing words to their base form (*stem*), e.g., `musicality -> music`
`SearchQuery` uses stemming algorithms before creating the search query. If also removes stop words.
`SearchRank`provides a way to sort results based on how often query terms appear and how close together they are.

## Development:

To get right Django HTML formatting in VSCode install `monosans.djLint`
Then install as tool with uv: `uv tool install djlint`
Look for tool directory: `uv tool list --show-paths` and add it to the `settings.json`:
```json
"[django-html]": {
  "editor.defaultFormatter": "monosans.djlint",
  "editor.formatOnSave": true
},
"djlint.useVenv": false,
"djlint.pythonPath": "/home/<USERNAME>/.local/share/uv/tools/djlint/bin/python",
```
