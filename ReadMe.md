[Philip James - API-Driven Django - PyCon 2018](https://www.youtube.com/watch?v=w0xgJ5C9Be8)

[Slides - API Driven Django - PyCon 2018](https://speakerdeck.com/phildini/api-driven-django)

"""
Views that lists and creates Votes

django.views.generic.list.ListView
django.views.generic.edit.CreateView
Template File
URL Update
(Possibly) a ModelForm
"""

"""
What about an API?

Class based and function based views are mostly written from the perspective of I am going to be rendering a template
    That's not strictly true - but that's most of the thought process that has gone into it.

Two options:
1. Add separate API views (Isn't that great since you are maintaining two sets of logic)
2. Munge JSON responses into existing views - Django has some facilities to support JSON output however not natively 
supported into the generic views that we want to be using to make our life easier to deal with models


Whats better for the client?
What's better for the dev?

    The approach suggested: If you do not have to duplicate the code, but still be able to render template and still 
    have the API first kind of mentality - then you are probably going to be happier in the long run.
    
    Also brings to the point that we are all and Django specifically is moving into - where its getting rarer and 
    rarer that the sites you are building in Django - are going to be using the full Django rendering context as the 
    frontend for your app
        Most of us now use
        Rich Frontends, client-first == API-Driven, API-First
    
STARTING WITH DJANGO REST VIEW
"""

"""
Immediately you will notice that to create the same view as mentioned earlier (through generic views) we need less 
things here comparatively. All we need to get going:

Goal: To create: APIView that lists and creates Votes

We Need:
1. ModelSerializer for Vote
2. rest_framework.generics.ListCreateAPIView

DRF ModelSerializers:
    Serializers - similar to django forms - take data from user - run some logic and save/update the model
        Serializers also however, take representation of the model and turn into json
            they sit between the model and the view to make sure that representations make sense to each part of the 
            stack.

E.g. of ModelSerializer
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'account_name', 'users', 'created')

"""

"""
Looking at two DRF views in this tutorial
1. ListCreateAPIView
    List instances from a model
    Create instances by making a POST request
2. 
"""

**DRF Renderer**
- A renderer is something that exists in Django by also exists in Django Rest Framework
- It's what we are going to use to really empower this idea that we can use the same view for both the API response 
and the rendered template response.
- The kind of default renderer if you are accessing Django Rest Framework API in an API context (e.g. using 
`requests` or using `curl`) is the JSONRenderer.
- To add renderers to a particular view, overwrite its `renderer_classes` variable as follows:
```python
renderer_classes = (
    JSONRenderer,
    TemplateHTMLRenderer,
    BrowsableAPIRenderer,
)
```
- Note: The order of renderer classes matter. For example, in the above scenario, since `TemplateHTMLRenderer` is 
added before `BrowsableAPIRender`, it will by default render in HTML format. If the `BrowsableAPIRenderer` was before
 `TemplateHTMLRenderer`, it would have by default given the DRF standard API view.
 Additionally if the `JSONRenderer` was not added, the `format=json` query param would not work and the `format=api` 
 would give a poorly formatted (too much spacing) data in response. Go check it out! 

**What a renderer does?**
- A renderer takes a representation of data - which is in Python in this case, so for example - the python view 
throws out a Python representation of data requested via the API (e.g. an OrderedDict) and the renderer takes that 
and translates it into JSON.
- So we get a much simpler JSON representation as output instead of Python representation which would have contained 
Python objects such as OrderedDicts, Lists, etc.

**DRF TemplateHTMLRenderer**
- We are going to be using DRF TemplateHTMLRenderer
- It takes that same internal Python representation and translates it into HTML using a template that we provided it

**DRF BrowsableAPIRenderer**
- Similarly there the browsable API renderer which is what we saw earlier when we passed query param `format=api` to 
the request url as follows: `http://localhost:8000/votes/?format=api`

**_Briefly_ just talking about Django templating**
```jinja2
<ul>
    {% for user in results %}
        <li>
            <a href="/users/{{ user.id }}/">{{ user.name }}</a>
        </li>
    {% endfor %}
</ul>
```
- Django templating allows lot of simple constructs like `for` loops and `if` statements
- Syntax of double curly braces for accessing things in the context, e.g. `{{ user.name }}`

**DRF Template Gotcha**
- In `settings.py`
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```
- When we move from that internal python representation to an HTML context, the renderer needs to know how to 
translate this big list of results from QuerySet into something that the frontend can parse. That means it needs to 
figure out how to break it into pages so it only sends a chunk at a time rather than trying to send down tens of 
thousands of millions of results in each query.
- For simplicity sake, we are using `PageNumberPagination` with `PAGE_SIZE: 10`
- Django Rest Framework comes with a whole set of default paginators
- Another popular one is kind of `cursor` and `page pagination`
---- This is like here's a cursor which represents where you are in your page set and like here's the cursor to next 
page set
---- `page and off set` is also very popular paginator


**Authentication**

- Several methods such as OAuth, Token, Session, RemoteAuth
- Cannot cover all these in this tutorial due to time limitations.
- DRF breaks its authentication system into twoparts:
    1. DRF Authentication classes and
        - Authentication classes are - how does a user say, yes I am a user
    2. DRF Permissions classes 
        - Great, now that I have a user, what can a user do on the API
_- You can think of this as Authentication (auth) vs Authorization (permissions)_
- In this tutorial - primary focus: Permissions class (confusing name): `isAuthenticatedOrReadOnly`
- We will add, to both our View Classes `VoteDetail` and `VoteList`,
  `permission_classes` variable that is going to contain
  `permissions.isAuthenticatedOrReadOnly`
  -   This means - if you are an anonymous user, you can read everything
      but if you try to update it you are going to get some sort of 40x
      error.
  - If you are authenticated, it will works as expected.