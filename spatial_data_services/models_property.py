from django.contrib.gis.db import models


class Property(models.Model):
    geometry = models.PointField(
        geography=True,
        srid=4326,
        verbose_name="Lokasi Properti",
        help_text="Titik koordinat (longitude, latitude)"
    )

    nama_properti = models.CharField(
        max_length=255,
        verbose_name="Nama Properti"
    )
    alamat_lengkap = models.TextField(
        blank=True,
        verbose_name="Alamat Lengkap"
    )
    kelurahan = models.CharField(
        max_length=100,
        verbose_name="Kelurahan"
    )
    jalan_terdekat = models.TextField(
        verbose_name="Jalan Terdekat"
    )
    kategori_properti = models.CharField(
        max_length=50,
        verbose_name="Kategori Properti"
    )
    status_properti = models.CharField(
        max_length=50,
        verbose_name="Status Properti"
    )
    harga_properti = models.IntegerField(
        verbose_name="Harga Properti (IDR)"
    )
    luas_bangunan = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Luas Bangunan (m²)"
    )
    luas_tanah = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Luas Tanah (m²)"
    )
    kecamatan = models.CharField(
        max_length=100,
        verbose_name="Kecamatan"
    )
    link_lengkap_properti = models.URLField(
        max_length=500,
        verbose_name="Link Lengkap Properti"
    )

    def __str__(self):
        return f"{self.nama_properti} ({self.kelurahan}, {self.kecamatan})"
