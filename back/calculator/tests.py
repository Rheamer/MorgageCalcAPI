from rest_framework.test import \
    APITestCase, \
    force_authenticate,\
    APIRequestFactory
from django.utils.http import urlencode
from calculator import views
from django.urls import reverse
from rest_framework import status
from calculator import models
from calculator import serializers
import json

def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


class TestOfferView(APITestCase):
    factory = APIRequestFactory()
    view_list = views.OfferApiView
    view_detail = views.OfferDetailApiView
    multi_db = True

    def create_offers(self):
        models.Offer.objects.create(
            bank_name='test',
            term_min='1', term_max='2',
            rate_min='120', rate_max='190',
            payment_min='120', payment_max='999',
        )
        models.Offer.objects.create(
            bank_name='test',
            term_min='1', term_max='2',
            rate_min='90', rate_max='190',
            payment_min='120', payment_max='999',
        )
        models.Offer.objects.create(
            bank_name='test',
            term_min='1', term_max='2',
            rate_min='120', rate_max='190',
            payment_min='500', payment_max='999',
        )
        models.Offer.objects.create(
            bank_name='test',
            term_min='1', term_max='2',
            rate_min='120', rate_max='190',
            payment_min='120', payment_max='300',
        )

    def test_list(self):
        self.create_offers()
        request = self.factory.get(
            reverse_querystring('offer-list')
        )
        resp = self.view_list.as_view({'get': 'list'})(request)
        serializer = serializers.OfferSerializer(data=resp.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(serializer.data), 4)

    def test_create(self):
        offer = models.Offer.objects.create(
            bank_name='test',
            term_min='10', term_max='30',
            rate_min='10', rate_max='16.5',
            payment_min='1000000', payment_max='10000000',
        )
        serializer = serializers.OfferSerializer(offer)
        serializer.data['bank_name'] = 'TEST'
        request = self.factory.post(
            reverse_querystring('offer-detail', args=(offer.id,)), data=serializer.data
        )
        resp = self.view_list.as_view({'post': 'create'})(request)
        self.assertEqual(models.Offer.objects.all().count(), 2)

    def test_delete(self):
        offer = models.Offer.objects.create(
            bank_name='test',
            term_min='10', term_max='30',
            rate_min='10', rate_max='16.5',
            payment_min='1000000', payment_max='10000000',
        )
        request = self.factory.delete(
            reverse_querystring('offerid-detail', args=(offer.id,))
        )
        resp = self.view_detail.as_view({'delete': 'destroy'})(request, id=offer.id)
        self.assertEqual(models.Offer.objects.all().count(), 0)

    def test_update(self):
        offer = models.Offer.objects.create(
            bank_name='test',
            term_min='10', term_max='30',
            rate_min='10', rate_max='16.5',
            payment_min='1000000', payment_max='10000000',
        )
        serializer = serializers.OfferSerializer(offer)
        offer.rate_min = 20
        offer.bank_name = 'TEST'
        serializer = serializers.OfferSerializer(offer)
        request = self.factory.patch(
            reverse_querystring('offerid-detail', args=(offer.id,)), data=serializer.data
        )
        resp = self.view_detail.as_view({'patch': 'update'})(request, id=offer.id)
        self.assertEqual(models.Offer.objects.all().count(), 1)
        self.assertEqual(resp.data['rate_min'], 20)
        self.assertEqual(resp.data['bank_name'], 'TEST')

    def test_filter_1(self):
        self.create_offers()
        querystring = {
            'payment_max': '400'
        }
        request = self.factory.get(
            reverse_querystring('offer-list', query_kwargs=querystring)
        )
        resp = self.view_list.as_view({'get': 'list'})(request)
        self.assertEqual(resp.status_code, 200)
        serializer = serializers.OfferSerializer(data=resp.data, many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.data), 1)

    def test_filter_2(self):
        self.create_offers()
        querystring = {
            'rate_min': '100',
            'rate_max': '200'
        }
        request = self.factory.get(
            reverse_querystring('offer-list', query_kwargs=querystring)
        )
        resp = self.view_list.as_view({'get': 'list'})(request)
        self.assertEqual(resp.status_code, 200)
        serializer = serializers.OfferSerializer(data=resp.data, many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.data), 3)

    def test_no_filter(self):
        self.create_offers()
        request = self.factory.get(
            reverse_querystring('offer-list')
        )
        resp = self.view_list.as_view({'get': 'list'})(request)
        self.assertEqual(resp.status_code, 200)
        serializer = serializers.OfferSerializer(data=resp.data, many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.data), 4)

    def test_sort(self):
        self.create_offers()
        querystring = {
            'order': 'rate'
        }
        request = self.factory.get(
            reverse_querystring('offer-list', query_kwargs=querystring)
        )
        resp = self.view_list.as_view({'get': 'list'})(request)
        self.assertEqual(resp.status_code, 200)
        serializer = serializers.OfferSerializer(data=resp.data, many=True)
        serializer.is_valid(raise_exception=True)
        for i in range(1,len(serializer.data)):
            self.assertGreaterEqual(
                serializer.data[i]['rate_min'],
                serializer.data[i-1]['rate_min'])


    def test_price(self):
        models.Offer.objects.create(
            bank_name='test',
            term_min='10', term_max='30',
            rate_min='10', rate_max='16.5',
            payment_min='1000000', payment_max='10000000',
        )
        querystring = {
            'price': '10000000',
            'term': '20',
            'deposit': '10',
        }
        request = self.factory.get(
            reverse_querystring('offer-list', query_kwargs=querystring)
        )
        resp = self.view_list.as_view({'get': 'list'})(request)
        self.assertEqual(resp.status_code, 200)
        serializer = serializers.OfferSerializer(data=resp.data, many=True)
        serializer.is_valid(raise_exception=True)

        self.assertEqual(json.loads(json.dumps(resp.data))[0]['payment'], 86852)

    def test_api_price(self):
        models.Offer.objects.create(
            bank_name='test',
            term_min='10', term_max='30',
            rate_min='2', rate_max='9.8',
            payment_min='1000000', payment_max='10000000',
        )
        querystring = {
            'price': '10000000',
            'term': '20',
            'deposit': '10',
        }
        request = self.factory.get(
            reverse_querystring('offer-list', query_kwargs=querystring)
        )
        resp = self.view_list.as_view({'get': 'list'})(request)
        self.assertEqual(resp.status_code, 200)
        serializer = serializers.OfferSerializer(data=resp.data, many=True)
        serializer.is_valid(raise_exception=True)
        # Значения в доках API не правильные
        self.assertEqual(json.loads(json.dumps(resp.data))[0]['payment'], 75995)
