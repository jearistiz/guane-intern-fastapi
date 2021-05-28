from tests.mock.db_session import (  # noqa
    close_test_db,
    init_test_db,
)


class HandleDBTest:
    """This Class assures that all tests within a subclass are done in
    the same database-circumstances
    """
    def setup_method(self):
        # populate_test_tables
        init_test_db()

    def teardown_method(self):
        close_test_db()

    @classmethod
    def teardown_class(cls):
        init_test_db()
