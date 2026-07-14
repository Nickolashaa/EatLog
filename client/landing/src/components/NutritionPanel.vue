<script setup lang="ts">
const rows = [
  { name: 'Поиск блюд', val: 'база продуктов', dv: 100, hi: true },
  { name: 'Дневник приёмов пищи', val: 'с временем', dv: 100, hi: true },
  { name: '— белки', val: 'г / норма', dv: 74 },
  { name: '— жиры', val: 'г / норма', dv: 80 },
  { name: '— углеводы', val: 'г / норма', dv: 71 },
  { name: '— калории', val: 'ккал / норма', dv: 84 },
  { name: 'Профиль и цель КБЖУ', val: 'по полу/весу/росту', dv: 100, hi: true },
  { name: 'Уведомления', val: 'приходят в telegram', dv: 100, hi: true },
]

const points = [
  { n: '01', t: 'База блюд', a: 'var(--mauve)' },
  { n: '02', t: 'Твой журнал', a: 'var(--green)' },
  { n: '03', t: 'Удобный дизайн', a: 'var(--blue)' },
]
</script>

<template>
  <section id="label" class="feat">
    <div class="shell feat__grid">
      <aside class="label" data-reveal>
        <div class="label__title">Пищевая ценность</div>
        <div class="label__sub">EATLOG · дневник питания</div>
        <div class="label__serv">
          <span>На порцию</span><b>1 приём пищи</b>
        </div>
        <div class="label__thick"></div>
        <div class="label__dv">
          <span>Функция</span><span>% дневной нормы</span>
        </div>
        <ul class="label__rows">
          <li v-for="r in rows" :key="r.name" :class="{ hi: r.hi }">
            <span class="label__name">{{ r.name }}</span>
            <span class="label__meta">{{ r.val }}</span>
            <span class="label__pct">{{ r.dv }}%</span>
            <i class="label__bar" :style="{ width: r.dv + '%' }"></i>
          </li>
        </ul>
        <div class="label__thin"></div>
        <p class="label__foot">
          * Процент показывает, насколько EatLog закрывает задачу вести КБЖУ.
          Не является медицинской рекомендацией.
        </p>
      </aside>

      <div class="cards">
        <header class="cards__head">
          <div class="section-no" data-reveal>02</div>
          <h2 class="cards__h" data-reveal="60">
            ЧТО<br />ВНУТРИ<em aria-hidden="true">.</em>
          </h2>
          <ul class="pts">
            <li
              v-for="(p, i) in points"
              :key="p.t"
              class="pt"
              :style="{ '--a': p.a }"
              :data-reveal="120 + i * 80"
            >
              <span class="pt__n">{{ p.n }}</span>
              <span class="pt__t">{{ p.t }}</span>
              <span class="pt__mark" aria-hidden="true"></span>
            </li>
          </ul>
        </header>
      </div>
    </div>
  </section>
</template>

<style scoped>
.feat {
  padding: clamp(40px, 6vw, 80px) 0;
}
.feat__grid {
  display: grid;
  grid-template-columns: 0.82fr 1.18fr;
  gap: clamp(22px, 3vw, 46px);
  align-items: start;
}

.label {
  position: sticky;
  top: 84px;
  background: var(--text);
  color: var(--crust);
  border: var(--edge) solid var(--ink);
  box-shadow: 9px 9px 0 var(--mauve);
  padding: 16px 18px 18px;
  font-family: var(--mono);
}
.label__title {
  font-family: var(--disp);
  font-weight: 900;
  font-size: clamp(26px, 3.4vw, 38px);
  line-height: 0.95;
  letter-spacing: -0.03em;
  border-bottom: 9px solid var(--crust);
  padding-bottom: 6px;
}
.label__sub {
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 6px 0;
}
.label__serv {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 13px;
  font-weight: 700;
  border-top: 1px solid var(--crust);
  padding-top: 6px;
}
.label__serv b {
  font-family: var(--disp);
  font-size: 15px;
}
.label__thick {
  height: 12px;
  background: var(--crust);
  margin: 6px 0;
}
.label__dv {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid var(--crust);
  padding-bottom: 5px;
}
.label__rows {
  list-style: none;
}
.label__rows li {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: baseline;
  column-gap: 8px;
  padding: 7px 0 8px;
  border-bottom: 1px solid color-mix(in srgb, var(--crust) 25%, transparent);
  overflow: hidden;
}
.label__name {
  font-weight: 700;
  font-size: 13.5px;
}
.label__rows li.hi .label__name {
  font-family: var(--disp);
  font-weight: 800;
}
.label__meta {
  grid-column: 1;
  font-size: 10.5px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  opacity: 0.6;
}
.label__pct {
  grid-column: 2;
  grid-row: 1 / span 2;
  align-self: center;
  font-family: var(--disp);
  font-weight: 800;
  font-size: 15px;
}
.label__bar {
  position: absolute;
  left: 0;
  bottom: 0;
  height: 2px;
  background: var(--crust);
}
.label__thin {
  height: 4px;
  background: var(--crust);
  margin: 6px 0;
}
.label__foot {
  font-size: 10px;
  line-height: 1.5;
  opacity: 0.7;
}

.cards {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: clamp(14px, 2vw, 22px);
}
.cards__head {
  margin-bottom: 0;
}
.cards__h {
  font-family: var(--disp);
  font-weight: 900;
  font-size: clamp(40px, 8vw, 92px);
  line-height: 0.84;
  letter-spacing: -0.04em;
  text-transform: uppercase;
  margin: 6px 0 14px;
}
.cards__h em {
  color: var(--mauve);
  font-style: normal;
}
.pts {
  list-style: none;
  display: flex;
  flex-direction: column;
  margin-top: 8px;
}
.pt {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 4px;
  border-top: 2px solid var(--border);
  transition: padding-left 0.16s ease;
}
.pt:last-child {
  border-bottom: 2px solid var(--border);
}
.pt__n {
  font-family: var(--mono);
  font-weight: 800;
  font-size: 13px;
  letter-spacing: 0.1em;
  color: var(--a);
}
.pt__t {
  flex: 1;
  font-family: var(--disp);
  font-weight: 800;
  font-size: clamp(20px, 3.2vw, 32px);
  line-height: 1;
  letter-spacing: -0.02em;
  text-transform: uppercase;
}
.pt__mark {
  width: 16px;
  height: 16px;
  border: 2px solid var(--a);
  transition: background 0.16s ease, transform 0.16s ease;
}
.pt:hover {
  padding-left: 12px;
}
.pt:hover .pt__mark {
  background: var(--a);
  transform: rotate(45deg);
}

@media (max-width: 900px) {
  .feat__grid {
    grid-template-columns: 1fr;
  }
  .cards {
    order: -1;
  }
  .label {
    position: static;
    max-width: 440px;
  }
}
</style>
