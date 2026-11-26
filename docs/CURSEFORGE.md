# Обновление сборки в CurseForge

После публикации в каталоге один раз установи «Пепел ушедшего мира» со страницы проекта. Стандартный ZIP из GitHub Actions подходит для тестирования и загрузки первого файла в кабинет автора.

## Перенос текущего профиля

1. Закрой Minecraft. В меню старого профиля CurseForge нажми **Open Folder** и скопируй папку `saves` в безопасное место.
2. Установи опубликованную сборку из каталога CurseForge. Открой папку нового профиля и скопируй туда `saves`. Для сетевых миров эта папка находится на сервере.
3. Запусти сборку и проверь мир. Для следующих версий в **My Modpacks** нажимай стрелки возле **Play** и выбирай **Update to the latest version**. Оставь **Update to a separate modpack profile** выключенным, если обновляешь существующий профиль.

Если кнопка версий скрыта, проверь **Profile Options → Allow content management**. При обновлении CurseForge может перезаписать вручную изменённые моды и настройки. Сохрани копию мира перед переходом между версиями.

## Подключение публикации в GitHub

1. В [CurseForge Author Dashboard](https://authors.curseforge.com/#/projects/create/choose-game) создай проект Minecraft с типом **Modpacks** или открой существующий. Скопируй его **Project ID**.
2. В GitHub открой **Settings → Secrets and variables → Actions**. В **Variables** создай `CURSEFORGE_PROJECT_ID`, в **Secrets** сохрани `CURSEFORGE_UPLOAD_TOKEN` из раздела API Tokens кабинета CurseForge. Токен должен принадлежать аккаунту с правом загрузки файлов в этот проект.
3. Выпусти тег с нужного коммита. Для текущей версии команды из рабочей ветки выглядят так:

   ```sh
   git tag curseforge-v1.0.0-rc5-author-content.6
   git push origin refs/tags/curseforge-v1.0.0-rc5-author-content.6
   ```

GitHub Actions соберёт оба архива и отправит стандартный ZIP в указанный проект. Версия в теге должна совпадать с `manifest.json`, а в `CHANGELOG.md` нужен раздел `### <версия>`. Кандидаты RC выходят как **Beta**. После загрузки следи за модерацией в кабинете автора. Если Actions не получил ответ и статус загрузки неизвестен, перед повторным запуском проверь список файлов проекта.

Первый ZIP также можно вручную загрузить в **Files → Upload file**. Если эта версия уже загружена вручную, начни публикацию тегами со следующей версии. Для каждого обновления используй тот же **Project ID**.

- [Как сменить версию модпака в приложении](https://support.curseforge.com/support/solutions/articles/9000206622)
- [API загрузки файлов CurseForge](https://support.curseforge.com/support/solutions/articles/9000197321)
