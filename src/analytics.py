from src.db import get_connection

def get_top_merchant():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT merchant_id, SUM(amount) AS total_volume
            FROM activities
            WHERE status = 'SUCCESS'
            GROUP BY merchant_id
            ORDER BY total_volume DESC
            LIMIT 1;
        """)

        result = cur.fetchone()

        if not result:
            return None

        return {
            "merchant_id": result["merchant_id"],
            "total_volume": float(result["total_volume"])
        }

    finally:
        cur.close()
        conn.close()