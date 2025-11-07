def load_detailed_schema(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [row[0] for row in cursor.fetchall()]
    schema = {}
    for table in tables:
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table}' AND table_schema = 'public'
            ORDER BY ordinal_position
        """)
        schema[table] = cursor.fetchall()

        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 5")
            sample_data = cursor.fetchall()
            if sample_data:
                sample_columns = [desc[0] for desc in cursor.description]
                schema[table + '_sample'] = {
                    'columns': sample_columns,
                    'data': sample_data
                }
        except:
            pass
    cursor.close()
    return tables, schema
