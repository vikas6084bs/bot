import pandas as pd
from .utils import format_answer

class QueryExecutor:
    def __init__(self, conn):
        self.conn = conn

    def execute_with_smart_matching(self, question, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)

            if sql.strip().upper().startswith('SELECT'):
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                cursor.close()

                if results:
                    df = pd.DataFrame(results, columns=columns)
                    return format_answer(question, df)
                else:
                    return "No results found."
            else:
                self.conn.commit()
                cursor.close()
                return "Action completed successfully."

        except Exception as e:
            cursor.close()
            return f"Error during query execution: {str(e)}"
