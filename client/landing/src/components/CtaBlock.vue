<script setup lang="ts">
const bars = Array.from({ length: 58 }, (_, i) => {
  const seq = (i * 73 + 17) % 11
  return seq < 4 ? 2 : seq < 8 ? 4 : 7
})
</script>

<template>
  <section class="cta">
    <div class="shell">
      <div class="cta__box" data-reveal>
        <div class="cta__grain" aria-hidden="true"></div>

        <div class="cta__inner">
          <p class="cta__kicker">
            <span class="cta__dot" aria-hidden="true"></span>
            начни сегодня · это бесплатно
          </p>
          <h2 class="cta__h">
            ЗАПУСКАЙ<br />
            <span class="cta__stripe">EAT-LOG</span>
          </h2>
          <p class="cta__lede">
            Записал приём — увидел свои КБЖУ. Ставь десктоп, веди дневник
            и держи дневную норму на виду.
          </p>

          <div class="cta__row">
            <a
              class="cta__btn"
              href="https://github.com/Nickolashaa/EatLog/releases/latest"
              target="_blank"
              rel="noopener"
              data-magnet
            >
              Скачать десктоп <span aria-hidden="true">→</span>
            </a>
            <a
              class="cta__link"
              href="https://github.com/Nickolashaa/EatLog"
              target="_blank"
              rel="noopener"
              data-magnet
            >
              Исходники на GitHub
            </a>
          </div>
        </div>

        <div class="cta__code" aria-hidden="true">
          <div class="cta__bars">
            <i v-for="(w, i) in bars" :key="i" :style="{ width: w + 'px' }"></i>
          </div>
          <div class="cta__digits">EAT·LOG&nbsp;·&nbsp;КБЖУ&nbsp;·&nbsp;0&nbsp;4&nbsp;2&nbsp;0</div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta {
  padding: clamp(30px, 5vw, 60px) 0 clamp(50px, 8vw, 90px);
}
.cta__box {
  position: relative;
  overflow: hidden;
  border: var(--edge) solid var(--ink);
  background: var(--mauve);
  color: var(--crust);
  box-shadow: 14px 14px 0 var(--ink);
  display: grid;
  grid-template-columns: 1.4fr 0.6fr;
}
.cta__grain {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(17, 17, 27, 0.14) 1px, transparent 1px),
    linear-gradient(90deg, rgba(17, 17, 27, 0.14) 1px, transparent 1px);
  background-size: 22px 22px;
}
.cta__inner {
  position: relative;
  padding: clamp(28px, 5vw, 60px);
}
.cta__kicker {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  font-family: var(--mono);
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.cta__dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--crust);
  animation: cbl 1s steps(1) infinite;
}
@keyframes cbl {
  50% {
    opacity: 0.2;
  }
}
.cta__h {
  font-family: var(--disp);
  font-weight: 900;
  font-size: clamp(40px, 8vw, 100px);
  line-height: 0.84;
  letter-spacing: -0.045em;
  text-transform: uppercase;
  margin: 16px 0 clamp(34px, 5vw, 58px);
}
.cta__stripe {
  display: inline-block;
  margin-top: 0.28em;
  color: var(--mauve);
  background: var(--crust);
  padding: 0 0.1em 0.04em;
  box-shadow: 8px 8px 0 var(--blue);
}
.cta__stripe em {
  color: var(--green);
  font-style: normal;
}
.cta__lede {
  max-width: 44ch;
  font-size: 15px;
  line-height: 1.6;
  font-weight: 500;
  color: color-mix(in srgb, var(--crust) 82%, transparent);
}
.cta__row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 18px;
  margin-top: 28px;
}
.cta__btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--disp);
  font-weight: 800;
  font-size: 17px;
  color: var(--mauve);
  background: var(--crust);
  border: var(--edge) solid var(--ink);
  padding: 15px 24px;
  box-shadow: 6px 6px 0 var(--blue);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.cta__btn:hover {
  transform: translate(-2px, -2px);
  box-shadow: 9px 9px 0 var(--blue);
}
.cta__btn:active {
  transform: translate(3px, 3px);
  box-shadow: 0 0 0 var(--blue);
}
.cta__btn span {
  transition: transform 0.16s ease;
}
.cta__btn:hover span {
  transform: translateX(4px);
}
.cta__link {
  font-family: var(--mono);
  font-weight: 800;
  font-size: 13px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  text-decoration: underline;
  text-underline-offset: 4px;
  text-decoration-thickness: 2px;
}

.cta__code {
  position: relative;
  border-left: var(--edge) solid var(--ink);
  background: var(--crust);
  color: var(--text);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 10px;
  padding: 22px 18px;
}
.cta__bars {
  display: flex;
  align-items: flex-end;
  gap: 3px;
  height: 100%;
  min-height: 120px;
}
.cta__bars i {
  display: block;
  height: 100%;
  background: var(--text);
}
.cta__bars i:nth-child(3n) {
  height: 82%;
}
.cta__bars i:nth-child(4n) {
  background: var(--mauve);
}
.cta__digits {
  font-family: var(--mono);
  font-weight: 700;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-align: center;
  color: var(--muted);
}

@media (max-width: 780px) {
  .cta__box {
    grid-template-columns: 1fr;
  }
  .cta__code {
    border-left: none;
    border-top: var(--edge) solid var(--ink);
    flex-direction: row;
    align-items: center;
  }
  .cta__bars {
    min-height: 60px;
    flex: 1;
  }
  .cta__digits {
    writing-mode: vertical-rl;
  }
}
</style>
