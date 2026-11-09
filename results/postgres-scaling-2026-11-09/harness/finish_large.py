"""Separate the index-maintenance deadline from query timing configuration."""
import json
import sys
import index_and_benchmark as benchmark
from pg_helpers import HERE, dump


def main():
    original_connect = benchmark.connect

    def maintenance_connection():
        pg = original_connect()
        pg.execute("SET statement_timeout='30min'")
        return pg

    benchmark.connect = maintenance_connection
    sys.argv = ['index_and_benchmark.py', 'stage2_large', 'indexes']
    benchmark.main()
    benchmark.connect = original_connect
    with original_connect() as pg:
        timeout = pg.execute('SHOW statement_timeout').fetchone()[0]
        indexes = pg.execute("SELECT c.relname,i.indisvalid,i.indisready FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' ORDER BY c.relname").fetchall()
        assert timeout == '5min', timeout
        assert len(indexes) == 14 and all(valid and ready for _, valid, ready in indexes), indexes
        dump(HERE / 'results/large-index-validation.json', {'statement_timeout': timeout, 'indexes': indexes, 'all14valid_ready': True})
    sys.argv = ['index_and_benchmark.py', 'stage2_large', 'queries', '--bracket-q03']
    benchmark.main()


if __name__ == '__main__':
    main()
