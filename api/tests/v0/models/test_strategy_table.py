from src.v0.models.strategy_table import Strategy, StrategyTableData


def test_Strategy():
    strategy = Strategy(name="junk")
    assert strategy.path is None


def test_StrategyTableData():
    strategies = StrategyTableData(
        table=[Strategy(name="first"), Strategy(name="second"), Strategy(name="third")]
    )
    assert strategies.table[0].name == "first"
