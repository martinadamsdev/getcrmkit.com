import uuid

from app.domain.customer.entities import Contact


class TestContact:
    def test_create_with_customer_id(self):
        customer_id = uuid.uuid7()
        contact = Contact(customer_id=customer_id, name="John Doe")
        assert contact.customer_id == customer_id
        assert contact.name == "John Doe"

    def test_is_primary_default_false(self):
        contact = Contact(customer_id=uuid.uuid7(), name="Jane")
        assert contact.is_primary is False

    def test_custom_fields_default_empty_dict(self):
        contact = Contact(customer_id=uuid.uuid7(), name="Bob")
        assert contact.custom_fields == {}

    def test_all_contact_channels_optional(self):
        contact = Contact(customer_id=uuid.uuid7(), name="Alice")
        assert contact.email is None
        assert contact.phone is None
        assert contact.whatsapp is None
        assert contact.skype is None
        assert contact.linkedin is None
        assert contact.wechat is None
        assert contact.title is None
        assert contact.notes is None
