from tests.mock.db_session import (  # noqa
    setup_test_db,
    teardown_test_db,
)


class HandleDBTest:
    """This Class assures that all tests within a subclass are done in
    the same database-circumstances
    """
    def setup_method(self):
        # populate_test_tables
        setup_test_db()

    def teardown_method(self):
        teardown_test_db()

    @classmethod
    def teardown_class(cls):
        setup_test_db()
