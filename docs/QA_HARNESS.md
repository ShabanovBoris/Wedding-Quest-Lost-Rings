# Контракт автоматического прогона уровня (`qa:capture`)

Версия 1.0. Обязателен с этапа 2 (вертикальный срез): без него QA Gate в Kent не запускается для задач уровней. Детерминированно прогоняет один уровень в headless-браузере и оставляет кадры ключевых моментов, видео и метрики. Не заменяет прохождение обычным вводом и QA19 (владелец или тестер).

## Команда

`npm run qa:capture -- --level <levelId> --out <dir> [--profile desktop|touch] [--browser chromium|webkit]`

- Запускается из корня репозитория; `<dir>` — относительный путь для результатов, создаётся при необходимости.
- Сам поднимает сервер на свободном порте и останавливает его при завершении, включая падение: параллельные прогоны в разных worktree не мешают друг другу.
- Работает только с тестовым режимом сборки: QA-хуки и быстрые переходы доступны в нём и не попадают в production (GAME_SPEC §11).
- Код выхода 0 — прогон завершён, метрики в бюджете; 1 — падение, ошибка или превышение бюджета. Диагностика — в stdout/stderr.

## Прогон

1. Открывает `?level=<levelId>&qa=1` во viewport 1280×720 (`desktop`) или в эмуляции landscape touch (`touch`), ждёт готовности игры.
2. Для каждого beat из `qa.beats` данных уровня: переводит игру в точку входа beat (старт уровня с нужного spawn или checkpoint — «быстрый переход» по GAME_SPEC §11), подаёт реальный ввод (`inputs`, удержание `holdMs`), ждёт `settleMs`, делает снимок. Один beat — один кадр.
3. Пишет видео всего прогона и собирает метрики после загрузки.

## `qa.beats` в данных уровня

```json
"qa": {
  "beats": [
    { "id": "start", "at": { "checkpoint": "cp_hall_start" }, "settleMs": 600, "expect": "Стартовая площадка, выход виден справа" },
    { "id": "first_jump", "at": { "checkpoint": "cp_hall_start" }, "inputs": [{ "action": "right", "holdMs": 900 }, { "action": "jump", "holdMs": 200 }], "expect": "Прыжок через первый стол" }
  ]
}
```

- `id` — уникален внутри уровня, `[a-z0-9_]`. `at` — точка входа: spawn или checkpoint из данных уровня. `inputs` — последовательность InputAction из GAME_SPEC §4. `settleMs` — пауза перед снимком, по умолчанию 500. `expect` — что должно быть видно на кадре.
- Beat — это момент для глаз (зона, обучение, бой, чекпоинт, секрет, финальный вызов), а не доказательство проходимости маршрута.

## Результаты в `<dir>`

| Файл | Содержимое |
| --- | --- |
| `frames/NN-<beatId>.png` | Снимок каждого beat в порядке `qa.beats` |
| `run.webm` | Видео прогона |
| `metrics.json` | Метрики и вердикт по схеме ниже |
| `report.md` | Вердикт, нарушения, метрики, ссылки на кадры |

## `metrics.json`

```json
{
  "schemaVersion": 1,
  "levelId": "hall",
  "profile": "desktop",
  "browser": "chromium",
  "viewport": { "width": 1280, "height": 720 },
  "beats": [{ "id": "start", "file": "frames/01-start.png", "ok": true }],
  "frameMs": { "p50": 8.2, "p95": 12.4, "p99": 16.1, "max": 21.0, "samples": 1800 },
  "longTasks": 0,
  "inputLatencyFrames": { "p50": 1, "max": 2, "samples": 12 },
  "consoleErrors": 0,
  "pageErrors": 0,
  "failedRequests": 0,
  "softlock": false,
  "violations": [],
  "verdict": "pass"
}
```

- `frameMs` — интервалы requestAnimationFrame после загрузки. `longTasks` — задачи основного потока дольше 50 мс.
- `inputLatencyFrames` — кадров между поданным InputAction и первым изменением состояния игры по `window.__GAME_TEST__` (позиция, скорость, состояние, анимация, эффект).
- `softlock` — игра не реагирует на ввод или игровое время не идёт.

## Бюджеты headless-прогона

| Метрика | Бюджет |
| --- | --- |
| `frameMs.p95` | ≤ 20 мс |
| `frameMs.max` после загрузки | ≤ 250 мс |
| `longTasks` | 0 |
| `inputLatencyFrames.max` | ≤ 3 |
| `consoleErrors`, `pageErrors`, `failedRequests` | 0 |
| `softlock` | false |
| Снято beat | все из `qa.beats` |

Нарушение любого пункта даёт `verdict: "fail"` и строку в `violations`. Числа headless-прогона — регрессионный сигнал, а не замер устройства: цель 60 FPS на ноутбуке и устойчивые 30+ на смартфоне проверяется на реальных устройствах (GAME_SPEC §9.2, QA14).
