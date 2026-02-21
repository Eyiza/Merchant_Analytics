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
    


def get_kyc_funnel():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
            COUNT(DISTINCT CASE 
                WHEN event_type='DOCUMENT_SUBMITTED' THEN merchant_id 
            END) AS documents_submitted,

            COUNT(DISTINCT CASE 
                WHEN event_type='VERIFICATION_COMPLETED' THEN merchant_id 
            END) AS verifications_completed,

            COUNT(DISTINCT CASE 
                WHEN event_type='TIER_UPGRADE' THEN merchant_id 
            END) AS tier_upgrades

            FROM activities
            WHERE product='KYC'
            AND status='SUCCESS';
        """)

        row = cur.fetchone()
        return dict(row)

    finally:
        cur.close()
        conn.close()


def get_failure_rates():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
            product,
            ROUND(
                100.0 * SUM(CASE WHEN status='FAILED' THEN 1 ELSE 0 END) /
                NULLIF(SUM(CASE WHEN status IN ('SUCCESS','FAILED') THEN 1 ELSE 0 END),0)
            ,1) AS failure_rate
            FROM activities
            GROUP BY product
            ORDER BY failure_rate DESC;
        """)

        rows = cur.fetchall()

        return [
            {"product": r["product"], "failure_rate": float(r["failure_rate"])}
            for r in rows
        ]

    finally:
        cur.close()
        conn.close()