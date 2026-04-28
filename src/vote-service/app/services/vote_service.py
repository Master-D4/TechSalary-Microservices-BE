from sqlalchemy.orm import Session
from app.models.vote import Report, Vote
from sqlalchemy import func, text
from sqlalchemy.exc import IntegrityError

APPROVAL_SCORE_THRESHOLD = 5
REJECTION_THRESHOLD = 5
REPORT_THRESHOLD = 5

def create_vote(db: Session, salary_submission_id: int, user_id: int, vote_type: str):
    user_id = int(user_id)

    existing = db.query(Vote).filter(
        Vote.salary_submission_id == salary_submission_id,
        Vote.user_id == user_id
    ).first()

    try:
        if existing:
            # Update existing vote
            existing.vote_type = vote_type
        else:
            # Insert new vote
            vote = Vote(
                salary_submission_id=salary_submission_id,
                user_id=user_id,
                vote_type=vote_type
            )
            db.add(vote)

        db.commit()

    except IntegrityError:
        db.rollback()
        return {"error": "Invalid vote data"}

    # Count UP votes
    up_votes = db.query(func.count(Vote.id)).filter(
        Vote.salary_submission_id == salary_submission_id,
        Vote.vote_type == "UP"
    ).scalar()

    # Count DOWN votes
    down_votes = db.query(func.count(Vote.id)).filter(
        Vote.salary_submission_id == salary_submission_id,
        Vote.vote_type == "DOWN"
    ).scalar()

    score = up_votes - down_votes

    # 🔥 Status decision logic
    if down_votes >= REJECTION_THRESHOLD:
        new_status = "REJECTED"
    elif score >= APPROVAL_SCORE_THRESHOLD:
        new_status = "APPROVED"
    else:
        new_status = "PENDING"

    db.execute(
        text("""
        UPDATE salary.salary_submissions
        SET status = :status
        WHERE id = :salary_submission_id
        """),
        {"status": new_status, "salary_submission_id": salary_submission_id}
    )
    db.commit()

    return {
        "message": "Vote recorded or updated",
        "up_votes": up_votes,
        "down_votes": down_votes,
        "score": score,
        "status": new_status
    }
# service function
def delete_vote_service(db: Session, salary_submission_id: int, user_id: int):
    """Delete a user's vote and recalculate submission status"""
    user_id = int(user_id)
    
    # Find existing vote
    existing = db.query(Vote).filter(
        Vote.salary_submission_id == salary_submission_id,
        Vote.user_id == user_id
    ).first()
    
    if not existing:
        return {"error": "No vote found to delete"}
    
    try:
        # Delete the vote
        db.delete(existing)
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"error": "Failed to delete vote"}
    
    # Recalculate votes after deletion
    up_votes = db.query(func.count(Vote.id)).filter(
        Vote.salary_submission_id == salary_submission_id,
        Vote.vote_type == "UP"
    ).scalar()

    down_votes = db.query(func.count(Vote.id)).filter(
        Vote.salary_submission_id == salary_submission_id,
        Vote.vote_type == "DOWN"
    ).scalar()

    score = up_votes - down_votes

    if down_votes >= REJECTION_THRESHOLD:
        new_status = "REJECTED"
    elif score >= APPROVAL_SCORE_THRESHOLD:
        new_status = "APPROVED"
    else:
        new_status = "PENDING"

    # Update submission status
    db.execute(
        text("""UPDATE salary.salary_submissions
                SET status = :status
                WHERE id = :salary_submission_id"""),
        {"status": new_status, "salary_submission_id": salary_submission_id}
    )
    db.commit()

    return {
        "message": "Vote deleted successfully",
        "up_votes": up_votes,
        "down_votes": down_votes,
        "score": score,
        "status": new_status
    }
def create_report(db: Session, salary_submission_id: int, user_id: int, reason: str):
    # Check if user already reported
    existing_report = db.query(Report).filter(
        Report.salary_submission_id == salary_submission_id,
        Report.user_id == user_id
    ).first()

    # Grab current status upfront
    status_row = db.execute(text("""
        SELECT status
        FROM salary.salary_submissions
        WHERE id = :salary_submission_id
    """), {"salary_submission_id": salary_submission_id}).fetchone()
    current_status = status_row[0] if status_row else None
    new_status = current_status

    # Compute total reports (including current user if they already reported)
    total_reports = db.query(func.count(Report.id)).filter(
        Report.salary_submission_id == salary_submission_id
    ).scalar()

    if existing_report:
        # If threshold reached, ensure status marked REPORTED
        if total_reports >= REPORT_THRESHOLD and current_status != "REPORTED":
            new_status = "REPORTED"
            db.execute(text("""
                UPDATE salary.salary_submissions
                SET status = :status
                WHERE id = :salary_submission_id
            """), {"status": new_status, "salary_submission_id": salary_submission_id})
            db.commit()

        return {
            "message": "You have already reported this submission",
            "report_id": existing_report.id,
            "total_reports": total_reports,
            "status": new_status
        }

    report = Report(
        salary_submission_id=salary_submission_id,
        user_id=user_id,
        reason=reason
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    # Recount after adding this report
    total_reports = db.query(func.count(Report.id)).filter(
        Report.salary_submission_id == salary_submission_id
    ).scalar()

    # If reports reach threshold, flag submission as REPORTED
    if total_reports >= REPORT_THRESHOLD and current_status != "REPORTED":
        new_status = "REPORTED"
        db.execute(text("""
            UPDATE salary.salary_submissions
            SET status = :status
            WHERE id = :salary_submission_id
        """), {"status": new_status, "salary_submission_id": salary_submission_id})
        db.commit()

    return {
        "message": "Report submitted successfully",
        "report_id": report.id,
        "total_reports": total_reports,
        "status": new_status
    }


def delete_report_service(db: Session, salary_submission_id: int, user_id: int):
    report = db.query(Report).filter(
        Report.salary_submission_id == salary_submission_id,
        Report.user_id == user_id
    ).first()

    if not report:
        return {"message": "No report found to delete"}

    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}
