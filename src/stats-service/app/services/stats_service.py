from sqlalchemy import text
from sqlalchemy.orm import Session


class StatsService:
    @staticmethod
    def _base_filter_sql():
        return """
            FROM salary.salary_submissions
            WHERE status = 'APPROVED'
              AND (:location IS NULL OR location = :location)
              AND (:job_title IS NULL OR job_title = :job_title)
        """

    @staticmethod
    def _base_params(location=None, job_title=None):
        return {
            "location": location,
            "job_title": job_title,
        }

    @staticmethod
    def get_filters(db: Session):
        countries_query = text(
            """
            SELECT DISTINCT location
            FROM salary.salary_submissions
            WHERE status = 'APPROVED'
            ORDER BY location
            """
        )

        roles_query = text(
            """
            SELECT DISTINCT job_title
            FROM salary.salary_submissions
            WHERE status = 'APPROVED'
            ORDER BY job_title
            """
        )

        countries = [row[0] for row in db.execute(countries_query).all()]
        roles = [row[0] for row in db.execute(roles_query).all()]

        return {
            "countries": countries,
            "roles": roles,
        }

    @staticmethod
    def get_summary(db: Session, location=None, job_title=None):
        query = text(
            f"""
            SELECT
                COUNT(*) AS total_entries,
                AVG(salary_amount) AS average_salary,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_amount) AS median_salary
            {StatsService._base_filter_sql()}
            """
        )

        row = db.execute(
            query,
            StatsService._base_params(location=location, job_title=job_title),
        ).mappings().first()

        return {
            "total_entries": row["total_entries"] or 0,
            "average_salary": float(row["average_salary"]) if row["average_salary"] is not None else None,
            "median_salary": float(row["median_salary"]) if row["median_salary"] is not None else None,
        }

    @staticmethod
    def get_percentiles(db: Session, location=None, job_title=None):
        query = text(
            f"""
            SELECT
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary_amount) AS p25_salary,
                PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY salary_amount) AS p50_salary,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary_amount) AS p75_salary,
                PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY salary_amount) AS p90_salary
            {StatsService._base_filter_sql()}
            """
        )

        row = db.execute(
            query,
            StatsService._base_params(location=location, job_title=job_title),
        ).mappings().first()

        return {
            "p25_salary": float(row["p25_salary"]) if row["p25_salary"] is not None else None,
            "p50_salary": float(row["p50_salary"]) if row["p50_salary"] is not None else None,
            "p75_salary": float(row["p75_salary"]) if row["p75_salary"] is not None else None,
            "p90_salary": float(row["p90_salary"]) if row["p90_salary"] is not None else None,
        }

    @staticmethod
    def get_by_experience(db: Session, location=None, job_title=None):
        query = text(
            """
            WITH filtered AS (
                SELECT
                    CASE
                        WHEN years_experience BETWEEN 0 AND 2 THEN '0-2'
                        WHEN years_experience BETWEEN 3 AND 5 THEN '3-5'
                        WHEN years_experience BETWEEN 6 AND 9 THEN '6-9'
                        ELSE '10+'
                    END AS experience_range,
                    salary_amount
                FROM salary.salary_submissions
                WHERE status = 'APPROVED'
                  AND (:location IS NULL OR location = :location)
                  AND (:job_title IS NULL OR job_title = :job_title)
            )
            SELECT
                experience_range,
                COUNT(*) AS count,
                AVG(salary_amount) AS average_salary
            FROM filtered
            GROUP BY experience_range
            ORDER BY
                CASE experience_range
                    WHEN '0-2' THEN 1
                    WHEN '3-5' THEN 2
                    WHEN '6-9' THEN 3
                    ELSE 4
                END
            """
        )

        rows = db.execute(
            query,
            StatsService._base_params(location=location, job_title=job_title),
        ).mappings().all()

        return [
            {
                "experience_range": row["experience_range"],
                "count": row["count"],
                "average_salary": float(row["average_salary"]) if row["average_salary"] is not None else None,
            }
            for row in rows
        ]

    @staticmethod
    def get_top_roles(db: Session, location=None, job_title=None, limit=10):
        query = text(
            """
            SELECT
                job_title,
                AVG(salary_amount) AS average_salary,
                COUNT(*) AS count
            FROM salary.salary_submissions
            WHERE status = 'APPROVED'
              AND (:location IS NULL OR location = :location)
              AND (:job_title IS NULL OR job_title = :job_title)
            GROUP BY job_title
            ORDER BY AVG(salary_amount) DESC
            LIMIT :limit
            """
        )

        rows = db.execute(
            query,
            {
                "location": location,
                "job_title": job_title,
                "limit": limit,
            },
        ).mappings().all()

        return [
            {
                "job_title": row["job_title"],
                "average_salary": float(row["average_salary"]),
                "count": row["count"],
            }
            for row in rows
        ]

    @staticmethod
    def get_submissions_by_country(db: Session, location=None, job_title=None, limit=20):
        query = text(
            """
            SELECT
                location AS country,
                COUNT(*) AS count
            FROM salary.salary_submissions
            WHERE status = 'APPROVED'
              AND (:location IS NULL OR location = :location)
              AND (:job_title IS NULL OR job_title = :job_title)
            GROUP BY location
            ORDER BY COUNT(*) DESC, location ASC
            LIMIT :limit
            """
        )

        rows = db.execute(
            query,
            {
                "location": location,
                "job_title": job_title,
                "limit": limit,
            },
        ).mappings().all()

        return [
            {
                "country": row["country"],
                "count": row["count"],
            }
            for row in rows
        ]