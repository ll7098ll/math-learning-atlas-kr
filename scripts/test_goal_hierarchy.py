import unittest
from goal_hierarchy import validate_condition_source


class ScopedGoalDependencyTests(unittest.TestCase):
    def setUp(self):
        self.goals={'C:radius':{},'C:diameter':{},'P:segment':{}}
        self.case={'goal_ids':['C:radius','C:diameter']}

    def test_sibling_goal_can_support_a_later_goal_in_same_case(self):
        source={'kind':'goal','goal_id':'C:radius','applies_to_goal_ids':['C:diameter'],'rationale':'Use the constructed radius to interpret two radii as a diameter'}
        self.assertEqual(validate_condition_source(source,self.case,self.goals),['C:diameter'])

    def test_a_goal_cannot_require_itself_even_inside_a_composite_case(self):
        source={'kind':'goal','goal_id':'C:radius','applies_to_goal_ids':['C:radius','C:diameter'],'rationale':'Invalid self requirement'}
        with self.assertRaises(AssertionError):validate_condition_source(source,self.case,self.goals)

    def test_unknown_or_missing_condition_targets_are_rejected(self):
        for targets in ([],['P:segment'],['C:diameter','C:diameter']):
            source={'kind':'goal','goal_id':'C:radius','applies_to_goal_ids':targets,'rationale':'Check exact target scope'}
            with self.assertRaises(AssertionError):validate_condition_source(source,self.case,self.goals)

    def test_legacy_whole_case_scope_still_rejects_reflexive_requirements(self):
        source={'kind':'goal','goal_id':'C:radius','rationale':'No explicit narrower target'}
        with self.assertRaises(AssertionError):validate_condition_source(source,self.case,self.goals)
        source['goal_id']='P:segment'
        self.assertEqual(validate_condition_source(source,self.case,self.goals),self.case['goal_ids'])


if __name__=='__main__':unittest.main()
