import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_cardgame"

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        ''')
        reset()

    def test_functional(self):
        master = new_master_account()
        COMMENT('''
        Create test accounts:
        ''')
        alice = new_account(master)
        carol = new_account(master)

        COMMENT('''
        Create, build and deploy the contract:
        ''')
        host = new_account(master)
        smart = Contract(host, project_from_template(
            CONTRACT_WORKSPACE, template="hello_world", 
            remove_existing=True))
        smart.build()
        smart.deploy()

        COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":alice}, permission=(alice, Permission.ACTIVE))
        self.assertTrue("alice" in DEBUG())

        COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        host.push_action(
            "hi", {"user":carol}, permission=(carol, Permission.ACTIVE))
        self.assertTrue("carol" in DEBUG())

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            host.push_action(
                "hi", {"user":carol}, permission=(bob, Permission.ACTIVE))
 
    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
