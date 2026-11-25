const ashesArtifacts = {"kubejs:field_kit": "kit/field_kit", "kubejs:scout_report": "kit/scout_report", "kubejs:ward_charm": "kit/ward_charm", "kubejs:hunter_medal": "kit/hunter_medal", "kubejs:living_heart": "kit/living_heart", "kubejs:abyssal_seal": "kit/abyssal_seal", "kubejs:power_regulator": "kit/power_regulator", "kubejs:source_capacitor": "kit/source_capacitor", "kubejs:expedition_seal": "skills/menu", "kubejs:logistics_badge": "kit/logistics", "kubejs:final_testament": "kit/testament", "kubejs:purity_sigil": "purify", "kubejs:cleansing_charge": "cleanse"}
Object.keys(ashesArtifacts).forEach(id => {
  ItemEvents.rightClicked(id, event => {
    event.cancel()
    const user = event.player.getUUID().toString()
    event.server.runCommandSilent('execute as ' + user + ' at @s run function ashes:' + ashesArtifacts[id])
  })
})

ItemEvents.rightClicked('kubejs:repair_kit', event => {
  event.cancel()
  const tool = event.player.getOffhandItem()
  if (!tool.isDamageableItem() || tool.getDamageValue() <= 0) {
    event.player.tell('Возьми повреждённый инструмент или предмет брони во вторую руку.')
    return
  }
  const repaired = Math.max(1, Math.floor(tool.getMaxDamage() / 4))
  tool.setDamageValue(Math.max(0, tool.getDamageValue() - repaired))
  if (!event.player.isCreative()) event.item.shrink(1)
  event.player.tell('Ремонтный комплект восстановил прочность.')
})
