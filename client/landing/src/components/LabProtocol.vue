<script setup lang="ts">
const steps = [
  {
    no: '01',
    key: 'НАЙДИ',
    title: 'Ищешь блюдо',
    body: 'Поиск по базе продуктов прямо в приложении.',
    accent: 'var(--blue)',
    shadow: 'hard--blue',
  },
  {
    no: '02',
    key: 'ЗАПИШИ',
    title: 'Логируешь приём',
    body: 'Приём пищи падает в дневник с временем.',
    accent: 'var(--green)',
    shadow: 'hard--green',
  },
  {
    no: '03',
    key: 'СЛЕДИ',
    title: 'Смотришь отчёт',
    body: 'Дневная норма КБЖУ всегда перед глазами — видно, сколько осталось до цели.',
    accent: 'var(--mauve)',
    shadow: 'hard--mauve',
  },
]
</script>

<template>
  <section id="protocol" class="proto">
    <div class="shell">
      <header class="proto__head">
        <div class="section-no" data-reveal>01</div>
        <div>
          <p class="mono-tag" data-reveal>/ порядок действий</p>
          <h2 class="proto__h" data-reveal="60">ПРОТОКОЛ<br />из трёх шагов</h2>
        </div>
      </header>

      <ol class="steps">
        <li
          v-for="(s, i) in steps"
          :key="s.no"
          class="step"
          :class="s.shadow"
          :style="{ '--a': s.accent }"
          :data-reveal="i * 90"
        >
          <div class="step__top">
            <span class="step__no">{{ s.no }}</span>
            <span class="step__key">{{ s.key }}</span>
          </div>
          <h3 class="step__title">{{ s.title }}</h3>
          <p class="step__body">{{ s.body }}</p>
          <div class="step__rule" aria-hidden="true">
            <i></i><i></i><i></i><i></i><i></i>
          </div>
        </li>
      </ol>
    </div>
  </section>
</template>

<style scoped>
.proto {
  padding: clamp(60px, 9vw, 120px) 0 clamp(30px, 5vw, 60px);
}
.proto__head {
  display: flex;
  align-items: flex-end;
  gap: 22px;
  margin-bottom: clamp(30px, 5vw, 56px);
}
.proto__h {
  font-family: var(--disp);
  font-weight: 900;
  font-size: clamp(28px, 5vw, 56px);
  line-height: 0.95;
  letter-spacing: -0.03em;
  text-transform: uppercase;
}

.steps {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: clamp(16px, 2.4vw, 30px);
}
.step {
  position: relative;
  border: var(--edge) solid var(--text);
  background: var(--bg-2);
  padding: 24px 22px 20px;
  transition: transform 0.16s ease;
}
.step:nth-child(2) {
  transform: translateY(clamp(0px, 3vw, 34px));
}
.step:hover {
  transform: translateY(-6px);
}
.step:nth-child(2):hover {
  transform: translateY(clamp(-6px, 3vw - 6px, 28px));
}

.step__top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 16px;
}
.step__no {
  font-family: var(--disp);
  font-weight: 900;
  font-size: 46px;
  line-height: 1;
  color: var(--a);
  -webkit-text-stroke: 1px var(--ink);
}
.step__key {
  font-family: var(--mono);
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.24em;
  color: var(--dim);
  writing-mode: vertical-rl;
}
.step__title {
  font-family: var(--disp);
  font-weight: 800;
  font-size: 22px;
  letter-spacing: -0.01em;
  margin-bottom: 10px;
}
.step__body {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
}
.step__rule {
  display: flex;
  gap: 6px;
  margin-top: 18px;
}
.step__rule i {
  height: 6px;
  flex: 1;
  background: var(--border);
}
.step__rule i:first-child {
  background: var(--a);
}
.step:hover .step__rule i {
  background: var(--a);
  transition: background 0.2s ease;
}
.step:hover .step__rule i:nth-child(4),
.step:hover .step__rule i:nth-child(5) {
  background: var(--border);
}

@media (max-width: 860px) {
  .steps {
    grid-template-columns: 1fr;
  }
  .step:nth-child(2) {
    transform: none;
  }
  .step:nth-child(2):hover {
    transform: translateY(-6px);
  }
}
</style>
