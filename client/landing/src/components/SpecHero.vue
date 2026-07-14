<script setup lang="ts">
import { computed } from 'vue'
import FlaskGauge from './FlaskGauge.vue'

const today = computed(() => {
  const d = new Date()
  const p = (n: number) => String(n).padStart(2, '0')
  return `${p(d.getDate())}.${p(d.getMonth() + 1)}.${d.getFullYear()}`
})

const flasks = [
  { label: 'Белки', unit: 'г', color: 'var(--blue)' },
  { label: 'Жиры', unit: 'г', color: 'var(--yellow)' },
  { label: 'Углеводы', unit: 'г', color: 'var(--green)' },
  { label: 'Калории', unit: 'ккал', color: 'var(--mauve)' },
]
</script>

<template>
  <section id="top" class="hero">
    <div class="shell">
      <div class="sheet">
        <b class="crop crop--tl" aria-hidden="true"></b>
        <b class="crop crop--tr" aria-hidden="true"></b>
        <b class="crop crop--bl" aria-hidden="true"></b>
        <b class="crop crop--br" aria-hidden="true"></b>

        <div class="sheet__head">
          <span>EATLOG™</span>
          <span>СПЕЦИФИКАЦИЯ&nbsp;ПИТАНИЯ</span>
          <span>ФОРМА&nbsp;№&nbsp;КБЖУ-04</span>
          <span class="sheet__date">{{ today }}</span>
        </div>

        <div class="grid">
          <div class="left">
            <p class="eyebrow" data-reveal>
              <span class="pulse" aria-hidden="true"></span> дневник питания
            </p>

            <h1 class="title">
              <span data-reveal>СЧИТАЙ</span>
              <span class="title__hl" data-reveal="80">
                КБЖУ<em aria-hidden="true">/</em>
              </span>
              <span data-reveal="140">БЕЗ&nbsp;ДУХОТЫ</span>
            </h1>

            <p class="lede">
              Записал приём пищи — увидел белки, жиры, углеводы и калории.
              EatLog держит твою дневную норму на виду, пока ты ешь.
              Никаких таблиц в голове.
            </p>

            <div class="cta-row">
              <a
                class="btn btn--go"
                href="https://github.com/Nickolashaa/EatLog/releases/latest"
                target="_blank"
                rel="noopener"
                data-magnet
              >
                Скачать десктоп
                <span class="btn__arr" aria-hidden="true">→</span>
              </a>
              <a class="btn btn--ghost" href="#protocol" data-magnet>
                Как это работает
              </a>
            </div>

            <ul class="stats" aria-label="Факты">
              <li data-reveal>
                <b>4</b><span>метрики<br />в реальном времени</span>
              </li>
              <li data-reveal="90">
                <b>1</b><span>тап<br />= один приём пищи</span>
              </li>
              <li data-reveal="180">
                <b>2</b><span>платформы<br />один аккаунт</span>
              </li>
            </ul>
          </div>

          <div class="lab">
            <div class="lab__bar">
              <span>ЕЖЕДНЕВНЫЙ&nbsp;ОТЧЁТ</span>
              <span class="lab__live"><i></i>LIVE</span>
            </div>
            <div class="lab__flasks">
              <FlaskGauge
                v-for="(f, i) in flasks"
                :key="f.label"
                :label="f.label"
                :unit="f.unit"
                :color="f.color"
                :index="i"
              />
            </div>
            <p class="lab__hint">↑ КЛИКНИ ПО ШКАЛЕ</p>
          </div>
        </div>

        <div class="sheet__foot">
          <span>РЕЖИМ&nbsp;·&nbsp;ДНЕВНИК</span>
          <span class="sheet__status"><i></i>НОРМА&nbsp;ДНЯ&nbsp;НА&nbsp;ВИДУ</span>
          <span>КБЖУ&nbsp;·&nbsp;БЕЗ&nbsp;ДУХОТЫ</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding: 30px 0 20px;
}

.sheet {
  position: relative;
  border: var(--edge) solid var(--text);
  background: color-mix(in srgb, var(--bg-2) 88%, transparent);
  box-shadow: 12px 12px 0 var(--ink);
  padding: clamp(18px, 3vw, 34px);
}

.crop {
  position: absolute;
  width: 16px;
  height: 16px;
  z-index: 2;
}
.crop::before,
.crop::after {
  content: '';
  position: absolute;
  background: var(--mauve);
}
.crop::before {
  width: 16px;
  height: 2px;
  top: 7px;
}
.crop::after {
  width: 2px;
  height: 16px;
  left: 7px;
}
.crop--tl {
  top: -9px;
  left: -9px;
}
.crop--tr {
  top: -9px;
  right: -9px;
}
.crop--bl {
  bottom: -9px;
  left: -9px;
}
.crop--br {
  bottom: -9px;
  right: -9px;
}

