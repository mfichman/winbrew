import winbrewtest
import winbrew.execute

class MockArgs(object):
    force = False

class InstallPlanTest(winbrewtest.TestCase):

    def test_dependencies(self): 
        formula = winbrew.Formula.formula_by_name('sfml')()
        plan = winbrew.execute.InstallPlan([formula], MockArgs())
        plan = [p.name for p in plan]
        assert(plan == ['cmake', 'sfml']) 

    def test_multiple(self): 
        formula = [winbrew.Formula.formula_by_name(n)() for n in ('openssl','sfml')]
        plan = winbrew.execute.InstallPlan(formula, MockArgs())
        plan = [p.name for p in plan]
        assert(plan == ['perl', 'openssl', 'cmake', 'sfml']) 

