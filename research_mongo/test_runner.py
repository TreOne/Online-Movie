from research_mongo.tests import read_tests, write_tests, check_count_in_tables

from research_mongo.tests_postgres import read_tests as postgres_read_tests, write_tests as postgres_write_tests, \
    check_count_in_tables as postgres_check_count_in_tables

if __name__ == "__main__":
    # Mongo
    for test in read_tests:
        test()
    for test in write_tests:
        test()
    check_count_in_tables()
    # Postgres
    for test in postgres_read_tests:
        test()
    for test in postgres_write_tests:
        test()
    postgres_check_count_in_tables()