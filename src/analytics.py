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
            "total_volume": float(round(result["total_volume"], 2))
        }

    finally:
        cur.close()
        conn.close()


def get_monthly_active_merchants():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                TO_CHAR(DATE_TRUNC('month', event_timestamp), 'YYYY-MM') AS month,
                COUNT(DISTINCT merchant_id) AS active_merchants
            FROM activities
            WHERE status = 'SUCCESS'
            GROUP BY month
            ORDER BY month;
        """)

        results = cur.fetchall()
        return {row["month"]: row["active_merchants"] for row in results}

    finally:
        cur.close()
        conn.close()