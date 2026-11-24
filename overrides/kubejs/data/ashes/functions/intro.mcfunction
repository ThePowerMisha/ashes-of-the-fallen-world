tag @s add ashes_intro
tellraw @s {"text": "Пепел ушедшего мира. Выбери специализацию: /trigger ashes_class set 1–6", "color": "gold"}
tellraw @s {"text": "1 Паладин | 2 Архимаг | 3 Инженер | 4 Следопыт | 5 Архитектор | 6 Оккультист", "color": "gold"}
tellraw @s {"text": "Открой книгу FTB Quests. /trigger ashes_status — прогресс; /trigger ashes_purify — знак очищения.", "color": "gold"}
tellraw @s {"text": "Навыки: /trigger ashes_talent set 1 (ранг II) или 2 (ранг III); /trigger ashes_ability — применить. /trigger ashes_cleanse — сбор образца.", "color": "gold"}
tellraw @s [{"text": "[Открыть меню классов]", "color": "gold", "bold": true, "clickEvent": {"action": "run_command", "value": "/trigger ashes_menu"}, "hoverEvent": {"action": "show_text", "contents": {"text": "Выбор класса, таланта, статус"}}}]
tellraw @s {"text": "[Хроники] Хроники мира: /trigger ashes_news set 2 — скрыть сообщения, set 1 — включить.", "color": "dark_aqua"}
