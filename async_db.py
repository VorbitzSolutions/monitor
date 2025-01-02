import psycopg
from dbfields import Fields

class DbAccess:
    def __init__(self, log, db_name, db_user,appid,sendmsgid):
        self.get_all_rows_sql = "SELECT * FROM domains"
        self.fetch_row_sql = "SELECT * FROM domains WHERE domain_id = %s"
        self.cheeck_new_or_updated = "SELECT 1 FROM domains WHERE status=1"
        self.set_status = "UPDATE domains SET status = 0 WHERE domain_id = %s"
        self.send_msg = "INSERT INTO messages (source_id,destanation_id, status, msg, created_ts, closed_ts) \
        VALUES (%s,%s,true,%s,now(),now())"

        self.log = log
        s = f"dbname={db_name} user={db_user}"
        self.db_conn = psycopg.connect(s)
        '''
        self.db_conn = psycopg.connect(
            host="localhost",
            database=db_name,
            user=db_user,
            password=""
        )
        '''

    # Get a single row
    async def select_single_row(self, id):
        rows = []
        try:
            with self.db_conn.cursor() as cur:
                sql = self.fetch_row_sql + f" {id}"
                cur.execute(sql)
                rows = cur.fetchall()
                if len(rows) == 0:
                    rows = None
        except RuntimeError as r:
            # Handle the error
            await self.log.error(f"An error occurred in select_all_tasks: {r}")
        except Exception as x:
            # Handle the error
            await self.log.error(f"An error occurred in select_all_tasks: {x}")
        finally:
            return rows

    # Return all rows from the table
    async def select_all_tasks(self) -> []:
        rows = []
        try:
            with self.db_conn.cursor() as cur:
                cur.execute(self.get_all_rows_sql)
                rows = cur.fetchall()
                if len(rows) == 0:
                    rows = None
        except RuntimeError as r:
            # Handle the error
            await self.log.error(f"An error occurred in select_all_tasks: {r}")
        except Exception as x:
            # Handle the error
            await self.log.error(f"An error occurred in select_all_tasks: {x}")
        finally:
            return rows

    # Check to see if data is dirty
    async def invalidate_queue(self) -> bool:
        invalidate: bool = False
        try:
            with self.db_conn.transaction():
                with self.db_conn.cursor() as cur:
                    cur.execute(self.cheeck_new_or_updated)
                    rows = cur.fetchall()
                if len(rows) == 0:
                    invalidate = True

        except RuntimeError as r:
            # Handle the error
            await self.log.error(f"An error occurred in invalidate_queue: {r}")
        except Exception as x:
            # Handle the error
            await self.log.error(f"An error occurred in invalidate_queue: {x}")
        finally:
            self.db_conn.commit()
            return invalidate

    # Set or reset the status flag
    async def change_status(self, dlist: list) -> bool:
        ok = False

        try:
            with self.db_conn.transaction():
                with self.db_conn.cursor() as cur:
                    for d in dlist:
                        id = d[Fields.id.value]
                        status = d[Fields.status.value]
                        if status == 1:
                            cur.execute(self.set_status,(id,))
            ok = True
        except RuntimeError as r:
            # Handle the error
            await self.log.error(f"An error occurred in change_status: {r}")
        except Exception as x:
            # Handle the error
            await self.log.error(f"An error occurred in change_status: {x}")
        finally:
            self.db_conn.commit()
            return ok

    def close(self):
        self.db_conn.close()

    def __del__(self):
        self.close()

