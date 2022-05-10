import unittest
'''
Basic app unit tests
'''

from omero_search_client import omero_client_app, create_app
create_app('testing')

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        pass#d_util.createdatabase(db)

    def tearDown(self):
        pass#d_util.drop_all_databases(db)

    def test_main(self):
        '''test home page'''
        tester = omero_client_app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        '''
        test not found url
        :return:
        '''
        tester = omero_client_app.test_client(self)
        response = tester.get('a12', content_type='html/text')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
