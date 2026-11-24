# Контракт передачи готовых ассетов
Версия 1.0. Владелец + внешний ИИ готовят и утверждают материалы; coding-агент принимает, проверяет и интегрирует. Предложенные технические параметры согласовать на этапе 0 до массового изготовления; изменения фиксировать в DECISIONS.md. При получении уже готового комплекта сначала проверить совместимость; адаптировать импорт без изменения игровых коллизий.

## Папка поставки
Передать архив или локальную папку `asset-delivery/` (gitignored). Не копировать её целиком в public/dist. Исходные фото остаются у владельца в private-input/. Только одобренные runtime-файлы поступают в согласованное хранилище сборки. Публичный git не предназначен для личных материалов, включая производные узнаваемые изображения и тексты.

```text
asset-delivery/
  manifest.json
  graphics/
    characters/bride/
    characters/groom/
    pets/cat_1/
    pets/cat_2/
    pets/bulldog/
    enemies/
    npc/
    environments/hall/
    environments/outdoor/
    environments/cloakroom/
    items/
    vfx/
    ui/
    cutscenes/
  audio/music/
  audio/sfx/
  personal/memories/
  personal/finale/
  previews/
  licenses/
```
Относительные пути ASCII lower_snake_case; точные пути определяет manifest. Никаких абсолютных путей, symlink или выхода за корень пакета. Preview и документы лицензий не runtime. При передаче партиями указывать версию, включённые/отсутствующие ID, изменения.

## Графика
| Тип | Формат и контракт |
|---|---|
| Герои | PNG RGBA, кадры или atlas PNG+JSON, baseline 64×64, рост около 48 px |
| Питомцы | PNG RGBA, коты 20–28 px, бульдог 28–36 px; одинаковые клетки внутри серии |
| NPC | PNG RGBA, согласованный масштаб, фиксированная точка ног |
| Тайлы | PNG, 16×16, согласованные края; коллизии задаёт разработчик |
| Фоны | PNG/WebP, отдельные слои без персонажей, текста и UI; бесшовные если повторяемые |
| Props, VFX, предметы, UI | PNG RGBA, отдельные ресурсы |
| Фото | Одобренный JPEG/WebP без EXIF/GPS |

Viewport 640×360, nearest-neighbor для pixel art. Ориентация вправо; отдельные левые кадры для асимметричных черт при необходимости. Настоящий alpha, не нарисованный клетчатый фон. Постоянная точка ног, одинаковые пропорции и свет; для trimmed atlas сохранить original size и offset. Рекомендуемый padding/extrusion 1–2 px. Для каждой серии — имена кадров, fps, порядок, loop. GIF не единственный runtime-источник. Разработчик определяет физическое тело, hitbox и активные окна навыков отдельно.

## Обязательные ID
- Герои bride/groom: idle (4), run (6), jump (2), fall (2), attack (5), skill (6), hurt (2).
- Питомцы cat_1/cat_2/bulldog: idle (4), follow (6), jump (2), ability (4), celebration (3).
- Три NPC: idle (3), walk (4), telegraph (3), attack (4), recover (2), defeated (3). ID архетипов согласовать на этапе 0.
- Музыка: music_intro, music_bride, music_groom, music_mystery, music_finale. Минимум три различных трека: intro, adventure (может использоваться в трёх главах), finale. Все логические ID должны разрешаться.
- SFX (namespace sfx/): jump, land, attack_bride, attack_groom, hit, hurt, pickup, checkpoint, door, bouquet_return, dash, cat_1, cat_2, bulldog, ring_reveal, ui_confirm, ui_cancel.
- Остальные ID окружения, предметов, эффектов и UI согласовать по полной ведомости ASSET_PRODUCTION.md. Число кадров — ориентир; сокращение или alias анимации согласовать, обязательные состояния не пропускать.

## Аудио
WAV PCM 44.1/48 kHz 16/24 bit или качественный оригинал, желательно Ogg/MP3 для браузера. Отдельный файл на эффект/трек, без clipping; длительность и режим loop/one-shot. Вступление 45–90 с, главы 60–120 с, финал 60–180 с. Loop points в секундах относительно декодированного файла, учитывать encoder padding. Авторство, источник, лицензия/разрешение, атрибуция и ограничения обязательны. Подписка на стриминг не даёт автоматически права на использование в игре.

## Manifest (пример, не реальные файлы)
UTF-8 JSON. ID глобально уникален, пути относительны пакету. Для atlas frames — имена кадров; для отдельных PNG frames — относительные пути в порядке проигрывания, path — первый файл. anchor нормализован относительно необрезанного кадра. Для обычных изображений width/height; для звука durationSeconds/loop; для SFX loop=false. Права и approval в примере условны, не доказательство лицензии. Одинаковый файл может обслуживать несколько логических ID. Желательны SHA-256 и версия каждого файла.
```json
{
  "schemaVersion": 1,
  "packageVersion": "1.0.0",
  "assets": [
    {
      "id": "bride/idle",
      "kind": "animation",
      "path": "graphics/characters/bride/atlas.png",
      "atlas": "graphics/characters/bride/atlas.json",
      "frames": ["bride/idle/00", "bride/idle/01", "bride/idle/02", "bride/idle/03"],
      "frameSize": [64, 64],
      "anchor": [0.5, 0.875],
      "fps": 8,
      "loop": true,
      "version": "1.0.0",
      "status": "approved",
      "rights": {"source": "owner_supplied", "approval": "owner_confirmed", "license": "recorded_in_licenses", "private": true}
    },
    {
      "id": "music_bride",
      "kind": "music",
      "path": "audio/music/bride.ogg",
      "durationSeconds": 90,
      "loop": true,
      "loopStartSeconds": 0,
      "loopEndSeconds": 90,
      "version": "1.0.0",
      "status": "approved",
      "rights": {"source": "owner_supplied", "approval": "owner_confirmed", "license": "recorded_in_licenses", "private": false}
    }
  ],
  "missing": []
}
```

## Приёмка разработчиком
1. Проверить схему, уникальность ID, безопасные пути, наличие файлов, размеры, alpha, atlas bounds, кадры, anchor, fps, loop bounds, права и одобрение. Существование файла не доказывает качество или лицензию.
2. Сопоставить stable ID с AssetRegistry, анимациями и аудио. Разрешены только детерминированные технические операции: упаковка готовых кадров, настройка anchor/масштаба, конвертация/оптимизация без художественной правки.
3. Проверить спрайты в движении, фон и тайлы, звук после жеста, петли и мобильную читаемость в браузере.
4. Недостающие/дефектные ID, формат, причину и блокируемый gate записать в ASSET_MANIFEST.md и передать владельцу. Продолжить независимую механику на геометрических заглушках и тишине. Не генерировать, не скачивать и не дорисовывать замену.
5. Dev допускает обозначенные заглушки; production validation отвергает их и пропуски P0. Все обязательные ресурсы проверены, одобрены, интегрированы; приватные файлы не попадают в открытый доступ.
