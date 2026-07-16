import unittest
from ikp_platform.core.ontology.models import Platform, SlotMapping

class TestTopology(unittest.TestCase):
    def test_slot_mapping(self):
        platform = Platform(id="plat1", title="DL380")
        mapping = SlotMapping(id="slotmap1", title="Mezz 1 Mapping", source_slot="Mezzanine 1", target_bays=["Bay 1", "Bay 4"])
        
        platform.slot_mapping_ids.append(mapping.id)
        
        self.assertEqual(mapping.source_slot, "Mezzanine 1")
        self.assertEqual(len(platform.slot_mapping_ids), 1)
        self.assertEqual(mapping.type, "Slot Mapping")

if __name__ == '__main__':
    unittest.main()
