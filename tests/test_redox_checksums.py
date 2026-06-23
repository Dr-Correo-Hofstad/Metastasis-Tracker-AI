import unittest
import os
import shutil
from src.data.logs.json_transaction_logger import JSONTransactionLogger

class TestLoggerIntegrityAndCohortAnalytics(unittest.TestCase):
    def setUp(self):
        self.scratch_dir = "tests/scratch_logs"
        self.logger = JSONTransactionLogger(self.scratch_dir)
        
        # Structure sample timeline rows for 2 mock patient builds
        self.p1_data = [{"step": 0, "ph": 7.42, "cbf": 250.0}, {"step": 1, "ph": 7.39, "cbf": 240.0}]
        self.p2_data = [{"step": 0, "ph": 7.12, "cbf": 110.0}, {"step": 1, "ph": 6.95, "cbf": 45.0}]

    def tearDown(self):
        if os.path.exists(self.scratch_dir):
            shutil.rmtree(self.scratch_dir)

    def test_end_to_end_checksum_and_cohort_analytics(self):
        """VERIFICATION: Confirms data verification gates and multi-patient loops pass."""
        # 1. Commit records and verify signature files exist on disk
        f1, hash1 = self.logger.serialize_and_compress_log(self.p1_data, patient_id="pat-alpha")
        f2, hash2 = self.logger.serialize_and_compress_log(self.p2_data, patient_id="pat-beta")
        
        self.assertTrue(self.logger.verify_compressed_log_checksum(f1))
        
        # 2. Simulate malicious data corruption or disk bad sector anomalies
        with open(f1, "ab") as f:
            f.write(b"\x00\xFF_CORRUPT_BYTES")
            
        # The verification gate must intercept the anomaly and flag a breach
        self.assertFalse(self.logger.verify_compressed_log_checksum(f1))
        print("[+] Assert Verified: Cryptographic checkpoint successfully flagged data corruption.")

        # 3. Verify analytics engine processes remaining secure files cleanly
        stats = self.logger.parse_multi_patient_cohort_statistics()
        self.assertEqual(stats["status"], "METRICS_COMPILED_SUCCESSFULLY")
        # Confirms only 1 valid uncorrupt record file is calculated
        self.assertEqual(stats["total_cohort_records_evaluated"], 2)
        self.assertLessEqual(stats["blood_ph_distribution"]["min"], 7.12)

if __name__ == "__main__":
    unittest.main()
