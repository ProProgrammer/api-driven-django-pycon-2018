# Create your tests here.
from unittest import TestCase

from django.utils import timezone
from rest_framework.test import APITestCase

from votes.models import Votes
from votes.serializers import VoteSerializer


class TestVotesView(APITestCase):
    number_of_votes = 13
    url = '/votes/'

    @classmethod
    def setUpTestData(cls):
        for vote_id in range(cls.number_of_votes):
            Votes.objects.create(
                subject=f"Vote: {vote_id}",
                ayes=vote_id,
                nays=100 - vote_id)  # Randomly subtracting from 100

    def test_get_view(self):
        """
        Ensure we are able to list the votes
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_content_in_view_response(self):
        response = self.client.get(self.url)
        print(response.data)
        print(type(response.data))
        # print(actual[0])
        # print(len(actual[0]))

        self.assertEqual(len(response.json()), self.number_of_votes)
        self.assertContains(response.json(), list(Votes.objects.all))


class TestVotesModel(TestCase):
    pass


class TestVoteSerializer(TestCase):

    def setUp(self):
        """
        Create a Votes object to use for testing purpose
        :return:
        """
        self.subject = "Is Django the best?"
        self.constant_time = timezone.now()
        self.vote_taken = self.constant_time
        self.ayes = 10
        self.nays = 15
        self.vote = Votes.objects.create(
            subject=self.subject,
            vote_taken=self.vote_taken,
            ayes=self.ayes,
            nays=self.nays
        )
        self.vote_serializer = VoteSerializer(self.vote)

    def test_serializer_fields_in_output(self):
        self.assertEqual(len(self.vote_serializer.fields.fields), 5)
        self.assertIn('id', self.vote_serializer.fields.fields)
        self.assertIn('vote_taken', self.vote_serializer.fields.fields)
        self.assertIn('subject', self.vote_serializer.fields.fields)
        self.assertIn('ayes', self.vote_serializer.fields.fields)
        self.assertIn('nays', self.vote_serializer.fields.fields)

    def test_serializer_field_values(self):
        """
        Assert values for each of the fields in serializer
        Not implemented due to shortage of time - but you get the point
        """
        pass
