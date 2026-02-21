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

        row = cur.fetchone()

        if not row:
            return None

        return {
            "merchant_id": row["merchant_id"],
            "total_volume": float(round(row["total_volume"], 2))
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

        rows = cur.fetchall()
        return {row["month"]: row["active_merchants"] for row in rows}

    finally:
        cur.close()
        conn.close()


def get_product_adoption():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                product, COUNT(DISTINCT merchant_id) AS merchant_count
            FROM activities
            GROUP BY product
            ORDER BY merchant_count DESC;
        """)

        rows = cur.fetchall()
        return {row["product"]: row["merchant_count"] for row in rows}

    finally:
        cur.close()
        conn.close()