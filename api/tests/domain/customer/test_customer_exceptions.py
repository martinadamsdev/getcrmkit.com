from app.domain.customer.exceptions import (
    ContactNotFoundError,
    CustomerGradeNotFoundError,
    CustomerNameRequiredError,
    CustomerNotFoundError,
    DuplicateTagError,
    GradeInUseError,
    TagNotFoundError,
)


class TestCustomerExceptions:
    def test_customer_not_found_error(self):
        err = CustomerNotFoundError("abc-123")
        assert err.code == "CUSTOMER_NOT_FOUND"
        assert "abc-123" in err.message

    def test_contact_not_found_error(self):
        err = ContactNotFoundError("contact-456")
        assert err.code == "CONTACT_NOT_FOUND"
        assert "contact-456" in err.message

    def test_tag_not_found_error(self):
        err = TagNotFoundError("tag-789")
        assert err.code == "TAG_NOT_FOUND"
        assert "tag-789" in err.message

    def test_customer_grade_not_found_error(self):
        err = CustomerGradeNotFoundError("grade-000")
        assert err.code == "CUSTOMER_GRADE_NOT_FOUND"
        assert "grade-000" in err.message

    def test_duplicate_tag_error(self):
        err = DuplicateTagError("VIP", "region")
        assert err.code == "DUPLICATE_TAG"
        assert "VIP" in err.message

    def test_customer_name_required_error(self):
        err = CustomerNameRequiredError()
        assert err.code == "CUSTOMER_NAME_REQUIRED"
        assert len(err.message) > 0

    def test_grade_in_use_error(self):
        err = GradeInUseError("grade-111")
        assert err.code == "GRADE_IN_USE"
        assert "grade-111" in err.message
