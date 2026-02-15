from sqlalchemy.orm import Session
from app.models.vote import Vote
from sqlalchemy import func, text
from sqlalchemy.exc import IntegrityError

APPROVAL_THRESHOLD = 3

def create_vote(db: Session, submission_id: int, user_id: int, vote_type: str):
    user_id = int(user_id)

    # Prevent duplicate vote
    existing = db.query(Vote).filter(
        Vote.salary_submission_id == submission_id,
        Vote.user_id == user_id
    ).first()

    if existing:
        return {"error": "User already voted"}

    vote = Vote(
        salary_submission_id=submission_id,
        user_id=user_id,
        vote_type=vote_type
    )

    try:
        db.add(vote)
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"error": "Invalid vote data or duplicate vote"}

    # Count UP votes
    upvotes = db.query(func.count(Vote.id)).filter(
        Vote.salary_submission_id == submission_id,
        Vote.vote_type == "UP"
    ).scalar()

    # If threshold reached → mark APPROVED
    if upvotes >= APPROVAL_THRESHOLD:
        db.execute(
            text("""
            UPDATE salary.salary_submissions
            SET status = 'APPROVED'
            WHERE id = :submission_id
            """),
            {"submission_id": submission_id}
        )
        db.commit()

    return {"message": "Vote recorded"}
# from sqlalchemy.orm import Session
# from app.models.vote import Vote
# from sqlalchemy import func, text

# APPROVAL_THRESHOLD = 3

# def create_vote(db: Session, submission_id: int, user_id: int, vote_type: str):
#     user_id = int(user_id)

#     # Prevent duplicate vote
#     existing = db.query(Vote).filter(
#         Vote.salary_submission_id == submission_id,
#         Vote.user_id == user_id
#     ).first()

#     if existing:
#         return {"error": "User already voted"}

#     vote = Vote(
#         salary_submission_id=submission_id,
#         user_id=user_id,
#         vote_type=vote_type
#     )

#     db.add(vote)
#     db.commit()

#     # Count UP votes
#     upvotes = db.query(func.count(Vote.id)).filter(
#         Vote.salary_submission_id == submission_id,
#         Vote.vote_type == "UP"
#     ).scalar()

#     # If threshold reached → mark APPROVED
#     if upvotes >= APPROVAL_THRESHOLD:
#         db.execute(
#             text("""
#             UPDATE salary.salary_submissions
#             SET status = 'APPROVED'
#             WHERE id = :submission_id
#             """),
#             {"submission_id": submission_id}
#         )
#         db.commit()

#     return {"message": "Vote recorded"}
# # from sqlalchemy.orm import Session
# # from app.models.vote import Vote
# # from sqlalchemy import func, text

# # APPROVAL_THRESHOLD = 3

# # def create_vote(db: Session, submission_id: int, user_id: int, vote_type: str):

# #     # Prevent duplicate vote
# #     existing = db.query(Vote).filter(
# #         Vote.submission_id == submission_id,
# #         Vote.user_id == user_id
# #     ).first()

# #     if existing:
# #         return {"error": "User already voted"}

# #     vote = Vote(
# #         submission_id=submission_id,
# #         user_id=user_id,
# #         vote_type=vote_type
# #     )

# #     db.add(vote)
# #     db.commit()

# #     # Count UP votes
# #     upvotes = db.query(func.count(Vote.id)).filter(
# #         Vote.submission_id == submission_id,
# #         Vote.vote_type == "UP"
# #     ).scalar()

# #     # If threshold reached → mark APPROVED
# #     if upvotes >= APPROVAL_THRESHOLD:
# #         db.execute(
# #             text("""
# #             UPDATE salary.submissions
# #             SET status = 'APPROVED'
# #             WHERE id = :submission_id
# #             """),
# #             {"submission_id": submission_id}
# #         )
# #         db.commit()

# #     return {"message": "Vote recorded"}