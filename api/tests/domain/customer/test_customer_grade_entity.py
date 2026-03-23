import uuid

from app.domain.customer.entities import CustomerGrade


class TestCustomerGrade:
    def test_create_with_defaults(self):
        grade = CustomerGrade(name="A")
        assert grade.color == "#3B82F6"
        assert grade.position == 0
        assert grade.label is None

    def test_create_with_custom_values(self):
        grade = CustomerGrade(name="S", label="超级VIP", color="#FF0000", position=-1)
        assert grade.name == "S"
        assert grade.label == "超级VIP"
        assert grade.color == "#FF0000"
        assert grade.position == -1

    def test_inherits_base_entity(self):
        grade = CustomerGrade(name="A")
        assert hasattr(grade, "id")
        assert hasattr(grade, "tenant_id")
        assert hasattr(grade, "created_at")
        assert hasattr(grade, "updated_at")
        assert isinstance(grade.id, uuid.UUID)
