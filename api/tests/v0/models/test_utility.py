from src.v0.models.utility import ContinuousUtilityData, DiscreteUtilityData, UtilityData


def test_DiscreteUtilityData():
    utility = DiscreteUtilityData(
        parents_uuid=["123", "124"], values=[[0, -10], [3, -5]]
    )
    assert isinstance(utility, DiscreteUtilityData)


def test_ContinuousUtilityData():
    utility = ContinuousUtilityData(parents_uuid=["123", "124"])
    assert isinstance(utility, ContinuousUtilityData)


def test_UtilityData():
    utility = UtilityData()
    assert utility.dtype is None
    assert utility.unit is None
