"""Generate item interactions from the same table used for the in-game tooltips."""
import json

CONSUMABLES = {
    'field_kit': ('Полевой комплект', 'Насыщение и регенерация на ходу.',
                  [('saturation', 1, 1), ('regeneration', 8, 0)]),
    'scout_report': ('Полевой отчёт', 'Ночное зрение на 60 секунд и скорость на 20 секунд.',
                     [('night_vision', 60, 0), ('speed', 20, 0)]),
    'ward_charm': ('Оберег рубежа', 'Поглощение на 30 секунд и сопротивление на 12 секунд.',
                   [('absorption', 30, 0), ('resistance', 12, 0)]),
    'hunter_medal': ('Медаль охотника', 'Сила и скорость на 20 секунд.',
                     [('strength', 20, 0), ('speed', 20, 0)]),
    'living_heart': ('Живое сердце', 'Регенерация и дополнительное здоровье на короткое время.',
                     [('regeneration', 10, 0), ('absorption', 25, 1)]),
    'abyssal_seal': ('Печать бездны', 'Подводное дыхание и ночное зрение на 60 секунд.',
                     [('water_breathing', 60, 0), ('night_vision', 60, 0)]),
    'power_regulator': ('Регулятор энергии', 'Спешка II на 25 секунд для полевых работ.',
                         [('haste', 25, 1)]),
    'source_capacitor': ('Конденсатор источника', 'Огнестойкость на 45 секунд.',
                         [('fire_resistance', 45, 0)]),
}

INTERACTIONS = {
    'expedition_seal': ('skills/menu', 'ПКМ — открыть меню классов, талантов и мастерства. Печать сохраняется.'),
    'logistics_badge': ('kit/logistics', 'ПКМ — показать справку по припасам. Знак сохраняется.'),
    'final_testament': ('kit/testament', 'ПКМ — прочитать послание трёх орденов. Завещание сохраняется.'),
    'purity_sigil': ('purify', 'ПКМ — снять отрицательные эффекты с себя. Расходуется один знак.'),
    'cleansing_charge': ('cleanse', 'ПКМ, стоя на скалке, — получить образец. Один заряд на успешный ритуал.'),
}

ARTIFACT_RECIPES = {
    'foundation_recovery': ('8x minecraft:stone_bricks', ['kubejs:foundation_stone', 'minecraft:cobblestone']),
    'seal_trace': ('kubejs:scout_report', ['kubejs:archive_fragment', 'minecraft:charcoal', 'minecraft:paper']),
    'memory_chart': ('2x kubejs:scout_report', ['kubejs:memory_lens', 'minecraft:paper']),
    'core_rations': ('4x kubejs:field_kit', ['kubejs:concord_core', 'minecraft:bread', 'minecraft:golden_carrot']),
    'renewed_rations': ('8x kubejs:field_kit', ['kubejs:renewal_heart', 'minecraft:bread']),
    'renewed_wards': ('4x kubejs:ward_charm', ['kubejs:renewal_circuit', 'minecraft:prismarine_shard']),
}


def usage_tooltips():
    tooltips = {name: f'ПКМ — {info[1]} Расходуется один предмет, восстановление 30 секунд.'
                for name, info in CONSUMABLES.items()}
    tooltips.update({name: info[1] for name, info in INTERACTIONS.items()})
    tooltips['repair_kit'] = 'ПКМ — восстановить до 25% прочности предмета во второй руке. Комплект расходуется при ремонте.'
    tooltips['foundation_stone'] = 'Камень основания используется для восстановления поселений. Через верстак даёт восемь каменных кирпичей.'
    tooltips['memory_lens'] = 'Линзу можно использовать в рецепте двух полевых отчётов.'
    return tooltips


def generate_artifacts(K, F, put, fn, msg):
    handlers = {name: 'kit/' + name for name in CONSUMABLES}
    handlers.update({name: info[0] for name, info in INTERACTIONS.items()})
    encoded = json.dumps({'kubejs:'+name: target for name, target in handlers.items()}, ensure_ascii=False)
    put(K/'server_scripts'/'ashes_artifacts.js', f'''
const ashesArtifacts = {encoded}
Object.keys(ashesArtifacts).forEach(id => {{
  ItemEvents.rightClicked(id, event => {{
    event.cancel()
    const user = event.player.getUUID().toString()
    event.server.runCommandSilent('execute as ' + user + ' at @s run function ashes:' + ashesArtifacts[id])
  }})
}})

ItemEvents.rightClicked('kubejs:repair_kit', event => {{
  event.cancel()
  const tool = event.player.getOffhandItem()
  if (!tool.isDamageableItem() || tool.getDamageValue() <= 0) {{
    event.player.tell('Возьми повреждённый инструмент или предмет брони во вторую руку.')
    return
  }}
  const repaired = Math.max(1, Math.floor(tool.getMaxDamage() / 4))
  tool.setDamageValue(Math.max(0, tool.getDamageValue() - repaired))
  if (!event.player.isCreative()) event.item.shrink(1)
  event.player.tell('Ремонтный комплект восстановил прочность.')
}})
'''.lstrip())
    def append(target, lines):
        path = F/(target+'.mcfunction')
        path.write_text(path.read_text(encoding='utf-8')+'\n'.join(lines)+'\n', encoding='utf-8')
    append('load', ['scoreboard objectives add akit_cd dummy', 'scoreboard objectives add akit_used dummy'])
    append('player', ['scoreboard players add @s akit_cd 0',
                      'execute if score @s akit_cd matches 1.. run scoreboard players remove @s akit_cd 1'])
    for item, (name, _, effects) in CONSUMABLES.items():
        fn('kit/'+item, [
            'scoreboard players add @s akit_cd 0',
            'execute if score @s akit_cd matches 1.. run '+msg('Припасы восстанавливаются. Попробуй через несколько секунд.'),
            f'execute if score @s akit_cd matches 0 store result score @s akit_used run clear @s kubejs:{item} 1',
            f'execute if score @s akit_cd matches 0 if score @s akit_used matches 1 run function ashes:kit/{item}_used',
        ])
        fn('kit/'+item+'_used', [
            *[f'effect give @s minecraft:{effect} {duration} {amplifier} true'
              for effect, duration, amplifier in effects],
            'scoreboard players set @s akit_cd 30', msg(f'{name} применён. Восстановление припасов 30 секунд.'),
        ])
    fn('kit/testament', [msg('Соберите город вокруг общего огня. Оставьте второй путь к воротам и место для тех, кто вернётся позже.'), 'function ashes:skills/menu'])
    fn('kit/logistics', [msg('Полевой комплект — еда и лечение. Отчёт — свет и скорость. Оберег — защита на отходе. Ремонтный комплект работает с повреждённым предметом во второй руке.')])
