from model.block import Block
import model.block as block


def test_initialize_block():
    my_block = Block()


def test_grass_block():
    my_block = block.GRASS
    assert 'grass' == my_block.madeof
    assert 2 == my_block.type_num


def test_stone_block():
    my_block = block.STONE
    assert 'stone' == my_block.madeof
    assert 1 == my_block.type_num
