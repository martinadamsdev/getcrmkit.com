from app.domain.customer.exceptions import (
    DataJobNotFoundError,
    DuplicateViewNameError,
    InvalidImportFileError,
    SavedViewNotFoundError,
)


class TestNewExceptions:
    def test_saved_view_not_found(self):
        e = SavedViewNotFoundError("abc-123")
        assert e.code == "SAVED_VIEW_NOT_FOUND"
        assert "abc-123" in e.message

    def test_duplicate_view_name(self):
        e = DuplicateViewNameError("My View")
        assert e.code == "DUPLICATE_VIEW_NAME"
        assert "My View" in e.message

    def test_data_job_not_found(self):
        e = DataJobNotFoundError("job-456")
        assert e.code == "DATA_JOB_NOT_FOUND"
        assert "job-456" in e.message

    def test_invalid_import_file(self):
        e = InvalidImportFileError("bad.txt")
        assert e.code == "INVALID_IMPORT_FILE"
        assert "bad.txt" in e.message