.sheet__head,
.sheet__foot {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 18px;
  font-family: var(--mono);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--dim);
}
.sheet__head {
  border-bottom: 2px dashed var(--border);
  padding-bottom: 12px;
  margin-bottom: clamp(20px, 3vw, 34px);
}
.sheet__foot {
  border-top: 2px dashed var(--border);
  padding-top: 12px;
  margin-top: clamp(20px, 3vw, 30px);
  align-items: center;
}
.sheet__date {
  margin-left: auto;
  color: var(--mauve);
}
.sheet__status {
  margin-left: auto;
  color: var(--green);
  display: inline-flex;
  align-items: center;
  gap: 7px;
}
.sheet__status i,
.lab__live i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 0 0 currentColor;
  animation: ping 1.8s ease-out infinite;
}
@keyframes ping {
  0% {
    box-shadow: 0 0 0 0 color-mix(in srgb, currentColor 70%, transparent);
  }
  70%,
  100% {
    box-shadow: 0 0 0 7px transparent;
  }
}

.grid {
  display: grid;
  grid-template-columns: 0.82fr 1.18fr;
  gap: clamp(22px, 3.4vw, 46px);
  align-items: start;
}

.pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--crust);
  animation: blink 1.2s steps(1) infinite;
}
@keyframes blink {
  50% {
    opacity: 0.2;
  }
}

.title {
  font-family: var(--disp);
  font-weight: 900;
  font-size: clamp(44px, 8.4vw, 104px);
  line-height: 0.86;
  letter-spacing: -0.035em;
  margin: 18px 0 20px;
  text-transform: uppercase;
}
.title span {
  display: block;
}
.title__hl {
  color: var(--crust);
  background: var(--mauve);
  width: fit-content;
  padding: 0 0.12em 0.04em;
  box-shadow: 8px 8px 0 var(--ink);
  transform: rotate(-1.4deg);
  margin: 0.06em 0;
}
.title__hl em {
  color: var(--blue);
  font-style: normal;
}

.lede {
  max-width: 46ch;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.65;
}

.cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 26px 0 30px;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--mono);
  font-weight: 800;
  font-size: 14px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 14px 20px;
  border: var(--edge) solid var(--ink);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.btn--go {
  color: var(--crust);
  background: var(--mauve);
  box-shadow: 6px 6px 0 var(--ink);
}
.btn--ghost {
  color: var(--text);
  background: var(--bg-3);
  border-color: var(--text);
  box-shadow: 6px 6px 0 var(--border);
}
.btn:hover {
  transform: translate(-2px, -2px);
}
.btn--go:hover {
  box-shadow: 9px 9px 0 var(--ink);
}
.btn--ghost:hover {
  box-shadow: 9px 9px 0 var(--border);
}
.btn:active {
  transform: translate(3px, 3px);
  box-shadow: 0 0 0 var(--ink) !important;
}
.btn__arr {
  transition: transform 0.16s ease;
}
.btn--go:hover .btn__arr {
  transform: translateX(4px);
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 26px;
  list-style: none;
  border-top: 2px solid var(--border);
  padding-top: 18px;
}
.stats li {
  display: flex;
  align-items: center;
  gap: 12px;
}
.stats b {
  font-family: var(--disp);
  font-weight: 900;
  font-size: 34px;
  line-height: 1;
  color: var(--text);
}
.stats span {
  font-family: var(--mono);
  font-size: 11px;
  line-height: 1.35;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--dim);
}

.lab {
  border: var(--edge) solid var(--text);
  background: var(--bg-2);
  box-shadow: 8px 8px 0 var(--mauve);
}
.lab__bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 11px 14px;
  border-bottom: var(--edge) solid var(--text);
  background: var(--bg-3);
  font-family: var(--mono);
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--muted);
}
.lab__live {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: var(--pink);
}
.lab__flasks {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: clamp(14px, 2vw, 22px);
  padding: clamp(16px, 2vw, 22px);
}
.lab__hint {
  border-top: 2px dashed var(--border);
  padding: 10px 14px;
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--dim);
}

@media (max-width: 940px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 560px) {
  .lab__flasks {
    grid-template-columns: repeat(2, 1fr);
  }
  .sheet__date,
  .sheet__status {
    margin-left: 0;
  }
}
</style>
