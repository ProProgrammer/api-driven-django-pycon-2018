# Create your views here.
# Django generic views - class based views - common operations combined in a class based view
from django.shortcuts import redirect
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer

from votes.models import Votes
from votes.serializers import VoteSerializer

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


class VotesList(ListCreateAPIView):
    queryset = Votes.objects.all()
    serializer_class = VoteSerializer

    # Order of renderer classes matters
    renderer_classes = (
        JSONRenderer,
        TemplateHTMLRenderer,
        BrowsableAPIRenderer,
    )

    template_name = 'vote_list.html'

    def create(self, request, *args, **kwargs):
        """
        Overriding the create function of ListCreateAPIView to:
        # redirect the user to /votes/ if:
            # the renderer used is of HTML format and the response returned is 201 - i.e. CREATED
                # Its like browser saying: "Hey give me what lives at /votes/ and also, I'd really like HTML back so
                if you can give me HTML back, that'd be great.
                    # DRF captures the info regarding format in which request was made in `accepted_renderer.format`
                    and so if we successfully created the vote, ie. the response status code would be 201
            # Since this indicates that on HTML format renderer, someone created something - i.e. using the form we
            provided in vote_create.html
        """
        response = super(VotesList, self).create(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html' and response.status_code == 201:
            return redirect('/votes/')
        return response


class VoteDetail(RetrieveUpdateDestroyAPIView):
    queryset = Votes.objects.all()
    serializer_class = VoteSerializer

    renderer_classes = (
        JSONRenderer,
        TemplateHTMLRenderer,
        BrowsableAPIRenderer,
    )

    template_name = 'vote.html'
