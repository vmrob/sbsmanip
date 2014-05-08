import sbsmanip.io
import sbsmanip.sector
import sbsmanip.modifier


def test_scale():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    sector = savefile.sector

    mod = sbsmanip.modifier.Scale(sector, 10)

    prepared = mod.prepare()

    assert len(prepared) == 102

    e1 = next(e for e in savefile.sector.entities()
              if e.id == '1066294968834912967')
    e2 = next(e for e in savefile.sector.entities()
              if e.id == '-2200846055786792018')

    assert e1.id == '1066294968834912967'
    assert e2.id == '-2200846055786792018'

    assert e1.position.x == -1118.05237
    assert e1.position.y == 6167.3833
    assert e1.position.z == 6817.74072

    assert e2.position.x == -5282.06836
    assert e2.position.y == -1049.00464
    assert e2.position.z == 1908.99719

    mod.execute(prepared)

    assert e1.position.x == -11180.5237
    assert e1.position.y == 61673.833
    assert e1.position.z == 68177.4072

    assert e2.position.x == -52820.6836
    assert e2.position.y == -10490.0464
    assert e2.position.z == 19089.9719


def test_remove_far():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    sector = savefile.sector

    mod = sbsmanip.modifier.RemoveFar(sector, 50000)
    prepared = mod.prepare()

    assert len(prepared) == 1
    assert sector.entity_count() == 102
    mod.execute(prepared)
    assert sector.entity_count() == 101

    mod = sbsmanip.modifier.RemoveFar(sector, 1)
    prepared = mod.prepare()

    assert len(prepared) == 101
    mod.execute(prepared)
    assert sector.entity_count() == 0


def test_remove_debris():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    sector = savefile.sector

    mod = sbsmanip.modifier.RemoveSize(sector, 0, 6)
    prepared = mod.prepare()

    assert len(prepared) == 1
    assert sector.entity_count() == 102

    mod.execute(prepared)

    assert sector.entity_count() == 101

    mod = sbsmanip.modifier.RemoveSize(sector, 0, 10000)
    prepared = mod.prepare()

    assert len(prepared) == 19
    mod.execute(prepared)
    assert sector.entity_count() == 82


def test_remove_ship():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    target_file = sbsmanip.io.XMLFile('tests/support/RespawnShip.sbc')
    target = sbsmanip.sector.CubeGridEntity(target_file.root)

    sector = savefile.sector

    mod = sbsmanip.modifier.RemoveShip(sector, target)
    prepared = mod.prepare()

    assert len(prepared) == 10
    assert sector.entity_count() == 102

    mod.execute(prepared)

    assert sector.entity_count() == 92

    mod = sbsmanip.modifier.RemoveShip(sector, target)
    prepared = mod.prepare()

    assert len(prepared) == 0
