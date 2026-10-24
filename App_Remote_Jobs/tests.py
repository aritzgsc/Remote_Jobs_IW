from django.test import TestCase
from django.urls import reverse

class InicioTests(TestCase):
    def test_la_portada_responde(self):
        respuesta = self.client.get(reverse("jobs:inicio"))
        self.assertEqual(respuesta.status_code, 200)
