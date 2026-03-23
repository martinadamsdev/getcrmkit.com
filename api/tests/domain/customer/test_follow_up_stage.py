from app.domain.customer.enums import FollowUpStage


class TestFollowUpStage:
    def test_all_seven_values(self):
        values = list(FollowUpStage)
        assert len(values) == 7

    def test_values_match_strings(self):
        assert FollowUpStage.NEW == "new"
        assert FollowUpStage.CONTACTED == "contacted"
        assert FollowUpStage.QUOTED == "quoted"
        assert FollowUpStage.SAMPLE_SENT == "sample_sent"
        assert FollowUpStage.NEGOTIATING == "negotiating"
        assert FollowUpStage.ORDERED == "ordered"
        assert FollowUpStage.LOST == "lost"
