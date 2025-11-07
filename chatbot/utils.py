def format_answer(question, df, max_rows=20):
    """
    Formats the SQL query result DataFrame into a user-readable string.

    - Returns explicit counts for count queries.
    - Returns table-formatted results for other queries.
    - Limits output to `max_rows` rows if data is large.
    """
    if df.empty:
        return "No matching records found."

    # Detect if this is a count query by inspecting columns
    if len(df.columns) == 1 and 'count' in df.columns[0].lower():
        count_value = df.iloc[0, 0]
        return f"Count: {count_value}"

    # For all other queries, return formatted table string
    if len(df) > max_rows:
        limited_df = df.head(max_rows)
        result_str = limited_df.to_string(index=False)
        more_rows = len(df) - max_rows
        return f"{result_str}\n\n... and {more_rows} more rows."
    else:
        return df.to_string(index=False)
