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


def test_remove_all():
    savefile = sbsmanip.io.SBSFile('tests/support/SANDBOX_0_0_0_.sbs')
    sector = savefile.sector

    mod = sbsmanip.modifier.RemoveAll(sector)
    prepared = mod.prepare()

    assert len(prepared) == sector.entity_count()

    mod.execute(prepared)

    assert sector.entity_count() == 0


def test_modify_welding():
    cube_blocks_sbc = sbsmanip.io.CubeBlocksSBC('tests/support/CubeBlocks.sbc')

    mod1 = sbsmanip.modifier.ScaleAssemblyTime(
        cube_blocks_sbc.definitions, 0.1)
    mod2 = sbsmanip.modifier.ScaleDisassemblyTime(
        cube_blocks_sbc.definitions, 10)

    prepared1 = mod1.prepare()
    prepared2 = mod2.prepare()

    assert len(prepared1) == 118
    assert len(prepared2) == 118

    block = next(d for d in prepared1 if d.type_name() ==
                 'CubeBlock:LargeBlockArmorBlock')

    assert block.build_time == 8
    assert block.disassembly_ratio == 2.5

    mod1.execute(prepared1)
    mod2.execute(prepared2)

    assert block.build_time == 0.8
    assert block.disassembly_ratio == 25