from fastapi import APIRouter, HTTPException, status
import uuid

from app.routes.schemas import IssueCreate, IssueOut, IssueUpdate
from app.routes.storage import load_data, save_data


router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

@router.get("/", response_model=list[IssueOut], status_code=status.HTTP_200_OK)
def get_issues():
    '''Get all issues from the database.'''
    issues=load_data()
    return issues

@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(issue: IssueCreate):
    issues = load_data()
    new_issue = issue.model_dump()
    new_issue["id"] = str(uuid.uuid4())
    issues.append(new_issue)
    save_data(issues) # this basically write data to the dataBase
    return new_issue

@router.get("/{issue_id}", response_model=IssueOut, status_code=status.HTTP_200_OK)
def get_issue(issue_id: uuid.UUID):
    issues = load_data()
    for issue in issues:
        if issue["id"] == str(issue_id):
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.put("/{issue_id}", response_model=IssueOut, status_code=status.HTTP_200_OK)
def update_issue(issue_id: uuid.UUID, updated_issue: IssueUpdate):
    issues = load_data()
    for index, issue in enumerate(issues):
        if issue["id"] == str(issue_id):
            updated_issue_data = updated_issue.model_dump(
                exclude_unset=True,
                exclude_none=True,
            )
            issue.update(updated_issue_data)
            issues[index] = issue
            save_data(issues)
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")    

@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: uuid.UUID):
    issues = load_data()
    for index, issue in enumerate(issues):
        if issue["id"] == str(issue_id):
            del issues[index]
            save_data(issues)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")