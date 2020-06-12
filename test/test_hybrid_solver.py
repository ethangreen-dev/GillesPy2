import unittest
import numpy as np
import gillespy2
from gillespy2.core.gillespyError import *
from example_models import Example
from gillespy2 import TauHybridSolver


class TestBasicTauHybridSolver(unittest.TestCase):

    def test_add_rate_rule(self):
        model = Example()
        species = gillespy2.Species('test_species', initial_value=1)
        rule = gillespy2.RateRule(name='rr1',formula='test_species+1',variable='test_species')
        model.add_species([species])
        model.add_rate_rule([rule])
        results = model.run()
        self.assertEqual(results[0].solver_name, 'TauHybridSolver')

    def test_add_rate_rule_dict(self):
        model = Example()
        species2 = gillespy2.Species('test_species2', initial_value=2, mode='continuous')
        species3 = gillespy2.Species('test_species3', initial_value=3, mode='continuous')
        rule2 = gillespy2.RateRule(species2, 'cos(t)')
        rule3 = gillespy2.RateRule(variable=species3, formula='sin(t)')
        rate_rule_dict = {'rule2': rule2, 'rule3': rule3}
        model.add_species([species2, species3])
        with self.assertRaises(ParameterError):
            model.add_rate_rule(rate_rule_dict)

    def test_add_bad_species_rate_rule_dict(self):
        model = Example()
        rule = gillespy2.RateRule(formula='sin(t)')
        with self.assertRaises(ModelError):
            model.add_rate_rule(rule)

    def test_add_assignment_rule(self):
        model = Example()
        species = gillespy2.Species('test_species4', initial_value=1)
        rule = gillespy2.AssignmentRule(name='ar1', variable=species.name, formula='2')
        model.add_species([species])
        model.add_assignment_rule([rule])
        results = model.run()
        self.assertEquals(results[species.name][0], 2) 
        self.assertEquals(results[species.name][-1], 2)
        self.assertEqual(results[0].solver_name,'TauHybridSolver')

    def test_add_function_definition(self):
        model = Example()
        funcdef = gillespy2.FunctionDefinition(name='fun', function='Sp+1')
        model.add_function_definition(funcdef)
        results = model.run()
        self.assertEqual(results[0].solver_name,'TauHybridSolver')

    def test_add_event(self):
        model = Example()
        eventTrig = gillespy2.EventTrigger(expression='Sp+1', initial_value=True, )
        event1 = gillespy2.Event(name='event1', trigger=eventTrig)
        model.add_event(event1)
        results = model.run()
        self.assertEqual(results[0].solver_name,'TauHybridSolver')

    def test_math_name_overlap(self):
        model = Example()
        gamma = gillespy2.Species('gamma',initial_value=2, mode='continuous')
        model.add_species([gamma])
        k2 = gillespy2.Parameter(name='k2', expression=1)
        model.add_parameter([k2])
        gamma_react = gillespy2.Reaction(name='gamma_react', reactants={'gamma': 1}, products={}, rate=k2)
        model.add_reaction([gamma_react])
        model.run(solver=TauHybridSolver)

    def test_add_bad_expression_rate_rule_dict(self):
        model = Example()
        species2 = gillespy2.Species('test_species2', initial_value=2, mode='continuous')
        rule = gillespy2.RateRule(variable=species2, formula='')
        with self.assertRaises(ModelError):
            model.add_rate_rule(rule)

    def test_ensure_hybrid_dynamic_species(self):
        model = Example()
        species1 = gillespy2.Species('test_species1',initial_value=1,mode='dynamic')
        model.add_species(species1)
        results = model.run()
        self.assertEqual(results[0].solver_name, 'TauHybridSolver')

    def test_ensure_hybrid_continuous_species(self):
        model = Example()
        species1 = gillespy2.Species('test_species1',initial_value=1,mode='continuous')
        model.add_species(species1)
        results = model.run()
        self.assertEqual(results[0].solver_name, 'TauHybridSolver')

    def test_ensure_continuous_dynamic_timeout_warning(self):
        model = Example()
        species1 = gillespy2.Species('test_species1', initial_value=1, mode='dynamic')
        model.add_species(species1)
        with self.assertLogs(level='WARN'):
            results = model.run(timeout=1)


if __name__ == '__main__':
    unittest.main()
