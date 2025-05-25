from django.test import TestCase
from django.contrib.gis.geos import Point

from .models import Kosan


class KosanModelTests(TestCase):
    def setUp(self):
        # Create dummy object
        self.kosan = Kosan.objects.create(
            nama="Kosan Mawar",
            alamat_lengkap="Jl. Mawar No. 12",
            luas_bangunan=24.5,
            link_lengkap_properti="https://example.com/kosan-mawar",
            geometry=Point(107.6191, -6.9175)  # (longitude, latitude)
        )

    def test_create_kosan(self):
        self.assertEqual(Kosan.objects.count(), 1)
        kosan = Kosan.objects.first()
        self.assertEqual(kosan.nama, "Kosan Mawar")
        self.assertEqual(kosan.geometry.x, 107.6191)
        self.assertEqual(kosan.geometry.y, -6.9175)

    def test_read_kosan(self):
        kosan = Kosan.objects.get(nama="Kosan Mawar")
        self.assertEqual(kosan.alamat_lengkap, "Jl. Mawar No. 12")

    def test_update_kosan(self):
        kosan = self.kosan
        kosan.nama = "Kosan Melati"
        kosan.luas_bangunan = 30.0
        kosan.save()

        updated = Kosan.objects.get(id=kosan.id)
        self.assertEqual(updated.nama, "Kosan Melati")
        self.assertEqual(updated.luas_bangunan, 30.0)

    def test_delete_kosan(self):
        kosan_id = self.kosan.id
        self.kosan.delete()
        self.assertFalse(Kosan.objects.filter(id=kosan_id).exists())

    def test_dunder_str_with_name(self):
        self.assertEqual(str(self.kosan), "Kosan Mawar")

    def test_dunder_str_without_name(self):
        kosan = Kosan.objects.create(
            nama=None,
            geometry=Point(107.6191, -6.9175)
        )
        self.assertEqual(str(kosan), "Kosan tanpa nama")
