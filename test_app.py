import unittest
import json
import os
import database
from app import app

class TestLaptopManagementSystem(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_dashboard_stats(self):
        """Uji API statistik papan pemuka."""
        response = self.app.get('/api/dashboard/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('total_records', data['data'])
        self.assertIn('total_laptops', data['data'])
        self.assertIn('total_departments', data['data'])
        self.assertIn('recent_activities', data['data'])
        print("\n[OK] Ujian Papan Pemuka Berjaya: ", data['data']['total_records'], "rekod dikesan.")

    def test_02_get_all_records(self):
        """Uji dapatkan senarai rekod peminjaman."""
        response = self.app.get('/api/records')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 0)
        print("[OK] Ujian Dapatkan Rekod Berjaya: Jumlah rekod =", data['count'])

    def test_03_create_record(self):
        """Uji pendaftaran rekod peminjaman baharu."""
        payload = {
            "nama_laptop": "Asus ZenBook 14 OLED",
            "nama_jabatan": "Fakulti Sains Komputer",
            "tarikh_peminjaman": "2026-10-14",
            "tujuan": "Ujian pembangunan sistem dan pembentangan projek tahun akhir"
        }
        response = self.app.post(
            '/api/records',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['record']['nama_laptop'], "Asus ZenBook 14 OLED")
        self.__class__.created_id = data['record']['id']
        print(f"[OK] Ujian Tambah Rekod Berjaya: ID #{self.__class__.created_id}")

    def test_04_create_record_validation(self):
        """Uji pengesahan data wajib semasa pendaftaran."""
        payload = {
            "nama_laptop": "",
            "nama_jabatan": "Fakulti Sains",
            "tarikh_peminjaman": "2026-10-14",
            "tujuan": "Tiada"
        }
        response = self.app.post(
            '/api/records',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        print("[OK] Ujian Pengesahan Borang Berjaya: Mesej ralat dikembalikan dengan betul.")

    def test_05_update_record(self):
        """Uji kemaskini rekod peminjaman."""
        record_id = getattr(self.__class__, 'created_id', 1)
        payload = {
            "nama_laptop": "Asus ZenBook 14 OLED (Terkemaskini)",
            "nama_jabatan": "Fakulti Sains Komputer & Matematik",
            "tarikh_peminjaman": "2026-10-15",
            "tujuan": "Ujian integrasi sistem berskala besar"
        }
        response = self.app.put(
            f'/api/records/{record_id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['record']['nama_laptop'], "Asus ZenBook 14 OLED (Terkemaskini)")
        print(f"[OK] Ujian Kemaskini Rekod Berjaya untuk ID #{record_id}")

    def test_06_search_and_filter(self):
        """Uji carian dan penapisan tarikh."""
        # Carian mengikut kata kunci
        response = self.app.get('/api/records?search=Asus')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['count'], 1)

        # Carian mengikut tarikh
        response_date = self.app.get('/api/records?date=2026-10-15')
        self.assertEqual(response_date.status_code, 200)
        data_date = json.loads(response_date.data)
        self.assertTrue(data_date['success'])
        self.assertGreaterEqual(data_date['count'], 1)
        print("[OK] Ujian Carian dan Tapisan Tarikh Berjaya.")

    def test_07_delete_record(self):
        """Uji pemadaman rekod peminjaman."""
        record_id = getattr(self.__class__, 'created_id', None)
        if record_id:
            response = self.app.delete(f'/api/records/{record_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])

            # Pastikan rekod telah dipadam
            check = self.app.get(f'/api/records/{record_id}')
            self.assertEqual(check.status_code, 404)
            print(f"[OK] Ujian Padam Rekod Berjaya untuk ID #{record_id}")

if __name__ == '__main__':
    unittest.main()
