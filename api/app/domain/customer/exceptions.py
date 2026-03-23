from app.domain.shared.exceptions import DomainError


class CustomerNameRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__(message="Customer name is required", code="CUSTOMER_NAME_REQUIRED")


class CustomerNotFoundError(DomainError):
    def __init__(self, customer_id: str) -> None:
        super().__init__(message=f"Customer not found: {customer_id}", code="CUSTOMER_NOT_FOUND")


class ContactNotFoundError(DomainError):
    def __init__(self, contact_id: str) -> None:
        super().__init__(message=f"Contact not found: {contact_id}", code="CONTACT_NOT_FOUND")


class TagNotFoundError(DomainError):
    def __init__(self, tag_id: str) -> None:
        super().__init__(message=f"Tag not found: {tag_id}", code="TAG_NOT_FOUND")


class CustomerGradeNotFoundError(DomainError):
    def __init__(self, grade_id: str) -> None:
        super().__init__(message=f"Customer grade not found: {grade_id}", code="CUSTOMER_GRADE_NOT_FOUND")


class DuplicateTagError(DomainError):
    def __init__(self, name: str, group_name: str | None) -> None:
        super().__init__(message=f"Tag already exists: {name} in group {group_name}", code="DUPLICATE_TAG")


class GradeInUseError(DomainError):
    def __init__(self, grade_id: str) -> None:
        super().__init__(message=f"Grade is in use by customers: {grade_id}", code="GRADE_IN_USE")


class SavedViewNotFoundError(DomainError):
    def __init__(self, view_id: str) -> None:
        super().__init__(message=f"Saved view not found: {view_id}", code="SAVED_VIEW_NOT_FOUND")


class DuplicateViewNameError(DomainError):
    def __init__(self, name: str) -> None:
        super().__init__(message=f"Saved view name already exists: {name}", code="DUPLICATE_VIEW_NAME")


class DataJobNotFoundError(DomainError):
    def __init__(self, job_id: str) -> None:
        super().__init__(message=f"Data job not found: {job_id}", code="DATA_JOB_NOT_FOUND")


class InvalidImportFileError(DomainError):
    def __init__(self, file_name: str) -> None:
        super().__init__(message=f"Invalid import file: {file_name}", code="INVALID_IMPORT_FILE")
