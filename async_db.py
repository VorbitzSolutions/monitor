import psycopg
from datetime import datetime
from dbfields import Fields
from idb import IDb

class DbAccess(IDb):
    def __init__(self, log, db_name, db_user, appid, sendmsgid):
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

    async def shut_down(self):
        end_program = 0
        try:
            with self.db_conn.transaction():
                with self.db_conn.cursor() as cur:
                    query = "select status from public.shutdown WHERE id=1;"
                    cur.execute(query)
                    rows = cur.fetchall()
                    i = 0
                    for row in rows: i += row[0]
                    if i > 0:
                        query = "UPDATE public.shutdown SET status=1 WHERE id = 1;"
                        cur.execute(query)
                        end_program = True
                    cur.execute("UPDATE public.shutdown SET status=0 WHERE id=1;")
        except RuntimeError as r:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in invalidate_queue: {r} at {dt}")
        except Exception as x:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in invalidate_queue: {x} at {dt}")
        finally:
            return end_program

    # Get a single row
    async def select_single_row(self, id):
        rows = []
        try:
            with self.db_conn.cursor() as cur:
                query = f"SELECT * FROM domains WHERE domain_id = {id}"
                cur.execute(query)
                rows = cur.fetchall()
                if len(rows) == 0:
                    rows = None
        except RuntimeError as r:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in select_all_tasks: {r} at {dt}")
        except Exception as x:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in select_all_tasks: {x} at {dt}")
        finally:
            return rows

    # Return all rows from the table
    async def select_all_tasks(self) -> []:
        rows = []
        try:
            with self.db_conn.cursor() as cur:
                query = "SELECT * FROM domains"
                cur.execute(query)
                rows = cur.fetchall()
                if len(rows) == 0:
                    rows = None
        except RuntimeError as r:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in select_all_tasks: {r} at {dt}")
        except Exception as x:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in select_all_tasks: {x} at {dt}")
        finally:
            return rows

    # Check to see if data is dirty
    async def invalidate_queue(self) -> bool:
        invalidate: bool = False
        try:
            with self.db_conn.transaction():
                with self.db_conn.cursor() as cur:
                    query = "SELECT 1 FROM domains WHERE status=1"
                    cur.execute(query)
                    rows = cur.fetchall()
                if len(rows) == 0:
                    invalidate = True

        except RuntimeError as r:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in invalidate_queue: {r} at {dt}")
        except Exception as x:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in invalidate_queue: {x} at {dt}")
        finally:
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
                            query = f"UPDATE domains SET status = 0 WHERE domain_id = {id}"
                            cur.execute(query)
            ok = True
        except RuntimeError as r:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in change_status: {r} at {dt}")
        except Exception as x:
            # Handle the error
            dt = datetime.now()
            await self.log.error(f"An error occurred in change_status: {x} at {dt}")
        finally:
            self.db_conn.commit()
            return ok

    def close(self):
        self.db_conn.close()

    def __del__(self):
        self.close()
