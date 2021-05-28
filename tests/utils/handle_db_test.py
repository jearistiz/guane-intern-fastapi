from tests.mock.db_session import clean_all_test_tables, populate_test_tables


class HandleDBTest:
    def setup_method(self):
        populate_test_tables()

    def teardown_method(self):
        clean_all_test_tables()

    @classmethod
    def teardown_class(cls):
        populate_test_tables()
